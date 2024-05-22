import csv
import struct

# Define the range for typable ASCII characters (32 to 126)
typable_ascii_range = range(32, 127)

def calculate_checksum(packet):
    return ~sum(packet) & 0xFF

def construct_color_packet(packet_type, rgb_values):
    # Construct the packet
    header = packet_type.encode()
    payload = struct.pack('BBB', *rgb_values)
    packet = header + payload
    # Calculate the checksum
    checksum = calculate_checksum(packet)
    # Append checksum to the packet
    full_packet = packet + struct.pack('B', checksum)
    return full_packet

def is_typable_ascii(packet):
    return all(32 <= byte <= 126 for byte in packet)

# Generate all possible RGB combinations
typable_packets = []
for r in range(256):
    for g in range(256):
        for b in range(256):
            full_packet = construct_color_packet('!C', (r, g, b))
            if is_typable_ascii(full_packet):
                ascii_packet = ''.join(chr(byte) for byte in full_packet)
                typable_packets.append((ascii_packet, r, g, b))

# Write to CSV
csv_file_path = 'typable_color_packets.csv'
with open(csv_file_path, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile, quotechar="'", quoting=csv.QUOTE_ALL)
    csvwriter.writerow(['Packet', 'R', 'G', 'B'])  # Write header
    for packet in typable_packets:
        csvwriter.writerow(packet)

print(f"CSV file generated at: {csv_file_path}")
