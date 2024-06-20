document.addEventListener("DOMContentLoaded", () => {
    showScreen('main-menu');
});

function showScreen(screenId) {
    document.querySelectorAll('.screen').forEach(screen => {
        screen.style.display = 'none';
    });
    document.getElementById(screenId).style.display = 'grid';
}

// Base class for Bluefruit packets
class BluefruitPacket {
    constructor(packetType, payload) {
        this.packetType = packetType;
        this.payload = payload;
        this.packetLen = payload.length;
    }

    toBytes() {
        const partialPacket = new Uint8Array([ ...this.packetType.split('').map(c => c.charCodeAt(0)), ...this.payload]);
        const checksum = this.checksum(partialPacket);
        return Uint8Array.from([...partialPacket, checksum]);
    }

    toArray() {
        return Array.from(this.toBytes());
    }

    checksum(packet) {
        return ~packet.reduce((sum, value) => sum + value, 0) & 0xFF;
    }
}

// Packet classes for specific types
class XYZPacket extends BluefruitPacket {
    constructor(x, y, z) {
        const payload = new Float32Array([x, y, z]).buffer;
        super('!XYZ', new Uint8Array(payload));
    }
}

class AccelerometerPacket extends XYZPacket {
    constructor(x, y, z) {
        super(x, y, z);
    }
}

class StringPacket extends BluefruitPacket {
    constructor(string) {
        const payload = new TextEncoder().encode(string);
        super('!S', payload);
    }
}

class RawPacket extends BluefruitPacket {
    constructor(bytes) {
        const payload = new Uint8Array(bytes);
        super('!R', payload);
    }
}

class DFUPacket extends BluefruitPacket {
    constructor(data) {
        const payload = new Uint8Array(data);
        super('!D', payload);
    }
}

class ButtonPacket extends BluefruitPacket {
    /*
    BUTTON_1: str = "1"
    """Code for Button 1 on the Bluefruit LE Connect app Control Pad screen."""
    BUTTON_2: str = "2"
    """Button 2."""
    BUTTON_3: str = "3"
    """Button 3."""
    BUTTON_4: str = "4"
    """Button 4."""
    UP: str = "5"
    """Up Button."""
    DOWN: str = "6"
    """Down Button."""
    LEFT: str = "7"
    """Left Button."""
    RIGHT: str = "8"
    """Right Button."""
     */
    constructor(button, pressed) {
        const payload = new Uint8Array(
            [
                ...String(button).split('').map(x=>x.charCodeAt(0)),
                ...(pressed ? "1":"0").split('').map(y=>y.charCodeAt(0))
            ]
        );
        super('!B', payload);
    }
}

class ColorPacket extends BluefruitPacket {
    constructor(r, g, b) {
        const payload = new Uint8Array([r, g, b]);
        super('!C', payload);
    }
}

class GyroPacket extends XYZPacket {
    constructor(x, y, z) {
        super(x, y, z);
    }
}

class LocationPacket extends BluefruitPacket {
    constructor(latitude, longitude, altitude) {
        const payload = new Float32Array([latitude, longitude, altitude]).buffer;
        super('!L', new Uint8Array(payload));
    }
}

class MagnetometerPacket extends XYZPacket {
    constructor(x, y, z) {
        super(x, y, z);
    }
}

class QuaternionPacket extends BluefruitPacket {
    constructor(w, x, y, z) {
        const payload = new Float32Array([w, x, y, z]).buffer;
        super('!Q', new Uint8Array(payload));
    }
}

class RawTextPacket extends BluefruitPacket {
    constructor(text) {
        const payload = new TextEncoder().encode(text);
        super('!T', payload);
    }
}

class ATCommandPacket extends BluefruitPacket {
    constructor(commandString) {
        const payload = Array.from(new TextEncoder().encode(commandString));
        super('!A', payload);
    }
}

class ControlCommandPacket extends BluefruitPacket {
    constructor(command, value) {
        const payload = [command, value];
        super('!D', payload);
    }
}

class TemperaturePacket extends BluefruitPacket {
    constructor(temperature) {
        const payload = new Float32Array([temperature]).buffer;
        super('!T', new Uint8Array(payload));
    }
}


class SerialFruit {
    constructor() {
        this._trackedSockets = [];
        // Initialize global variables for serial port and writer
        this._port, this._writer, this._webworkflow_serial, this._ble_serial, this._web_usb_serial, this._accelerometerEnabled = false;
    }

    getTrackedSockets() {
        return this._trackedSockets;
    }

    cleanTrackedSockets() {
        this._trackedSockets = this._trackedSockets.filter((x) => (x instanceof WebSocket && x?.readyState == 1) ||
            (x instanceof SerialPort && x?.readable && x?.writable) ||
            (x instanceof BluetoothDevice && x?.gatt?.connected));
    }

        
    
    // Connect to serial or web serial (or eventually BLE serial)
    async connectAnySerial() {
        if (writer) return;
        if (webworkflow_serial || web_usb_serial) {
            //setup textencoder for writer to websocket
            if (!window?.serialfruit?.getTrackedSockets) {
                console.error('WebSocket/Serialport/BLE tracking not enabled, enabling now...');
                await ensureEverythingHooked();
            }
            activeWebSocket = window.serialfruit.getTrackedSockets().find((ws) => ws.readyState === 1);
            if (activeWebSocket) {
                writer = {
                    write: async (data) => {
                        console.debug('Attempting to send packet after fetching websocket:', data);
                        if (!activeWebSocket || activeWebSocket.readyState !== 1) {
                            console.error("WebSocket not found or not connected, attempting to reget.");
                            activeWebSocket = window.serialfruit.getTrackedSockets().find((ws) => ws.readyState === 1);
                            if (!activeWebSocket) {
                                console.debug('WebSocket refetch failed:', window.serialfruit.getTrackedSockets());
                                debugger;
                                console.error("WebSocket not found or not connected.");
                                return;
                            }
                            console.log('WebSocket refetched:', activeWebSocket);
                        }
                        console.log('Sending packet:', data);
                        // circuirpython websocket uses text based comms
                        activeWebSocket.send(new TextDecoder('ascii',options={encoding:'ascii'}).decode(Uint8Array.from(data)));
                        console.log('Packet(s) sent:', data);
                    }
                };
            } else {
                console.error("WebSocket not found or not connected.");
            }
        } else if (ble_serial) {
            console.error("BLE serial not supported yet");
        } else {
            if ('serial' in navigator) {
                console.log("Attempting to connect to serial port...");
                await connectSerial();
            } else {
                console.error("Web USB-serial not supported, try a Chromium based browser like Chrome or Edge.");
            }
        }
    }

    // Connect to the serial port
    async connectSerial() {
        try {
            this._port = await navigator.serial.requestPort();
            await this._port.open({ baudRate: 115200 });
            this._writer = this._port.writable.getWriter();
            //TODO: refactor into ensureHooked so all transports setup trackedSockets array + func
            window.serialfruit._trackedSockets = window.serialfruit._trackedSockets || [];
            window.serialfruit.getTrackedSockets = window.serialfruit.getTrackedSockets || function () { return window.serialfruit._trackedSockets; };
            window.serialfruit._trackedSockets.push(port);
            console.log("Connected to serial port", port);
        } catch (error) {
            console.error("Failed to connect to serial port: ", error);
        }
    }

    async ensureEverythingHooked() {
        // monkey patch websockets to allow reuse
        if (window.serialfruit.getTrackedSockets) {
            console.log('WebSocket tracking already enabled.');
            if (window.serialfruit.getTrackedSockets().length > 1) {
                console.log('Cleaning up old closed connections');
                window.serialfruit.cleanTrackedSockets();
                console.log('Existing Closed WebSocket connections cleaned up.');
                if (window.serialfruit.getTrackedSockets().filter(ws => ws.readyState === 1).length > 1) {
                    console.log('Unexpected MULTIPLE Open Existing WebSocket connections:', window.serialfruit.getTrackedSockets());
                    for (const ws of window.serialfruit.getTrackedSockets().filter((x)=>x?.readyState===1)) {
                        console.log('Closing WebSocket:', ws);
                        ws.close();
                    }
                    console.error('Existing WebSocket connections forceably closed.');
                }
                return;
            } else if (window.serialfruit.getTrackedSockets().length === 1) {
                console.log('Existing WebSocket connection found:', window.serialfruit.getTrackedSockets()[0]);
            }
            return;
        } else {

            const originalWebSocket = window.WebSocket;
            const trackedSockets = [];
            
            function TrackingWebSocket(url, protocols) {
                const ws = new originalWebSocket(url, protocols);
                trackedSockets.push(ws);
                console.log('WebSocket created:', ws);
                return ws;
            }

            TrackingWebSocket.prototype = originalWebSocket.prototype;
            window.WebSocket = TrackingWebSocket;
            
            window.serialfruit.getTrackedSockets = function () {
                return trackedSockets;
            };
            window.serialfruit.cleanTrackedSockets = function () {
                trackedSockets = trackedSockets.filter((x) => (x instanceof WebSocket && x?.readyState == 1) ||
                    (x instanceof SerialPort && x?.readable && x?.writable) ||
                    (x instanceof BluetoothDevice && x?.gatt?.connected));
            };
            window.serialfruit._trackedSockets = trackedSockets;
            
            console.log('WebSocket tracking enabled.');
        }
    }

    async updateStatsTable() {
        if (window.serialfruit.getTrackedSockets) {
            let trackedSockets = window.serialfruit.getTrackedSockets();
            const deviceElement = document.getElementById('web-serial-device');
            const stateElement = document.getElementById('web-serial-state');
            let returnedDeviceAndStates = [];
            if (!trackedSockets || trackedSockets.length === 0) {
                returnedDeviceAndStates.push(['No tracked sockets', 'Disconnected'])
            } else {
                trackedSockets.forEach((ws) => {
                    if (ws instanceof WebSocket) {
                        deviceTextContents = ws.url;
                        switch (ws.readyState) {
                            case 0:
                                stateTextContents = 'connecting';
                                break;
                            case 1:
                                stateTextContents = 'open';
                                break;
                            case 2:
                                stateTextContents = 'closing';
                                break;
                            case 3:
                                stateTextContents = 'closed';
                                break;
                            default:
                                stateTextContents = ws.readyState;
                        }
                    } else if (ws instanceof SerialPort) {
                        let deviceInfo = SerialPort.prototype.getInfo.call(ws);
                        let deviceName = "Unknown Device";
                        if (deviceInfo && deviceInfo.hasOwnProperty('usbProductId') && deviceInfo.hasOwnProperty('usbVendorId')) {
                            deviceName = `Vid:${deviceInfo.usbVendorId} Pid:${deviceInfo.usbProductId}`;
                        }
                        deviceTextContents = "Uart: " + deviceName;
                        stateTextContents = ws.connected && ws.readable && ws.writable ? 'open' : 'closed';
                        // TODO: remove serialport connection from stats if closed and other connections available, also handle PolyFill
                    } else if (ws instanceof BluetoothDevice) {
                        deviceTextContents = "BT:" + ws.name;
                        stateTextContents = ws.gatt.connected ? 'open' : 'closed';
                    } else {
                        console.error('Unknown device type:', ws);
                        deviceTextContents = 'Unknown';
                        stateTextContents = 'Unknown';
                    }
                    returnedDeviceAndStates.push([deviceTextContents, stateTextContents]);
                });
            }
            if (returnedDeviceAndStates.length !== 0) {
                // Clear the table
                const statsTableBody = await this.asyncAwaitVisibleElement('#statsTableBody',500);
                if (!statsTableBody) {
                    console.error('Stats table body not found');
                    return;
                }
                while (statsTableBody?.firstChild) {
                    statsTableBody.removeChild(statsTableBody.firstChild);
                }

                returnedDeviceAndStates.forEach((item) => {
                    const deviceTextContents = item[0];
                    const stateTextContents = item[1];
                    // Create a new row for each device
                    const newRow = document.createElement('tr');
                    const deviceCell = document.createElement('td');
                    const stateCell = document.createElement('td');

                    deviceCell.textContent = deviceTextContents;
                    stateCell.textContent = stateTextContents;

                    newRow.appendChild(deviceCell);
                    newRow.appendChild(stateCell);

                    statsTableBody.appendChild(newRow);
                });
            }
        }
    }

    async asyncAwaitVisibleElement(selector, timeout=15000) {
        return new Promise((resolve, reject) => {
            let elements = document.querySelectorAll(selector);
            elements = Array.from(elements).filter((x) => x.offsetHeight !== 0);
            if (elements.length > 0) {
                resolve(elements[0]);
            } else {
                const observer = new MutationObserver((mutationsList, observer) => {
                    elements = document.querySelectorAll(selector);
                    elements = Array.from(elements).filter((x) => x.offsetHeight !== 0);
                    if (elements.length > 0) {
                        observer.disconnect();
                        clearTimeout(timeoutId); // Clear the timeout
                        resolve(elements[0]);
                    }
                });
                observer.observe(document.body, { childList: true, subtree: true });

                // Set a timeout to reject the promise if the element is not found within the specified time
                const timeoutId = setTimeout(() => {
                    observer.disconnect(); // Stop observing if timeout
                    console.error('Element not found within timeout:', selector);
                    resolve(null);
                }, timeout);
            }
        });
    }

    async getVisibleElement(selector) {
        let buttons = [...document.querySelectorAll(selector)];
        buttons = buttons.filter((x) => x.offsetHeight !== 0);
        return Array.isArray(buttons) ? buttons[0] : buttons;
    }


    // Ensure access to serial port and writer
    async ensureAddressAndSocketAccess() {
        if (window.location.host.match(/^((192.168)|(cpy-))/i)) {
            if (window.location.pathname.endsWith('cp/serial')) {
                webworkflow_serial = true;
                ensureEverythingHooked();
                debugger;
                this._activeWebSocket = this._activeWebSocket || null;
                this._activeWebSocket = this._activeWebSocket || new WebSocket('ws://' + window.location.host + '/ws/serial');
                // console.log('Sending packet:', packet);
                // activeWebSocket.send(packet.toArray());
                // console.log('Packet sent:', packet.toArray());
                return;
            } else if (window.location.pathname == "/code/") {
                webworkflow_serial = true;
                if (!window.serialfruit?.getTrackedSockets) {
                    await ensureEverythingHooked();
                
                    // check if device connected state on page and reconnect
                    let connectButton = await getVisibleElement('button.btn-connect');
                    if (connectButton) {
                        if (connectButton.innerText === 'Disconnect') {
                            console.log('Device already connected, disconnecting first');
                            connectButton.click();
                            setTimeout(async () => {
                                console.log('Reconnecting device');
                                let cButton = await asyncAwaitVisibleElement('button.btn-connect', 5000);
                                if (!cButton) {
                                    console.error('Visible "Connect" button not found');
                                    return;
                                }
                                cButton.click();
                                setTimeout(async () => {
                                    //button#web-workflow click
                                    console.log('Triggering button#web-workflow with event');
                                    // first trigger focusIn on <div class="popup-modal shadow prompt closable is--visible" 
                                    // and on button#web-workflow
                                    let wModal = await asyncAwaitVisibleElement('div.popup-modal.is--visible[data-popup-modal="connection-type"]');
                                    if (wModal){
                                        let focusInEvent = new FocusEvent('focusin', {
                                            view: wModal.ownerDocument.defaultView,
                                            bubbles: true,
                                            cancelable: false
                                        });
                                        wModal.dispatchEvent(focusInEvent);
                                        console.log('FocusIn event dispatched on modal');
                                        let wButton = await asyncAwaitVisibleElement('button#web-workflow');
                                        if (wButton){
                                            let focusInEvent = new FocusEvent('focusin', {
                                                view: wButton.ownerDocument.defaultView,
                                                bubbles: true,
                                                cancelable: false
                                            });
                                            wButton.dispatchEvent(focusInEvent);
                                            // use PointerEvent with target instead of MouseEvent
                                            let clickEvent = new PointerEvent('click', {
                                                view: wButton.ownerDocument.defaultView,
                                                bubbles: true,
                                                cancelable: false,
                                                pointerType: 'mouse',
                                                button: 0,
                                                buttons: 1,
                                                isPrimary: true,
                                                isTrusted: true,
                                                target: wButton
                                            });
                                            wButton.dispatchEvent(clickEvent);
                                            // let clickEvent = new MouseEvent('click', {
                                            //     view: wButton.ownerDocument.defaultView,
                                            //     bubbles: true,
                                            //     cancelable: false
                                            // });
                                            // wButton.dispatchEvent(clickEvent);
                                            console.log('Button#web-workflow event dispatched');
                                        } else {
                                            console.error('Button#web-workflow not found - click manually');
                                        }
                                    } else {
                                        console.error('Modal not found - click manually');
                                    }
                                }, 800);
                            }, 800);
                        } else {
                            console.log('Device already disconnected, new socket will be caught');
                        }
                    } else {
                        console.error('Connect button not found');
                    }

                    // check if Serial panel (id serial-page) is visible or click button#btn-mode-serial
                    const serialPanel = document.getElementById('serial-page');
                    if (serialPanel) {
                        if (serialPanel.style.display === 'none') {
                            console.log('Serial panel hidden, clicking button#btn-mode-serial');
                            setTimeout(() => {
                                document.getElementById('btn-mode-serial').click();
                            }, 1800);
                        } else {
                            console.log('Serial panel already visible');
                        }
                    } else {
                        console.error('Serial panel not found');
                    }

                    // check if Serial panel is connected
                }
                // console.error('CircuitPython.org support not implemented yet - try using webserial.io or the device web workflow page (at device IP or circuitpython.local)');
            } else {
                console.log("SerialFruit: Unsupported path:", window.location.pathname);
                // fallback to doing connectSerial or BLE ourselves
            }
        } else if (window.location.hostname.match(/code.circuitpython.org/i)) {
            // check if device connected state on page

            // check if Serial panel is visible

            // check if Serial panel is connected

            // send packet
            throw Error('Code.CircuitPython.Org support not implemented yet - try using webserial.io or the device web workflow page (at device IP or circuitpython.local)');
        } else if (window.location.host.match(/webserial.io/i)) {
            if (window.location.queryParams && !window.location.queryParams.vid) {
                console.error('WebSerial.io: No vid query parameter found - visit page first with a device selected');
                alert("WebSerial.io: No vid query parameter found - visit page first with a device selected, but don't click connect yet");
                return;
            }
            this._web_usb_serial = true;
            // check if device connected state on page
            if (document.querySelector('div#options').classList.contains('start')) {
                console.log('Device not connected, connecting...');
                ensureEverythingHooked();
                // document.querySelector('#options > fieldset > button').click();
            } else {
                if (!window.serialfruit || !window.serialfruit._trackedSockets) {
                    console.error('WebSerial.io: No tracked sockets found');
                    alert('WebSerial.io: No tracked sockets found, refresh the page and activate bookmarklet again before clicking connect');
                    return;
                }
            }
            // check if Serial panel is connected
        } else {
            console.error('SerialFruit: Unsupported host:', window.location.host);
            // fallback to doing connectSerial or BLE ourselves
        }
    }


    // Send packet via the serial connection
    async sendPacket(packet) {
        ensureAddressAndSocketAccess();
        if (!this._writer) await connectAnySerial();
        try {
            // if already Uint8Array, just send it
            if (packet instanceof Uint8Array) {
                await this._writer.write(packet);
                console.log("Successfully sent packet:", packet);
                return;
            } else if (packet instanceof BluefruitPacket) {
                await this._writer.write(packet.toBytes());
                console.log("Successfully sent packet:", packet.toBytes());
                return;
            } else {
                // assume it's a string
                const packetArray = new TextEncoder().encode(packet);
                await this._writer.write(packetArray);
                console.log("Successfully sent packet:", packetArray);
                return;
            }
            // const packetArray = packet.toBytes();
            // await writer.write(packetArray);
            // console.log("Successfully sent packet:", packetArray);
        } catch (error) {
            console.error("Failed to send packet: ", error);
        }
    }

    // Send color data
    async sendColor() {
        const color = document.getElementById("colorInput").value;
        const red = parseInt(color.slice(1, 3), 16);
        const green = parseInt(color.slice(3, 5), 16);
        const blue = parseInt(color.slice(5, 7), 16);
        const colorPacket = new ColorPacket(red, green, blue);
        await this.sendPacket(colorPacket);
    }

    async sendButton(button, pressed, eventType) {
        //todo: Add support for toggling button click type (mousedown, mouseup, versus click)
        switch ((""+eventType).startsWith('on') ? eventType.slice(2) : eventType) {
            case 'mousedown':
                console.log('ignoring mousedown event for now...')
                break;
            case 'mouseup':
                console.log('ignoring mouseup event for now...')
                break;
            case 'click':
            default:
                const buttonPacket = new ButtonPacket(button, pressed);
                await this.sendPacket(buttonPacket);
                break;
        }
    }

    // Send control command
    async sendControlCommand(command) {
        const controlCommandPacket = new ControlCommandPacket(command, 0x01); // Example value
        await this.sendPacket(controlCommandPacket);
    }

    // Send accelerometer data
    async sendAccelerometerData(event) {
        window.serialfruit.lastAccelerometerEventTimestamp =
            window.serialfruit.lastAccelerometerEventTimestamp || Date.now();
        if (Date.now() - window.serialfruit.lastAccelerometerEventTimestamp < 500) {
            const x = event.accelerationIncludingGravity.x || 0;
            const y = event.accelerationIncludingGravity.y || 0;
            const z = event.accelerationIncludingGravity.z || 0;
            console.log(event);
            // https://timvolodine.github.io/deviceorientation-test/
            // https://sensor-js.xyz/demo.html
            // https://developer.mozilla.org/en-US/docs/Web/API/DeviceMotionEventAcceleration
            // https://developer.mozilla.org/en-US/docs/Web/API/DeviceOrientationEvent/DeviceOrientationEvent
            const absoluteRotationX = event;
            debugger;
            console.log('Accelerometer data (x,y,z):', x,y,z)
            const accelerometerPacket = new AccelerometerPacket(x, y, z);
            await this.sendPacket(accelerometerPacket);
        } else {
            console.log('Skipping accelerometer data due to rate limiting');
        }
    }

    // Toggle accelerometer data capture
    async toggleAccelerometer(deviceOrBrowser = 'browser') {
        if (deviceOrBrowser === 'device') {
            if (window.DeviceMotionEvent) {
                if (accelerometerEnabled) {
                    window.removeEventListener('devicemotion', sendAccelerometerData);
                    console.log('Device motion event listener removed');
                } else {
                    window.addEventListener('devicemotion', sendAccelerometerData);
                    console.log('Device motion event listener added');
                }
                this._accelerometerEnabled = !this._accelerometerEnabled;
            } else {
                console.error('Device motion not supported on this device');
                alert('Device motion not supported on this device, possibly try messing with the browser settings');
            }
            return;
        } else if (deviceOrBrowser === 'browser') {
            // TODO: set up subscription to incoming messages, route to accelerometer visualisation or appropriate bridging transport (BLE/web-serial/WifiWebWorkflow/AdafruitIO-MQTT/AdafruitIO-REST)
            console.log('Toggling browser accelerometer data capture');
        }
    }

    // Send AT command
    async sendATCommand() {
        const command = document.getElementById("commandInput").value;
        const atCommandPacket = new ATCommandPacket(command);
        await this.sendPacket(atCommandPacket);
    }

    // Send DFU packet
    async sendDFUPacket() {
        const fileInput = document.getElementById("dfuFileInput");
        const file = fileInput.files[0];
        const reader = new FileReader();
        const self=this;
        reader.onload = function(e) {
            const arrayBuffer = e.target.result;
            const dfuPacket = new DFUPacket(new Uint8Array(arrayBuffer));
            window.serialfruit.sendPacket(dfuPacket);
        };
        reader.readAsArrayBuffer(file);
    }

    // Send Security packet
    async sendSecurityPacket() {
        const securityData = document.getElementById("securityInput").value;
        const payload = Array.from(new TextEncoder().encode(securityData));
        const securityPacket = new SecurityPacket(payload);
        await this.sendPacket(securityPacket);
    }

    // Send Read packet
    async sendReadPacket() {
        const readData = document.getElementById("readInput").value;
        const payload = Array.from(new TextEncoder().encode(readData));
        const readPacket = new ReadPacket(payload);
        await this.sendPacket(readPacket);
    }

    // Send Write packet
    async sendWritePacket() {
        const writeData = document.getElementById("writeInput").value;
        const payload = Array.from(new TextEncoder().encode(writeData));
        const writePacket = new WritePacket(payload);
        await this.sendPacket(writePacket);
    }

    // Send Notify packet
    async sendNotifyPacket() {
        const notifyData = document.getElementById("notifyInput").value;
        const payload = Array.from(new TextEncoder().encode(notifyData));
        const notifyPacket = new NotifyPacket(payload);
        await this.sendPacket(notifyPacket);
    }

    // Send Scan packet
    async sendScanPacket() {
        const scanPacket = new ScanPacket(new Uint8Array([]));
        await this.sendPacket(scanPacket);
    }

    // Send IO Pin packet
    async sendIOPinPacket() {
        const ioPinData = document.getElementById("ioPinInput").value;
        const payload = Array.from(new TextEncoder().encode(ioPinData));
        const ioPinPacket = new IOPinPacket(payload);
        await this.sendPacket(ioPinPacket);
    }

    // Send Neopixel packet
    async sendNeopixelPacket() {
        const neopixelData = document.getElementById("neopixelInput").value;
        const payload = Array.from(new TextEncoder().encode(neopixelData));
        const neopixelPacket = new NeopixelPacket(payload);
        await this.sendPacket(neopixelPacket);
    }

    // Send String packet
    async sendStringPacket() {
        const stringData = document.getElementById("stringInput").value;
        const stringPacket = new StringPacket(stringData);
        await this.sendPacket(stringPacket);
    }

    // Send Raw Bytes packet
    async sendRawBytes() {
        const rawBytesInput = document.getElementById("rawBytesInput").value;
        const rawBytes = rawBytesInput.split(',').map(byte => parseInt(byte.trim(), 10));
        const rawPacket = new RawPacket(rawBytes);
        await this.sendPacket(rawPacket);
    }

    // Send Raw String packet
    async sendRawString() {
        const rawStringInput = document.getElementById("rawStringInput").value;
        const stringPacket = new StringPacket(rawStringInput);
        await this.sendPacket(stringPacket);
    }

    // Send location
    async sendLocation() {
        const latitude = parseFloat(document.getElementById("latitudeInput").value);
        const longitude = parseFloat(document.getElementById("longitudeInput").value);
        const locationPacket = new LocationPacket(latitude, longitude);
        await this.sendPacket(locationPacket);
    }

    // Use current location
    async getCurrentLocation() {
        navigator.geolocation.getCurrentPosition((position) => {
            const latitude = position.coords.latitude;
            const longitude = position.coords.longitude;
            document.getElementById("latitudeInput").value = latitude;
            document.getElementById("longitudeInput").value = longitude;
            sendLocation();
        });
    }
}


window.serialfruit = window.serialfruit || new SerialFruit();
window.serialfruit.showScreen = showScreen;
// window.serialfruit.ensureAddressAndSocketAccess = ensureAddressAndSocketAccess;
window.serialfruit._trackedSockets = [];

setInterval(async ()=> await window.serialfruit.updateStatsTable(), 5000);