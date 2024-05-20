# Web Serial Bookmarklet

This project is a web-based tool that allows you to send various types of data packets over a serial connection using the Web Serial API. It can be used with a variety of devices that support serial communication, including Bluefruit devices and others.

## Features

- **Color Picker**: Send color data.
- **Control Pad**: Send control commands.
- **Accelerometer**: Send accelerometer data from the device's sensors.
- **Terminal**: Send AT commands.
- **DFU**: Send Device Firmware Update packets.
- **Security**: Send security-related data.
- **Read/Write**: Send read and write data.
- **Notify**: Send notification data.
- **Scan**: Send scan data.
- **IO Pin**: Send IO Pin data.
- **Neopixel**: Send Neopixel data.
- **String**: Send string data.
- **Raw Data**: Send raw bytes and strings.
- **Location**: Send location data using manual input or the device's GPS.

## Getting Started

### Prerequisites

- A device (running circuitpython?) that supports serial communication.
- Using web workflow requires any compatible browser
- Using USB-Serial or BLE requires a web browser that supports the Web Serial or BLE API

_If you have problems then try a Chromium based web browser (e.g., Chrome, Edge)._

### Usage

See `./examples` folder for a Crickit based project that previously required bluetooth

Next is a link to the bookmarklet code which you can right click <a href="javascript:(function(){var script=document.createElement('script');script.src='https://cdn.jsdelivr.net/gh/tyeth/serialfruit-connect@v0.0.9/src/bookmarklet.js';document.body.appendChild(script);})();">HERE</a> and choose add to favourites/bookmark,

Or the bookmarklet code to copy and paste into address bar: 
```
javascript:(function() {
    var script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/gh/tyeth/serialfruit-connect@v0.0.9/src/bookmarklet.js';
    document.body.appendChild(script);
})();
```
_(You may need to add the `javascript:` prefix back into the address bar after pasting the code from above, as browsers remove it as part of keeping you safe - bookmarks are not affected by this protection)_


## Available User Interface (UI) screens


1. **Color Picker**:
    - Select a color using the color input.
    - Click "Send Color" to send the selected color data.

2. **Control Pad**:
    - Click on the directional buttons (Up, Down, Left, Right) to send control commands.

3. **Accelerometer**:
    - Click "Start/Stop Sending Data" to toggle sending accelerometer data.

4. **Terminal**:
    - Enter an AT command in the input box.
    - Click "Send Command" to send the command.

5. **DFU**:
    - Click "Choose File" to select a DFU file.
    - Click "Send DFU Packet" to send the DFU data.

6. **Security**:
    - Enter security data in the input box.
    - Click "Send Security Packet" to send the data.

7. **Read/Write**:
    - Enter data to read or write in the respective input boxes.
    - Click "Read" or "Write" to send the respective packets.

8. **Notify**:
    - Enter notification data in the input box.
    - Click "Send Notify Packet" to send the data.

9. **Scan**:
    - Click "Send Scan Packet" to send a scan packet.

10. **IO Pin**:
    - Enter IO Pin data in the input box.
    - Click "Send IO Pin Packet" to send the data.

11. **Neopixel**:
    - Enter Neopixel data in the input box.
    - Click "Send Neopixel Packet" to send the data.

12. **String**:
    - Enter a string in the input box.
    - Click "Send String Packet" to send the string data.

13. **Raw Data**:
    - Enter raw bytes (comma-separated) or a raw string in the respective input boxes.
    - Click "Send Raw Bytes" or "Send Raw String" to send the data.

14. **Location**:
    - Enter latitude and longitude manually, or click "Use Current Location" to get the device's current location.
    - Click "Send Location" to send the location data.

### Screenshots

![Main Menu](screenshots/main-menu.png)
![Color Picker](screenshots/color-picker.png)
![Control Pad](screenshots/control-pad.png)
![Accelerometer](screenshots/accelerometer.png)
![Terminal](screenshots/terminal.png)
![DFU](screenshots/dfu.png)
![Security](screenshots/security.png)
![Read/Write](screenshots/read-write.png)
![Notify](screenshots/notify.png)
![Scan](screenshots/scan.png)
![IO Pin](screenshots/iopin.png)
![Neopixel](screenshots/neopixel.png)
![String](screenshots/string.png)
![Raw Data](screenshots/raw.png)
![Location](screenshots/location.png)

### Contributing

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Acknowledgments

- [Adafruit Bluefruit Connect](https://learn.adafruit.com/bluefruit-le-connect)
- [Web Serial API](https://developer.mozilla.org/en-US/docs/Web/API/Serial)
