# SPDX-FileCopyrightText: 2019 John Edgar Park for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# CircuitPython BLE Rover
# Use with the Adafruit BlueFruit LE Connect app
# Works with CircuitPython 4.0.0-beta.1 and later
# running on an nRF52840 Feather board and Crickit FeatherWing

#TODO: Look at https://learn.adafruit.com/crickit-flippy-robot for door lip in greenhouse
#NOTE: Original BLE project for Crickit https://learn.adafruit.com/circuitpython-ble-crickit-rover


import os
import re
import supervisor
import sys
import time

# from board_definitions import adafruit_matrixportal_s3 as board
import board

import digitalio

from adafruit_crickit import crickit

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
# Only the packet classes that are imported will be known to Packet.
from adafruit_bluefruit_connect.button_packet import ButtonPacket
from adafruit_bluefruit_connect.color_packet import ColorPacket

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
    # Prep the status LEDs on the Feather
    
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

if HAS_BLE:
    ble = BLERadio()
    uart_service = UARTService()
    advertisement = ProvideServicesAdvertisement(uart_service)

# motor setup
motor_1 = crickit.dc_motor_1
motor_2 = crickit.dc_motor_2

FWD = -1.0
REV = 0.7

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

def convert_slashXstrings(input_string=''):
    result_bytes = bytearray()
    i = 0
    while i < len(input_string):
        if re.match(f'\\x[a-fA-F0-9]{2}', input_string[i:i+4]):
            result_bytes.extend(bytes.fromhex(input_string[i+2:i+4]))
            i += 4
        else:
            result_bytes.append(ord(input_string[i]))
            i += 1
    return bytes(result_bytes)

def check_for_waiting_serial(old_n=0):
    n = supervisor.runtime.serial_bytes_available
    # if n - old_n > 0:  # we read something extra!
    #     time.sleep(0.01)  # give some time to get all data - change to async
    #     return check_for_waiting_serial(n)
    return n

def get_serial_data(should_convert_slash_x_strings=False):
    #store bytes from serial and then create packet from it
    s=''
    while supervisor.runtime.serial_bytes_available:
        try:
            n = check_for_waiting_serial()
            if n > 0:  # we read something!
                print("New Serial Data: ",n)
                # packet = Packet.from_stream(sys.stdin)
                # print("Packet: ", packet)
                # s = input()  # read a line from the serial input
                s = sys.stdin.read()  # actually read it in - don't pass n as seemed wrong for web workflow
                print(f"Read {n} bytes: {s}")
                # convert \xXX from incoming string, e.g. '!C\x20\x20\x20;' = b'!C   ;' (end up convert whole string to bytes)
                if should_convert_slash_x_strings:
                    s = convert_slashXstrings(s)
                    print("Converted: ", s)

                # print both text & hex version of recv'd chars (see control chars!)
                print("got:", ", ".join("{:s} ({:02d}=\\x{:02x})".format(c,ord(c),ord(c)) for c in s))
                print(s)
                print(bytes(s, 'utf-8'))
        except Exception as e:
            print("Error: ", e)
        
        if s==b'\x04': #ctrl-d
            print("Ctrl-D received, rebooting / exiting in 3 seconds")
            time.sleep(3)
            if hasattr(supervisor, "reload"):
                supervisor.reload()
            else:
                sys.exit()
    if s:
        try:
            decoded_packet = Packet.from_bytes(s)
            return decoded_packet
        except ValueError as e:
            print("Error: ", e)
            print("Packet decoding failed: is None")
    return None


print("WiFi/BLE Rover")
print("Use Web Browser or Adafruit Bluefruit app to connect")
#print mac address for BT and print IP address for WiFi
if wifi:
    print("WiFi MAC Address:", [hex(i) for i in wifi.radio.mac_address])
    print("WiFi IP Address:", wifi.radio.ipv4_address)
    print("URL: http://", wifi.radio.ipv4_address, ":" + str(os.getenv("CIRCUITPY_WEB_API_PORT", 80)), "/", sep="")
    def new_wifi_data_packet(passed_packet):  # pylint: disable=unused-argument
        if supervisor.runtime.serial_bytes_available:
            print("Serial Bytes Available: ", supervisor.runtime.serial_bytes_available)
            print("Web serial data comes as text, attempting to force decode:")
            passed_packet = get_serial_data(should_convert_slash_x_strings=True)
            print("Web Packet: ", passed_packet)
            return True
        return False
        # if wifi.radio.connected:
        #     return True
        # else:
        #     return False

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
    while (HAS_BLE and ble.connected) or (HAS_WIFI and wifi.radio.connected) or (not HAS_BLE and not HAS_WIFI and supervisor.runtime.serial_connected):
        packet = None
        if (HAS_BLE and uart_service.in_waiting):
            print("BLE Packet")
            # Packet is arriving.
            red_led.value = False  # turn off red LED
            packet = Packet.from_stream(uart_service)
        elif (HAS_WIFI and new_wifi_data_packet(packet)):
            print("WiFi Packet")
            # get serial from web workflow serial or via webpage/API/sockets
            red_led.value = False  # turn off red LED
        if not packet:
            packet = get_serial_data(should_convert_slash_x_strings=False)
            if packet:
                print("Serial Packet")
            else:
                continue
            # Packet is arriving.
            red_led.value = False  # turn off red LED
        if packet is not None:
            if isinstance(packet, ColorPacket):
                # Change the color.
                print("Color Packet: ", packet.color)
                color = packet.color
                crickit.neopixel.fill(color)

            # do this when buttons are pressed
            if isinstance(packet, ButtonPacket) and packet.pressed:
                red_led.value = True  # blink to show a packet has been received
                if packet.button == ButtonPacket.UP:  # UP button pressed
                    crickit.neopixel.fill(color)
                    motor_1.throttle = FWD
                    motor_2.throttle = FWD
                elif packet.button == ButtonPacket.DOWN:  # DOWN button
                    crickit.neopixel.fill(color)
                    motor_1.throttle = REV
                    motor_2.throttle = REV
                elif packet.button == ButtonPacket.RIGHT:
                    prior_color = color
                    color = YELLOW
                    crickit.neopixel.fill(color)
                    motor_1.throttle = FWD
                    motor_2.throttle = FWD * 0.5
                elif packet.button == ButtonPacket.LEFT:
                    prior_color = color
                    color = YELLOW
                    crickit.neopixel.fill(color)
                    motor_1.throttle = FWD * 0.5
                    motor_2.throttle = FWD
                elif packet.button == ButtonPacket.BUTTON_1:
                    crickit.neopixel.fill(RED)
                    motor_1.throttle = 0.0
                    motor_2.throttle = 0.0
                    time.sleep(0.5)
                    crickit.neopixel.fill(color)
                elif packet.button == ButtonPacket.BUTTON_2:
                    color = GREEN
                    crickit.neopixel.fill(color)
                elif packet.button == ButtonPacket.BUTTON_3:
                    color = BLUE
                    crickit.neopixel.fill(color)
                elif packet.button == ButtonPacket.BUTTON_4:
                    color = PURPLE
                    crickit.neopixel.fill(color)
            # do this when some buttons are released
            elif isinstance(packet, ButtonPacket) and not packet.pressed:
                if packet.button == ButtonPacket.RIGHT:
                    print("released right")
                    color = prior_color
                    crickit.neopixel.fill(color)
                    motor_1.throttle = FWD
                    motor_2.throttle = FWD
                if packet.button == ButtonPacket.LEFT:
                    print("released left")
                    color = prior_color
                    crickit.neopixel.fill(color)
                    motor_1.throttle = FWD
                    motor_2.throttle = FWD
