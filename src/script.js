document.addEventListener("DOMContentLoaded", () => {
    showScreen('main-menu');
});

function showScreen(screenId) {
    document.querySelectorAll('.screen').forEach(screen => {
        screen.style.display = 'none';
    });
    document.getElementById(screenId).style.display = 'flex';
}

// Base class for Bluefruit packets
class BluefruitPacket {
    constructor(packetType, payload) {
        this.packetType = packetType;
        this.payload = payload;
        this.packetLen = payload.length + 2; // Packet type + Length + Payload + Checksum
    }

    // Calculate checksum using two's complement
    calculateChecksum() {
        let sum = this.packetType + this.packetLen;
        for (const byte of this.payload) {
            sum += byte;
        }
        return (~sum + 1) & 0xFF; // Two's complement
    }

    // Convert packet to Uint8Array
    toArray() {
        const packetArray = [this.packetType, this.packetLen, ...this.payload];
        const checksum = this.calculateChecksum();
        packetArray.push(checksum);
        return new Uint8Array(packetArray);
    }
}

// Packet types
const PacketType = {
    CONNECTED: 0x01,
    DISCONNECTED: 0x02,
    ATCOMMAND: 0x0A,
    DFU: 0x0B,
    SECURITY: 0x0C,
    CONTROL: 0x0D,
    COLOR: 0x0E,
    LOCATION: 0x0F,
    TEMPERATURE: 0x10,
    BUTTON: 0x11,
    ACCELEROMETER: 0x12,
    GYROSCOPE: 0x13,
    QUATERNION: 0x14,
    MAGNETOMETER: 0x15,
    READ: 0x16,
    WRITE: 0x17,
    NOTIFY: 0x18,
    SCAN: 0x19,
    IOPIN: 0x1A,
    NEOPIXEL: 0x1B,
    STRING: 0x1C,
    RAW: 0x1D
};

// AT Command Packet class
class ATCommandPacket extends BluefruitPacket {
    constructor(commandString) {
        const payload = Array.from(new TextEncoder().encode(commandString));
        super(PacketType.ATCOMMAND, payload);
    }
}

// Control Command Packet class
class ControlCommandPacket extends BluefruitPacket {
    constructor(command, value) {
        const payload = [command, value];
        super(PacketType.CONTROL, payload);
    }
}

// Color Packet class
class ColorPacket extends BluefruitPacket {
    constructor(red, green, blue) {
        const payload = [red, green, blue];
        super(PacketType.COLOR, payload);
    }
}

// Location Packet class
class LocationPacket extends BluefruitPacket {
    constructor(latitude, longitude) {
        const payload = new DataView(new ArrayBuffer(8));
        payload.setFloat32(0, latitude, true);
        payload.setFloat32(4, longitude, true);
        super(PacketType.LOCATION, new Uint8Array(payload.buffer));
    }
}

// Temperature Packet class
class TemperaturePacket extends BluefruitPacket {
    constructor(temperature) {
        const payload = new DataView(new ArrayBuffer(4));
        payload.setFloat32(0, temperature, true);
        super(PacketType.TEMPERATURE, new Uint8Array(payload.buffer));
    }
}

// Button Packet class
class ButtonPacket extends BluefruitPacket {
    constructor(button, state) {
        const payload = [button, state];
        super(PacketType.BUTTON, payload);
    }
}

// Accelerometer Packet class
class AccelerometerPacket extends BluefruitPacket {
    constructor(x, y, z) {
        const payload = new DataView(new ArrayBuffer(12));
        payload.setFloat32(0, x, true);
        payload.setFloat32(4, y, true);
        payload.setFloat32(8, z, true);
        super(PacketType.ACCELEROMETER, new Uint8Array(payload.buffer));
    }
}

// Gyroscope Packet class
class GyroscopePacket extends BluefruitPacket {
    constructor(x, y, z) {
        const payload = new DataView(new ArrayBuffer(12));
        payload.setFloat32(0, x, true);
        payload.setFloat32(4, y, true);
        payload.setFloat32(8, z, true);
        super(PacketType.GYROSCOPE, new Uint8Array(payload.buffer));
    }
}

// Quaternion Packet class
class QuaternionPacket extends BluefruitPacket {
    constructor(w, x, y, z) {
        const payload = new DataView(new ArrayBuffer(16));
        payload.setFloat32(0, w, true);
        payload.setFloat32(4, x, true);
        payload.setFloat32(8, y, true);
        payload.setFloat32(12, z, true);
        super(PacketType.QUATERNION, new Uint8Array(payload.buffer));
    }
}

// Magnetometer Packet class
class MagnetometerPacket extends BluefruitPacket {
    constructor(x, y, z) {
        const payload = new DataView(new ArrayBuffer(12));
        payload.setFloat32(0, x, true);
        payload.setFloat32(4, y, true);
        payload.setFloat32(8, z, true);
        super(PacketType.MAGNETOMETER, new Uint8Array(payload.buffer));
    }
}

// DFU Packet class
class DFUPacket extends BluefruitPacket {
    constructor(payload) {
        super(PacketType.DFU, payload);
    }
}

// Security Packet class
class SecurityPacket extends BluefruitPacket {
    constructor(payload) {
        super(PacketType.SECURITY, payload);
    }
}

// Read Packet class
class ReadPacket extends BluefruitPacket {
    constructor(payload) {
        super(PacketType.READ, payload);
    }
}

// Write Packet class
class WritePacket extends BluefruitPacket {
    constructor(payload) {
        super(PacketType.WRITE, payload);
    }
}

// Notify Packet class
class NotifyPacket extends BluefruitPacket {
    constructor(payload) {
        super(PacketType.NOTIFY, payload);
    }
}

// Scan Packet class
class ScanPacket extends BluefruitPacket {
    constructor(payload) {
        super(PacketType.SCAN, payload);
    }
}

// IO Pin Packet class
class IOPinPacket extends BluefruitPacket {
    constructor(payload) {
        super(PacketType.IOPIN, payload);
    }
}

// Neopixel Packet class
class NeopixelPacket extends BluefruitPacket {
    constructor(payload) {
        super(PacketType.NEOPIXEL, payload);
    }
}

// String Packet class
class StringPacket extends BluefruitPacket {
    constructor(payload) {
        const payloadArray = Array.from(new TextEncoder().encode(payload));
        super(PacketType.STRING, payloadArray);
    }
}

// Raw Data Packet class
class RawPacket extends BluefruitPacket {
    constructor(payload) {
        super(PacketType.RAW, payload);
    }
}

// Initialize global variables for serial port and writer
let port, writer, webworkflow_serial, ble_serial, accelerometerEnabled = false;

// Connect to serial or web serial (or eventually BLE serial)
async function connectAnySerial() {
    if (writer) return;
    if (webworkflow_serial) {
        //setup textencoder for writer to websocket
        ws = getTrackedSockets().find((ws) => ws.url === 'ws://' + window.location.host + '/ws/serial' && ws.readyState === 1);
        if (ws) {
            writer = {
                write: async (data) => {
                    console.log('Sending packet:', data);
                    ws.send(new TextEncoder().encode(data));
                    console.log('Packet sent:', data);
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
async function connectSerial() {
    try {
        port = await navigator.serial.requestPort();
        await port.open({ baudRate: 115200 });
        writer = port.writable.getWriter();
        console.log("Connected to serial port", port);
    } catch (error) {
        console.error("Failed to connect to serial port: ", error);
    }
}

// Ensure access to serial port and writer
async function ensureAddressAndSocketAccess() {
    if (window.location.host.match(/^((192.168)|(cpy-))/i)) {
        webworkflow_serial = true;
        if (window.location.pathname.endsWith('cp/serial')) {
            console.log('Sending packet:', packet);
            debugger;
            ws = ws || new WebSocket('ws://' + window.location.host + '/ws/serial');
            ws.send(packet.toArray());
            console.log('Packet sent:', packet.toArray());
            return;
        } else if (window.location.pathname == "/code/") {
            // monkey patch websockets to allow reuse
            if (window.getTrackedSockets) {
                console.log('WebSocket tracking already enabled.');
                debugger;
                if (window.getTrackedSockets().length > 1) {
                    console.log('Cleaning up old closed connections');
                    window._trackedSockets = window._trackedSockets.filter((x) => x?.readyState !== 3);
                    console.log('Existing Closed WebSocket connections cleaned up.');
                    if (window.getTrackedSockets().filter(ws => ws.readyState === 1).length > 1) {
                        console.log('Unexpected MULTIPLE Open Existing WebSocket connections:', window.getTrackedSockets());
                        for (const ws of window.getTrackedSockets().filter((x)=>x?.readyState===1)) {
                            console.log('Closing WebSocket:', ws);
                            ws.close();
                        }
                        console.log('Existing WebSocket connections forceably closed.');
                    }
                    return;
                } else if (window.getTrackedSockets().length === 1) {
                    console.log('Existing WebSocket connection found:', window.getTrackedSockets()[0]);
                    return;
                }
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
                
                window.getTrackedSockets = function () {
                    return trackedSockets;
                };
                window._trackedSockets = trackedSockets;
                
                console.log('WebSocket tracking enabled.');
            }
                
            // check if device connected state on page and reconnect
            let connectButton = document.querySelector('button.btn-connect');
            connectButton = Object.prototype.hasOwnProperty("length", connectButton) && connectButton.length > 1 ? connectButton[0] : connectButton;
            if (connectButton) {
                if (connectButton.textContent === 'Disconnect') {
                    console.log('Device already connected, disconnecting first');
                    connectButton.click();
                    setTimeout(() => {
                        console.log('Reconnecting device');
                        let cButton = document.querySelector('button.btn-connect');
                        cButton = Object.prototype.hasOwnProperty("length", cButton) && cButton.length > 1 ? cButton[0] : cButton;
                        cButton.click();
                        setTimeout(() => {
                            //button#web-workflow click
                            console.log('Triggering button#web-workflow with event');
                            // first trigger focusIn on <div class="popup-modal shadow prompt closable is--visible" 
                            // and on button#web-workflow
                            let wModal = document.querySelector('div.popup-modal.is--visible[data-popup-modal="connection-type"]');
                            if (wModal){
                                let focusInEvent = new FocusEvent('focusin', {
                                    view: wModal.ownerDocument.defaultView,
                                    bubbles: true,
                                    cancelable: false
                                });
                                wModal.dispatchEvent(focusInEvent);
                                console.log('FocusIn event dispatched on modal');
                                debugger;
                                let wButton = document.querySelector('button#web-workflow');
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

            // send packet
            console.error('CircuitPython.org support not implemented yet - try using webserial.io or the device web workflow page (at device IP or circuitpython.local)');
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
        // check if device connected state on page

        // check if Serial panel is visible

        // check if Serial panel is connected

        // send packet
        throw Error('WebSerial.io support not implemented yet - try using the device web workflow page (at device IP or circuitpython.local)');
    } else {
        console.error('SerialFruit: Unsupported host:', window.location.host);
        // fallback to doing connectSerial or BLE ourselves
    }
}


// Send packet via the serial connection
async function sendPacket(packet) {
    ensureAddressAndSocketAccess();
    if (!writer) await connectSerial();
    try {
        const packetArray = packet.toArray();
        await writer.write(packetArray);
        console.log("Packet sent:", packetArray);
    } catch (error) {
        console.error("Failed to send packet: ", error);
    }
}

// Send color data
function sendColor() {
    const color = document.getElementById("colorInput").value;
    const red = parseInt(color.slice(1, 3), 16);
    const green = parseInt(color.slice(3, 5), 16);
    const blue = parseInt(color.slice(5, 7), 16);
    const colorPacket = new ColorPacket(red, green, blue);
    sendPacket(colorPacket);
}

// Send control command
function sendControlCommand(command) {
    const controlCommandPacket = new ControlCommandPacket(command, 0x01); // Example value
    sendPacket(controlCommandPacket);
}

// Send accelerometer data
function sendAccelerometerData(event) {
    const x = event.accelerationIncludingGravity.x || 0;
    const y = event.accelerationIncludingGravity.y || 0;
    const z = event.accelerationIncludingGravity.z || 0;
    const accelerometerPacket = new AccelerometerPacket(x, y, z);
    sendPacket(accelerometerPacket);
}

// Toggle accelerometer data capture
function toggleAccelerometer() {
    if (accelerometerEnabled) {
        window.removeEventListener('devicemotion', sendAccelerometerData);
    } else {
        window.addEventListener('devicemotion', sendAccelerometerData);
    }
    accelerometerEnabled = !accelerometerEnabled;
}

// Send AT command
function sendATCommand() {
    const command = document.getElementById("commandInput").value;
    const atCommandPacket = new ATCommandPacket(command);
    sendPacket(atCommandPacket);
}

// Send DFU packet
function sendDFUPacket() {
    const fileInput = document.getElementById("dfuFileInput");
    const file = fileInput.files[0];
    const reader = new FileReader();
    reader.onload = function(e) {
        const arrayBuffer = e.target.result;
        const dfuPacket = new DFUPacket(new Uint8Array(arrayBuffer));
        sendPacket(dfuPacket);
    };
    reader.readAsArrayBuffer(file);
}

// Send Security packet
function sendSecurityPacket() {
    const securityData = document.getElementById("securityInput").value;
    const payload = Array.from(new TextEncoder().encode(securityData));
    const securityPacket = new SecurityPacket(payload);
    sendPacket(securityPacket);
}

// Send Read packet
function sendReadPacket() {
    const readData = document.getElementById("readInput").value;
    const payload = Array.from(new TextEncoder().encode(readData));
    const readPacket = new ReadPacket(payload);
    sendPacket(readPacket);
}

// Send Write packet
function sendWritePacket() {
    const writeData = document.getElementById("writeInput").value;
    const payload = Array.from(new TextEncoder().encode(writeData));
    const writePacket = new WritePacket(payload);
    sendPacket(writePacket);
}

// Send Notify packet
function sendNotifyPacket() {
    const notifyData = document.getElementById("notifyInput").value;
    const payload = Array.from(new TextEncoder().encode(notifyData));
    const notifyPacket = new NotifyPacket(payload);
    sendPacket(notifyPacket);
}

// Send Scan packet
function sendScanPacket() {
    const scanPacket = new ScanPacket(new Uint8Array([]));
    sendPacket(scanPacket);
}

// Send IO Pin packet
function sendIOPinPacket() {
    const ioPinData = document.getElementById("ioPinInput").value;
    const payload = Array.from(new TextEncoder().encode(ioPinData));
    const ioPinPacket = new IOPinPacket(payload);
    sendPacket(ioPinPacket);
}

// Send Neopixel packet
function sendNeopixelPacket() {
    const neopixelData = document.getElementById("neopixelInput").value;
    const payload = Array.from(new TextEncoder().encode(neopixelData));
    const neopixelPacket = new NeopixelPacket(payload);
    sendPacket(neopixelPacket);
}

// Send String packet
function sendStringPacket() {
    const stringData = document.getElementById("stringInput").value;
    const stringPacket = new StringPacket(stringData);
    sendPacket(stringPacket);
}

// Send Raw Bytes packet
function sendRawBytes() {
    const rawBytesInput = document.getElementById("rawBytesInput").value;
    const rawBytes = rawBytesInput.split(',').map(byte => parseInt(byte.trim(), 10));
    const rawPacket = new RawPacket(rawBytes);
    sendPacket(rawPacket);
}

// Send Raw String packet
function sendRawString() {
    const rawStringInput = document.getElementById("rawStringInput").value;
    const stringPacket = new StringPacket(rawStringInput);
    sendPacket(stringPacket);
}

// Send location
function sendLocation() {
    const latitude = parseFloat(document.getElementById("latitudeInput").value);
    const longitude = parseFloat(document.getElementById("longitudeInput").value);
    const locationPacket = new LocationPacket(latitude, longitude);
    sendPacket(locationPacket);
}

// Use current location
function getCurrentLocation() {
    navigator.geolocation.getCurrentPosition((position) => {
        const latitude = position.coords.latitude;
        const longitude = position.coords.longitude;
        document.getElementById("latitudeInput").value = latitude;
        document.getElementById("longitudeInput").value = longitude;
        sendLocation();
    });
}

window.serialfruit = window.serialfruit || {};
window.serialfruit.showScreen = showScreen;
window.serialfruit.ensureAddressAndSocketAccess = ensureAddressAndSocketAccess;
window.serialfruit._trackedSockets = window._trackedSockets;