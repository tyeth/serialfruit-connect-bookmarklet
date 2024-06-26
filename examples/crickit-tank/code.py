# SPDX-FileCopyrightText: 2019 John Edgar Park for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# CircuitPython BLE Rover
# Use with the Adafruit BlueFruit LE Connect app
# Works with CircuitPython 4.0.0-beta.1 and later
# running on an nRF52840 Feather board and Crickit FeatherWing

#TODO: Look at https://learn.adafruit.com/crickit-flippy-robot for door lip in greenhouse
#NOTE: Original BLE project for Crickit https://learn.adafruit.com/circuitpython-ble-crickit-rover

DEBUG = False

import os
import re
import supervisor
import sys
import time
# sys.exit(0)
# from board_definitions import adafruit_matrixportal_s3 as board
import board
import io

import digitalio

from adafruit_crickit import crickit
servo1_pulses = (500, 2500)  # min and max pulse lengths for servo 1
servo2_pulses = (500, 2500)
servo3_pulses = (500, 2500)


def logError(error):
    print("=-> ** Error: ", end="")
    print(error)

try:
    from adafruit_ble import BLERadio
    from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
    from adafruit_ble.services.nordic import UARTService
    HAS_BLE = True
except ImportError as ie:
    if "bleio" in str(ie):
        logError(ImportError("This example does not work with the 'bleio' library. Please use 'adafruit_ble' and some external bluetooth daughter-board."))
    HAS_BLE = False

# Import the packet classes that will be used.
from adafruit_bluefruit_connect.packet import Packet
# from adafruit_bluefruit_connect.raw_text_packet import Packet
# Only the packet classes that are imported will be known to Packet.
from adafruit_bluefruit_connect.button_packet import ButtonPacket
from adafruit_bluefruit_connect.color_packet import ColorPacket
from adafruit_bluefruit_connect.raw_text_packet import RawTextPacket

fake_blue=False

# Feather nRF52840 Express
if board.board_id == "adafruit_feather_nrf52840_express":
    print("Using Feather nRF52840 Express")
    # Prep the status LEDs on the Feather
    blue_led = digitalio.DigitalInOut(board.BLUE_LED)
    red_led = digitalio.DigitalInOut(board.RED_LED)
    blue_led.direction = digitalio.Direction.OUTPUT
    red_led.direction = digitalio.Direction.OUTPUT

elif board.board_id == "adafruit_feather_esp32s2_tft":
    print("Using Feather ESP32-S2 TFT")
    fake_blue=True
elif board.board_id == "adafruit_feather_esp32_v2":
    print("Using Feather ESP32v2")
    fake_blue=True
    
    
# Prep the status LEDs on the Feather
if fake_blue:    
    #create fake object for blue LED that has a value Property that can be set and alters the onboard neopixel like a fake LED
    class fakeLED:
        def __init__(self):
            self._value = False
            from neopixel import NeoPixel
            self._neopixel = NeoPixel(board.NEOPIXEL,1)
        def value(self, value):
            self._value = value
            if value:
                self._neopixel.fill((0, 0, 255))
            else:
                self._neopixel.fill((0, 0, 0))
        def direction(self, direction):
            pass
    blue_led = fakeLED()

    # blue_led = digitalio.DigitalInOut(board.BLUE_LED)
    red_led = digitalio.DigitalInOut(board.LED)
    # blue_led.direction = digitalio.Direction.OUTPUT
    red_led.direction = digitalio.Direction.OUTPUT

try:
    import wifi
    HAS_WIFI = True
except ImportError as ie:
    if "wifi" in str(ie):
        logError(ImportError("This example does not work with the 'wifi' library. Please use 'adafruit_esp32spi' or 'adafruit_esp32spi_socket'."))
    HAS_WIFI = False

WAITING_DATA = 0  # used to keep track of available serial bytes.
# needed in a slow loop rather than recheck in each condition/branch
# (which leads to serial conditional stealing data from web workflow)

if HAS_BLE:
    ble = BLERadio()
    uart_service = UARTService()
    advertisement = ProvideServicesAdvertisement(uart_service)

# motor setup
motor_1 = crickit.dc_motor_1
motor_2 = crickit.dc_motor_2

FWD = -1.0
REV = 0.7

# servos
servo1 = crickit.servo_1
servo2 = crickit.servo_2
servo3 = crickit.servo_3
servo1.set_pulse_width_range(servo1_pulses[0], servo1_pulses[1])
servo2.set_pulse_width_range(servo2_pulses[0], servo2_pulses[1])
servo3.set_pulse_width_range(servo3_pulses[0], servo3_pulses[1])
servo1.angle = 90
servo2.angle = 90
servo3.angle = 90


# neopixel setup
crickit.init_neopixel(24, brightness = 0.2)  # create Crickit neopixel object
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 200)
PURPLE = (120, 0, 160)
YELLOW = (100, 100, 0)
AQUA = (0, 100, 100)
color = PURPLE  # current NeoPixel color
prior_color = PURPLE  # to store state of previous color when changing them
crickit.neopixel.fill(color)

def convert_slash_x_strings(input_string=''):
    result_bytes = bytearray()
    i = 0
    while i < len(input_string):
        if re.match(r'\\x[a-fA-F0-9]{2}', input_string[i:i+4]):
            # Convert matched hexadecimal string to bytes and extend bytearray
            result_bytes.extend(bytes.fromhex(input_string[i+2:i+4]))
            i += 4  # Skip the matched pattern
        else:
            # Handle cp1252 characters by encoding them back to cp1252 bytes
            # This prevents 'ord()' from being used on extended characters which can be out of the 0-255 range
            try:
                result_bytes.extend(input_string[i].encode('cp1252'))
            except UnicodeEncodeError:
                print(f"Error encoding character {input_string[i]} in cp1252")
            i += 1
    return bytes(result_bytes)

def serial_bytes_waiting(old_n=0):
    """Returns the number of bytes available to read from the serial connection(s)."""
    global WAITING_DATA
    WAITING_DATA = supervisor.runtime.serial_bytes_available
    # if n - old_n > 0:  # we read something extra!
    #     time.sleep(0.01)  # give some time to get all data - change to async
    #     return serial_bytes_waiting(n)
    return WAITING_DATA

def get_serial_data(should_convert_slash_x_strings=False):
    serial_data = bytearray()
    if not serial_bytes_waiting():
        if DEBUG: print("No serial bytes available, exiting get_serial_data()")
        return None
    print(f"get_serial_data({should_convert_slash_x_strings}) Serial Bytes Available: ", WAITING_DATA)
    while serial_bytes_waiting():
        serial_data += sys.stdin.read(1)  # Read data directly as bytes

    # Log the raw bytes coming in to diagnose the exact input
    print(f"Raw serial bytes ({len(serial_data)}): {serial_data}")

    if should_convert_slash_x_strings:
        # If you need to work with or display the data as string:
        decoded_string = serial_data.decode('utf-8')  # Decode using cp1252 for correct display/logging
        import cp1252
        print(f"Decoded string (cp1252): {decoded_string}")
        bytes_from_cp1252 = cp1252.get_decimals_from_string(decoded_string)
        print(f"Bytes from cp1252: {bytes_from_cp1252}")
        serial_bytes = bytes(bytes_from_cp1252)
        print(f"bytearray from cp1252: {serial_bytes}")
        # for char in decoded_string:
        #     print(f"Char: {char} - Ord: {bytes(char).encode('cp1252')}")
    else:
        # convert string to utf-8 by decimal char values from cp1252
        serial_bytes = bytes(serial_data)
        print(f"bytes from raw serial: {serial_bytes}")

    # # Convert bytearray to bytes for packet processing
    # serial_bytes = bytes(serial_data)

    # Use the converted bytes for packet creation or processing
    try:
        # make serial_bytes into a readable RawIO like stream
        raw_stream = io.BytesIO(serial_bytes)  # TODO: refactor this stream stuff
        decoded_packet = Packet.from_stream(raw_stream)  # Make sure packet expects bytes
        print("Decoded Packet: ", decoded_packet)
        return decoded_packet
    except ValueError as ve:
        print("Error: ", ve)
        print("Raw Text Packet decoding failed: is None")
    try:
        decoded_packet = Packet.from_bytes(serial_bytes)  # Make sure packet expects bytes
        print("Decoded Packet: ", decoded_packet)
        return decoded_packet
    except ValueError as ve:
        print("Error: ", ve)
        print("Packet decoding failed: is None")
    return None


print("WiFi/BLE Rover")
print("Use Web Browser or Adafruit Bluefruit app to connect")
#print mac address for BT and print IP address for WiFi
if wifi:
    print("WiFi MAC Address:", [hex(i) for i in wifi.radio.mac_address])
    print("WiFi IP Address:", wifi.radio.ipv4_address)
    print("URL: http://", wifi.radio.ipv4_address, ":" + str(os.getenv("CIRCUITPY_WEB_API_PORT", "80")), "/", sep="")
    
    def new_wifi_data_packet(passed_packet, check_connected_first=True):  # pylint: disable=unused-argument
        """Checks for data available and converts from web socket text to packet if possible."""
        if check_connected_first and not wifi.radio.connected:
            print("WiFi not connected, exiting new_wifi_data_packet()")
            return None
        if serial_bytes_waiting():
            print(f"new_wifi_data({passed_packet}, {check_connected_first}) Serial Bytes Available: ", WAITING_DATA)
            print("Web serial data comes as text, attempting to force decode:")
            passed_packet = get_serial_data(should_convert_slash_x_strings=True)
            print("Web Packet: ", passed_packet)
        else:
            if DEBUG:
                print("No serial bytes available, exiting new_wifi_data_packet()")
        return passed_packet

if HAS_BLE:
    print("BLE MAC Address:", [hex(i) for i in ble.address_bytes])

while True:
    if HAS_BLE:
        blue_led.value = False
        ble.start_advertising(advertisement)
        start_time = time.monotonic_ns()
        while (time.monotonic_ns() - start_time) / 1e9 < 15:
            if start_time > time.monotonic_ns():
                start_time = time.monotonic_ns() # handle rollover
            # Wait for a connection.
            if ble.connected:
                blue_led.value = True  # turn on blue LED when connected
                break
    while (HAS_BLE and ble.connected) or (HAS_WIFI and wifi.radio.connected) or \
        (supervisor.runtime.serial_connected):
        PACKET = None
        WAITING_DATA = 0
        if (HAS_BLE and uart_service.in_waiting):
            print("BLE Packet")
            # Packet is arriving.
            red_led.value = False  # turn off red LED
            PACKET = Packet.from_stream(uart_service)
        elif HAS_WIFI:
            PACKET=new_wifi_data_packet(PACKET) # updates WAITING_DATA from serial_bytes_waiting
            if PACKET:
                print("WiFi Packet Received!", PACKET)
                # get serial from web workflow serial or via webpage/API/sockets
                red_led.value = False  # turn off red LED
        # by rechecking serial bytes available here, we potentially accidentally steal new web data
        if (not PACKET and WAITING_DATA) or not HAS_WIFI: # refactor to update WAITINGDATA even if no wifi
            if DEBUG:
                print("No packet from BLE or WiFi, but Serial Bytes Available: ", WAITING_DATA)
            PACKET = get_serial_data(should_convert_slash_x_strings=False)
            if PACKET:
                print("Final check for Serial Packet successful: ", PACKET)
            else:
                continue
            # Packet is arriving.
            red_led.value = False  # turn off red LED
        if PACKET is not None:
            print("Valid Packet: ", PACKET)
            # DEBUG = False
            if isinstance(PACKET, ColorPacket):
                # Change the color.
                print("Color Packet: ", PACKET.color)
                color = PACKET.color
                crickit.neopixel.fill(color)
            

            # servos
            if isinstance(PACKET, RawTextPacket):
                print("Raw Text Packet: ", PACKET.text)
                # assume it's pan,tilt,roll servo angles 0-180
                try:
                    # comes as a byte string, with RT prefix
                    pan, tilt, roll = PACKET.text.decode()[2:].split(",")
                    print("Pan/Tilt/Roll: ", pan, tilt, roll)
                    pan = int(pan)
                    tilt = int(tilt)
                    roll = int(roll)
                    print("Setting Servo1-3 Pan/Tilt/Roll: ", pan, tilt, roll, end=" ")
                    crickit.servo_1.angle = pan
                    crickit.servo_2.angle = tilt
                    crickit.servo_3.angle = roll
                    print("Servo1-3 Pan/Tilt/Roll set")
                except Exception as e:
                    print("Error decoding raw packet to Pan/Tilt/Roll: ", e)


            # do this when buttons are pressed
            elif isinstance(PACKET, ButtonPacket) and PACKET.pressed:
                red_led.value = True  # blink to show a packet has been received
                if PACKET.button == ButtonPacket.UP:  # UP button pressed
                    crickit.neopixel.fill(color)
                    motor_1.throttle = FWD
                    motor_2.throttle = FWD
                elif PACKET.button == ButtonPacket.DOWN:  # DOWN button
                    crickit.neopixel.fill(color)
                    motor_1.throttle = REV
                    motor_2.throttle = REV
                elif PACKET.button == ButtonPacket.RIGHT:
                    prior_color = color
                    color = YELLOW
                    crickit.neopixel.fill(color)
                    motor_1.throttle = FWD
                    motor_2.throttle = FWD * 0.5
                elif PACKET.button == ButtonPacket.LEFT:
                    prior_color = color
                    color = YELLOW
                    crickit.neopixel.fill(color)
                    motor_1.throttle = FWD * 0.5
                    motor_2.throttle = FWD
                elif PACKET.button == ButtonPacket.BUTTON_1:
                    crickit.neopixel.fill(RED)
                    motor_1.throttle = 0.0
                    motor_2.throttle = 0.0
                    time.sleep(0.5)
                    crickit.neopixel.fill(color)
                elif PACKET.button == ButtonPacket.BUTTON_2:
                    color = GREEN
                    crickit.neopixel.fill(color)
                elif PACKET.button == ButtonPacket.BUTTON_3:
                    color = BLUE
                    crickit.neopixel.fill(color)
                elif PACKET.button == ButtonPacket.BUTTON_4:
                    color = PURPLE
                    crickit.neopixel.fill(color)
            # do this when some buttons are released
            elif isinstance(PACKET, ButtonPacket) and not PACKET.pressed:
                if PACKET.button == ButtonPacket.RIGHT:
                    print("released right")
                    color = prior_color
                    crickit.neopixel.fill(color)
                    motor_1.throttle = FWD
                    motor_2.throttle = FWD
                if PACKET.button == ButtonPacket.LEFT:
                    print("released left")
                    color = prior_color
                    crickit.neopixel.fill(color)
                    motor_1.throttle = FWD
                    motor_2.throttle = FWD
        else:
            if DEBUG:
                print("No packet received")


