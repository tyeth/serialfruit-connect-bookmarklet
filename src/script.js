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

// Initialize global variables for serial port and writer
let port, writer, accelerometerEnabled = false;

// Connect to the serial port
async function connectSerial() {
    try {
        port = await navigator.serial.requestPort();
        await port.open({ baudRate: 9600 });
        writer = port.writable.getWriter();
    } catch (error) {
        console.error("Failed to connect to serial port: ", error);
    }
}

// Send packet via the serial connection
async function sendPacket(packet) {
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
