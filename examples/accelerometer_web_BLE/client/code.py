# SPDX-FileCopyrightText: 2020 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This example solicits that devices that provide the acceleration service connect to it, initiates
pairing and then prints the value every second.
"""

import time
import adafruit_ble
from adafruit_ble.advertising.standard import SolicitServicesAdvertisement
from adafruit_ble_adafruit.accelerometer_service import AccelerometerService

# from adafruit_ble.services.standard import CurrentTimeService
print("Setting up radio")
radio = adafruit_ble.BLERadio()
a = SolicitServicesAdvertisement()
a.complete_name = "CPLAY"
print("adding acclerometer service to advertisement")
a.solicited_services.append(AccelerometerService)
print("Starting advertising")
radio.start_advertising(a)
print("Advertising, waiting for connection")

COUNTER=10000
while not radio.connected:
    if COUNTER == 0:
        COUNTER=10000
        print("waiting")
    COUNTER -= 1
print("connected")

while radio.connected:
    print("still connected")
    print("Connections:", radio.connections)
    for connection in radio.connections:
        print("Connection:", connection)
        if not connection.paired:
            print(dir(connection))
            print("pairing")
            connection.pair()
            print("paired")
        else:
            print("already paired")
        cts = connection[AccelerometerService]
        print(dir(cts))
        if hasattr(cts, "acceleration"):
            print("Acceleration:", cts.acceleration)
        if hasattr(cts, "x"):
            print("X:", cts.x)
            print("Y:", cts.y)
            print("Z:", cts.z)
    time.sleep(1)

print("disconnected")
