# BlueFruit Connect Adaptation for Crickit Tank

This project is an adaptation of the Crickit Tank project for the FeatherWing Crickit, with added support for Bluetooth, Wi-Fi, and USB connectivity. It utilizes a JavaScript bookmarklet to access devices through a Chromium-based browser.

## Prerequisites

Before getting started, make sure you have the following:

- FeatherWing Crickit
- Chromium-based browser (e.g., Google Chrome)
- Bluetooth, Wi-Fi, or USB enabled device

## Usage

1. Connect your FeatherWing Crickit to your device, load example code and required modules.
2. Open your Chromium-based browser and navigate to the web serial page, connect device to browser serial page.
3. Use the bookmarklet URL and paste into address bar.
4. Notice the side panel that now appears (otherwise check dev console and report issue)
5. Follow the on-screen instructions in panel to control the Crickit Tank using Bluetooth, Wi-Fi, or USB.

## Development

You'll need the following to stop your editor moaning about imports on a real computer:
```shell
pip install circuitpython-stubs --upgrade
circuitpython_setboard adafruit_feather_esp32s3_4mbflash_2mbpsram
pip install adafruit-circuitpython-ble --upgrade
pip install adafruit-circuitpython-bluefruitconnect --upgrade
pip install adafruit-circuitpython-crickit --upgrade
pip install adafruit-circuitpython-neopixel --upgrade
echo "use circuitpython_setboard --list to show other boards"
```

## Contributing

Contributions are welcome! If you have any ideas, suggestions, or bug reports, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).