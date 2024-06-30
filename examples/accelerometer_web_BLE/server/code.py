# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-FileCopyrightText: 2024 Tyeth Gundry for Adafruit Industries
# SPDX-License-Identifier: MIT

# Adafruit BLE Service demo for Adafruit Feather Bluefruit Sense board, may work
# with other boards. Accessible via Adafruit Web Bluetooth Dashboard / BlueFruit apps.
# (As of this writing, 2021, not yet accessible via Bluefruit Playground app.)

import time

import board
import busio
import digitalio
import neopixel_write

from ulab import numpy as np

from adafruit_ble import BLERadio

import audiobusio

import adafruit_apds9960.apds9960
import adafruit_bmp280
import adafruit_lsm6ds.lsm6ds33
import adafruit_lsm9ds1
import adafruit_lsm303_accel
import adafruit_sht31d

from adafruit_ble_adafruit.adafruit_service import AdafruitServerAdvertisement

from adafruit_ble_adafruit.accelerometer_service import AccelerometerService
from adafruit_ble_adafruit.addressable_pixel_service import AddressablePixelService
from adafruit_ble_adafruit.barometric_pressure_service import BarometricPressureService
from adafruit_ble_adafruit.button_service import ButtonService
from adafruit_ble_adafruit.humidity_service import HumidityService
from adafruit_ble_adafruit.light_sensor_service import LightSensorService
from adafruit_ble_adafruit.microphone_service import MicrophoneService
from adafruit_ble_adafruit.temperature_service import TemperatureService

i2c = board.I2C() if hasattr(board, "I2C") else \
    board.STEMMA_I2C() if hasattr(board, "STEMMA_I2C") else \
    busio.I2C(board.SCL, board.SDA) if hasattr(board, "SCL") else \
    busio.I2C(board.SCL1, board.SDA1) if hasattr(board, "SCL1") else \
    busio.I2C(board.IO2, board.IO1) # LilyGo T-Display S3 - Set your pins here!
    # busio.I2C(board.STEMMA_SCL, board.STEMMA_SDA) if hasattr(board, "STEMMA_SCL") else \

# Set your button pin here:
button_pin = board.SWITCH if hasattr(board, "SWITCH") \
    else board.BUTTON0 if hasattr(board, "BUTTON0") \
    else board.BOOT0 if hasattr(board, "BOOT0") \
    else board.BOOT if hasattr(board, "BOOT") \
    else board.D0 # esp boot button - Set your button pin here!

try:
    # Accelerometer
    lsm6ds33 = adafruit_lsm6ds.lsm6ds33.LSM6DS33(i2c)
    print("Using LSM6DS33 accelerometer. Current value: ", lsm6ds33.acceleration)
except Exception as e:
    print("No LSM6DS33 found.", e)
    lsm6ds33 = None

if lsm6ds33 is None:
    try:
        # Alternative accelerometer
        lms9ds1 = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)
        lsm6ds33 = lms9ds1
        #{"acceleration": lms9ds1.acceleration, "gyro": lms9ds1.gyro, "magnetic": lms9ds1.magnetic}
        print("Using LSM9DS1 accelerometer. Current value: ", lms9ds1.acceleration)
    except Exception as e:
        print("No LSM9DS1 found.", e)
        lsm6ds33 = None

if lsm6ds33 is None:
    try:
        # Alternative accelerometer
        lsm303 = adafruit_lsm303_accel.LSM303_Accel(i2c)
        lsm6ds33 = lsm303
        print("Using LSM303 accelerometer, current value: ", lsm303.acceleration)
    except Exception as e:
        print(e, "\nNo LSM303 detected. (No accelerometers found)")
        lsm6ds33 = None


try:
    # Used for pressure and temperature.
    bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
except:
    bmp280 = None

try:
    # Humidity.
    sht31d = adafruit_sht31d.SHT31D(i2c)
except:
    sht31d = None

try:
    # Used only for light sensor
    apds9960 = adafruit_apds9960.apds9960.APDS9960(i2c)
    apds9960.enable_color = True
except:
    apds9960 = None

if hasattr(board, "MICROPHONE_CLOCK") and hasattr(board, "MICROPHONE_DATA"):
    mic = audiobusio.PDMIn(
        board.MICROPHONE_CLOCK,
        board.MICROPHONE_DATA,
        sample_rate=16000,
        bit_depth=16,
    )
else:
    mic = None

# Create and initialize the available services.
if lsm6ds33 is not None:
    accel_svc = AccelerometerService()
    accel_svc.measurement_period = 500
    accel_last_update = 0

if hasattr(board, "NEOPIXEL"):
    # Feather Bluefruit Sense has just one board pixel. 3 RGB bytes * 1 pixel
    NEOPIXEL_BUF_LENGTH = 3 * 1
    neopixel_svc = AddressablePixelService()
    neopixel_buf = bytearray(NEOPIXEL_BUF_LENGTH)
    neopixel_out = digitalio.DigitalInOut(board.NEOPIXEL)
    neopixel_out.switch_to_output()
else:
    neopixel_svc = None

if bmp280 is not None:
    baro_svc = BarometricPressureService()
    baro_svc.measurement_period = 100
    baro_last_update = 0

button_svc = ButtonService()
button = digitalio.DigitalInOut(button_pin)
button.pull = digitalio.Pull.UP
button_svc.set_pressed(False, not button.value, False)

if sht31d is not None:
    humidity_svc = HumidityService()
    humidity_svc.measurement_period = 100
    humidity_last_update = 0

if apds9960 is not None:
    light_svc = LightSensorService()
    light_svc.measurement_period = 100
    light_last_update = 0

if mic is not None:
    # Send 256 16-bit samples at a time.
    MIC_NUM_SAMPLES = 256
    mic_svc = MicrophoneService()
    mic_svc.number_of_channels = 1
    mic_svc.measurement_period = 100
    mic_last_update = 0
    mic_samples = np.zeros(MIC_NUM_SAMPLES, dtype=np.uint16)

if bmp280 is not None or sht31d is not None:
    temp_svc = TemperatureService()
    temp_svc.measurement_period = 100
    temp_last_update = 0
else:
    temp_svc = None

# if none enabled then print msg
if (
    lsm6ds33 is None
    and bmp280 is None
    and sht31d is None
    and apds9960 is None
    and mic is None
):
    print("No sensors found. Exiting.")
    raise Exception("No sensors found.")


ble = BLERadio()
# The Web Bluetooth dashboard identifies known boards by their
# advertised name, not by advertising manufacturer data.
ble.name = "Sense" # Pretend to be a Feather Bluefruit Sense

# The Bluefruit Playground app looks in the manufacturer data
# in the advertisement. That data uses the USB PID as a unique ID.
# Feather Bluefruit Sense USB PID:
# This board is not yet support on the app.
# Arduino: 0x8087,  CircuitPython: 0x8088
adv = AdafruitServerAdvertisement()
adv.pid = 0x8088

while True:
    # Advertise when not connected.
    ble.start_advertising(adv)
    while not ble.connected:
        pass
    ble.stop_advertising()

    while ble.connected:
        now_msecs = time.monotonic_ns() // 1000000  # pylint: disable=no-member

        if lsm6ds33 is not None and now_msecs - accel_last_update >= accel_svc.measurement_period:
            accel_svc.acceleration = lsm6ds33.acceleration
            accel_last_update = now_msecs

        if bmp280 is not None and now_msecs - baro_last_update >= baro_svc.measurement_period:
            baro_svc.pressure = bmp280.pressure
            baro_last_update = now_msecs

        button_svc.set_pressed(False, not button.value, False)

        if sht31d is not None and now_msecs - humidity_last_update >= humidity_svc.measurement_period:
            humidity_svc.humidity = sht31d.relative_humidity
            humidity_last_update = now_msecs

        if apds9960 is not None and now_msecs - light_last_update >= light_svc.measurement_period:
            # Return "clear" color value from color sensor.
            light_svc.light_level = apds9960.color_data[3]
            light_last_update = now_msecs

        if mic is not None and now_msecs - mic_last_update >= mic_svc.measurement_period:
            mic.record(mic_samples, len(mic_samples))
            # This subtraction yields unsigned values which are
            # reinterpreted as signed after passing.
            mic_svc.sound_samples = mic_samples - 32768
            mic_last_update = now_msecs

        if neopixel_svc is not None:
            neopixel_values = neopixel_svc.values
            if neopixel_values is not None:
                start = neopixel_values.start
                if start > NEOPIXEL_BUF_LENGTH:
                    continue
                data = neopixel_values.data
                data_len = min(len(data), NEOPIXEL_BUF_LENGTH - start)
                neopixel_buf[start : start + data_len] = data[:data_len]
                if neopixel_values.write_now:
                    neopixel_write.neopixel_write(neopixel_out, neopixel_buf)

        if (sht31d is not None or bmp280 is not None) and now_msecs - temp_last_update >= temp_svc.measurement_period:
            temp_svc.temperature = bmp280.temperature if bmp280 is not None else sht31d.temperature
            temp_last_update = now_msecs
