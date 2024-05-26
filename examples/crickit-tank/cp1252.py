# Define the CP1252 to UTF-8 mapping
cp1252_to_utf8 = {
    0x00: b'\x00', 0x01: b'\x01', 0x02: b'\x02', 0x03: b'\x03', 0x04: b'\x04', 0x05: b'\x05', 0x06: b'\x06', 0x07: b'\x07',
    0x08: b'\x08', 0x09: b'\x09', 0x0A: b'\x0A', 0x0B: b'\x0B', 0x0C: b'\x0C', 0x0D: b'\x0D', 0x0E: b'\x0E', 0x0F: b'\x0F',
    0x10: b'\x10', 0x11: b'\x11', 0x12: b'\x12', 0x13: b'\x13', 0x14: b'\x14', 0x15: b'\x15', 0x16: b'\x16', 0x17: b'\x17',
    0x18: b'\x18', 0x19: b'\x19', 0x1A: b'\x1A', 0x1B: b'\x1B', 0x1C: b'\x1C', 0x1D: b'\x1D', 0x1E: b'\x1E', 0x1F: b'\x1F',
    0x20: b'\x20', 0x21: b'\x21', 0x22: b'\x22', 0x23: b'\x23', 0x24: b'\x24', 0x25: b'\x25', 0x26: b'\x26', 0x27: b'\x27',
    0x28: b'\x28', 0x29: b'\x29', 0x2A: b'\x2A', 0x2B: b'\x2B', 0x2C: b'\x2C', 0x2D: b'\x2D', 0x2E: b'\x2E', 0x2F: b'\x2F',
    0x30: b'\x30', 0x31: b'\x31', 0x32: b'\x32', 0x33: b'\x33', 0x34: b'\x34', 0x35: b'\x35', 0x36: b'\x36', 0x37: b'\x37',
    0x38: b'\x38', 0x39: b'\x39', 0x3A: b'\x3A', 0x3B: b'\x3B', 0x3C: b'\x3C', 0x3D: b'\x3D', 0x3E: b'\x3E', 0x3F: b'\x3F',
    0x40: b'\x40', 0x41: b'\x41', 0x42: b'\x42', 0x43: b'\x43', 0x44: b'\x44', 0x45: b'\x45', 0x46: b'\x46', 0x47: b'\x47',
    0x48: b'\x48', 0x49: b'\x49', 0x4A: b'\x4A', 0x4B: b'\x4B', 0x4C: b'\x4C', 0x4D: b'\x4D', 0x4E: b'\x4E', 0x4F: b'\x4F',
    0x50: b'\x50', 0x51: b'\x51', 0x52: b'\x52', 0x53: b'\x53', 0x54: b'\x54', 0x55: b'\x55', 0x56: b'\x56', 0x57: b'\x57',
    0x58: b'\x58', 0x59: b'\x59', 0x5A: b'\x5A', 0x5B: b'\x5B', 0x5C: b'\x5C', 0x5D: b'\x5D', 0x5E: b'\x5E', 0x5F: b'\x5F',
    0x60: b'\x60', 0x61: b'\x61', 0x62: b'\x62', 0x63: b'\x63', 0x64: b'\x64', 0x65: b'\x65', 0x66: b'\x66', 0x67: b'\x67',
    0x68: b'\x68', 0x69: b'\x69', 0x6A: b'\x6A', 0x6B: b'\x6B', 0x6C: b'\x6C', 0x6D: b'\x6D', 0x6E: b'\x6E', 0x6F: b'\x6F',
    0x70: b'\x70', 0x71: b'\x71', 0x72: b'\x72', 0x73: b'\x73', 0x74: b'\x74', 0x75: b'\x75', 0x76: b'\x76', 0x77: b'\x77',
    0x78: b'\x78', 0x79: b'\x79', 0x7A: b'\x7A', 0x7B: b'\x7B', 0x7C: b'\x7C', 0x7D: b'\x7D', 0x7E: b'\x7E', 0x7F: b'\x7F',
    0x80: b'\xC2\x80', 0x81: b'\xC2\x81', 0x82: b'\xE2\x80\x9A', 0x83: b'\xC6\x92', 0x84: b'\xE2\x80\x9E', 0x85: b'\xE2\x80\xA6', 0x86: b'\xE2\x80\xA0', 0x87: b'\xE2\x80\xA1',
    0x88: b'\xCB\x86', 0x89: b'\xE2\x80\xB0', 0x8A: b'\xC5\xA0', 0x8B: b'\xE2\x80\xB9', 0x8C: b'\xC5\x92', 0x8D: b'\xC2\x8D', 0x8E: b'\xC5\xBD', 0x8F: b'\xC2\x8F',
    0x90: b'\xC2\x90', 0x91: b'\xE2\x80\x98', 0x92: b'\xE2\x80\x99', 0x93: b'\xE2\x80\x9C', 0x94: b'\xE2\x80\x9D', 0x95: b'\xE2\x80\xA2', 0x96: b'\xE2\x80\x93', 0x97: b'\xE2\x80\x94',
    0x98: b'\xCB\x9C', 0x99: b'\xE2\x84\xA2', 0x9A: b'\xC5\xA1', 0x9B: b'\xE2\x80\xBA', 0x9C: b'\xC5\x93', 0x9D: b'\xC2\x9D', 0x9E: b'\xC5\xBE', 0x9F: b'\xC5\xB8',
    0xA0: b'\xC2\xA0', 0xA1: b'\xC2\xA1', 0xA2: b'\xC2\xA2', 0xA3: b'\xC2\xA3', 0xA4: b'\xC2\xA4', 0xA5: b'\xC2\xA5', 0xA6: b'\xC2\xA6', 0xA7: b'\xC2\xA7',
    0xA8: b'\xC2\xA8', 0xA9: b'\xC2\xA9', 0xAA: b'\xC2\xAA', 0xAB: b'\xC2\xAB', 0xAC: b'\xC2\xAC', 0xAD: b'\xC2\xAD', 0xAE: b'\xC2\xAE', 0xAF: b'\xC2\xAF',
    0xB0: b'\xC2\xB0', 0xB1: b'\xC2\xB1', 0xB2: b'\xC2\xB2', 0xB3: b'\xC2\xB3', 0xB4: b'\xC2\xB4', 0xB5: b'\xC2\xB5', 0xB6: b'\xC2\xB6', 0xB7: b'\xC2\xB7',
    0xB8: b'\xC2\xB8', 0xB9: b'\xC2\xB9', 0xBA: b'\xC2\xBA', 0xBB: b'\xC2\xBB', 0xBC: b'\xC2\xBC', 0xBD: b'\xC2\xBD', 0xBE: b'\xC2\xBE', 0xBF: b'\xC2\xBF',
    0xC0: b'\xC3\x80', 0xC1: b'\xC3\x81', 0xC2: b'\xC3\x82', 0xC3: b'\xC3\x83', 0xC4: b'\xC3\x84', 0xC5: b'\xC3\x85', 0xC6: b'\xC3\x86', 0xC7: b'\xC3\x87',
    0xC8: b'\xC3\x88', 0xC9: b'\xC3\x89', 0xCA: b'\xC3\x8A', 0xCB: b'\xC3\x8B', 0xCC: b'\xC3\x8C', 0xCD: b'\xC3\x8D', 0xCE: b'\xC3\x8E', 0xCF: b'\xC3\x8F',
    0xD0: b'\xC3\x90', 0xD1: b'\xC3\x91', 0xD2: b'\xC3\x92', 0xD3: b'\xC3\x93', 0xD4: b'\xC3\x94', 0xD5: b'\xC3\x95', 0xD6: b'\xC3\x96', 0xD7: b'\xC3\x97',
    0xD8: b'\xC3\x98', 0xD9: b'\xC3\x99', 0xDA: b'\xC3\x9A', 0xDB: b'\xC3\x9B', 0xDC: b'\xC3\x9C', 0xDD: b'\xC3\x9D', 0xDE: b'\xC3\x9E', 0xDF: b'\xC3\x9F',
    0xE0: b'\xC3\xA0', 0xE1: b'\xC3\xA1', 0xE2: b'\xC3\xA2', 0xE3: b'\xC3\xA3', 0xE4: b'\xC3\xA4', 0xE5: b'\xC3\xA5', 0xE6: b'\xC3\xA6', 0xE7: b'\xC3\xA7',
    0xE8: b'\xC3\xA8', 0xE9: b'\xC3\xA9', 0xEA: b'\xC3\xAA', 0xEB: b'\xC3\xAB', 0xEC: b'\xC3\xAC', 0xED: b'\xC3\xAD', 0xEE: b'\xC3\xAE', 0xEF: b'\xC3\xAF',
    0xF0: b'\xC3\xB0', 0xF1: b'\xC3\xB1', 0xF2: b'\xC3\xB2', 0xF3: b'\xC3\xB3', 0xF4: b'\xC3\xB4', 0xF5: b'\xC3\xB5', 0xF6: b'\xC3\xB6', 0xF7: b'\xC3\xB7',
    0xF8: b'\xC3\xB8', 0xF9: b'\xC3\xB9', 0xFA: b'\xC3\xBA', 0xFB: b'\xC3\xBB', 0xFC: b'\xC3\xBC', 0xFD: b'\xC3\xBD', 0xFE: b'\xC3\xBE', 0xFF: b'\xC3\xBF',
}

# Reverse the mapping to go from UTF-8 bytes to CP1252 decimal values
utf8_to_cp1252 = {v: k for k, v in cp1252_to_utf8.items()}

# # Input string assumed to be in UTF-8 encoding
# utf8_string = "Hello›"  # Example string including the character ›

# # Convert the string to bytes
# utf8_bytes = utf8_string.encode('utf-8')

# # Function to convert UTF-8 bytes to their corresponding CP1252 decimal values
# def utf8_to_cp1252_decimal(utf8_bytes):
#     i = 0
#     cp1252_values = []
#     while i < len(utf8_bytes):
#         for length in range(1, 4):  # UTF-8 characters can be 1 to 4 bytes long
#             utf8_char = utf8_bytes[i:i+length]
#             if utf8_char in utf8_to_cp1252:
#                 cp1252_values.append(utf8_to_cp1252[utf8_char])
#                 i += length
#                 break
#         else:
#             # If no valid CP1252 character is found, just increment by 1 (this should not normally happen for valid input)
#             i += 1
#     return cp1252_values

# # Get the CP1252 decimal values
# cp1252_values = utf8_to_cp1252_decimal(utf8_bytes)

# # Print each character and its corresponding CP1252 decimal value
# for i, char in enumerate(utf8_string):
#     print(f"Character: {char} => CP1252 Decimal Value: {cp1252_values[i]}")

def get_decimal_value_from_char(char=''):
    # Iterate through the string and look up each character's CP1252 decimal value
    decimal_value = None
    if char:
        char_value = char.encode('utf-8')
        decimal_value = utf8_to_cp1252.get(char_value, None)
        if decimal_value is not None:
            print(f"Character: {char} => CP1252 Decimal Value: {decimal_value}")
        else:
            print(f"Character: {char} => Not found in CP1252 mapping")
    return decimal_value

def get_decimals_from_string(input_string=''):
    # Convert the string to a list of decimal values
    decimal_values = []
    if input_string:
        for char in input_string:
            decimal_value = get_decimal_value_from_char(char)
            if decimal_value is not None:
                decimal_values.append(decimal_value)
    return decimal_values

# # Define a mapping from CP1252 characters to their decimal values
# cp1252_to_decimal = {
#     '\x00': 0, '\x01': 1, '\x02': 2, '\x03': 3, '\x04': 4, '\x05': 5, '\x06': 6, '\x07': 7,
#     '\x08': 8, '\x09': 9, '\x0A': 10, '\x0B': 11, '\x0C': 12, '\x0D': 13, '\x0E': 14, '\x0F': 15,
#     '\x10': 16, '\x11': 17, '\x12': 18, '\x13': 19, '\x14': 20, '\x15': 21, '\x16': 22, '\x17': 23,
#     '\x18': 24, '\x19': 25, '\x1A': 26, '\x1B': 27, '\x1C': 28, '\x1D': 29, '\x1E': 30, '\x1F': 31,
#     '\x20': 32, '\x21': 33, '\x22': 34, '\x23': 35, '\x24': 36, '\x25': 37, '\x26': 38, '\x27': 39,
#     '\x28': 40, '\x29': 41, '\x2A': 42, '\x2B': 43, '\x2C': 44, '\x2D': 45, '\x2E': 46, '\x2F': 47,
#     '\x30': 48, '\x31': 49, '\x32': 50, '\x33': 51, '\x34': 52, '\x35': 53, '\x36': 54, '\x37': 55,
#     '\x38': 56, '\x39': 57, '\x3A': 58, '\x3B': 59, '\x3C': 60, '\x3D': 61, '\x3E': 62, '\x3F': 63,
#     '\x40': 64, '\x41': 65, '\x42': 66, '\x43': 67, '\x44': 68, '\x45': 69, '\x46': 70, '\x47': 71,
#     '\x48': 72, '\x49': 73, '\x4A': 74, '\x4B': 75, '\x4C': 76, '\x4D': 77, '\x4E': 78, '\x4F': 79,
#     '\x50': 80, '\x51': 81, '\x52': 82, '\x53': 83, '\x54': 84, '\x55': 85, '\x56': 86, '\x57': 87,
#     '\x58': 88, '\x59': 89, '\x5A': 90, '\x5B': 91, '\x5C': 92, '\x5D': 93, '\x5E': 94, '\x5F': 95,
#     '\x60': 96, '\x61': 97, '\x62': 98, '\x63': 99, '\x64': 100, '\x65': 101, '\x66': 102, '\x67': 103,
#     '\x68': 104, '\x69': 105, '\x6A': 106, '\x6B': 107, '\x6C': 108, '\x6D': 109, '\x6E': 110, '\x6F': 111,
#     '\x70': 112, '\x71': 113, '\x72': 114, '\x73': 115, '\x74': 116, '\x75': 117, '\x76': 118, '\x77': 119,
#     '\x78': 120, '\x79': 121, '\x7A': 122, '\x7B': 123, '\x7C': 124, '\x7D': 125, '\x7E': 126, '\x7F': 127,
#     '\x80': 128, '\x81': 129, '\x82': 130, '\x83': 131, '\x84': 132, '\x85': 133, '\x86': 134, '\x87': 135,
#     '\x88': 136, '\x89': 137, '\x8A': 138, '\x8B': 139, '\x8C': 140, '\x8D': 141, '\x8E': 142, '\x8F': 143,
#     '\x90': 144, '\x91': 145, '\x92': 146, '\x93': 147, '\x94': 148, '\x95': 149, '\x96': 150, '\x97': 151,
#     '\x98': 152, '\x99': 153, '\x9A': 154, '\x9B': 155, '\x9C': 156, '\x9D': 157, '\x9E': 158, '\x9F': 159,
#     '\xA0': 160, '\xA1': 161, '\xA2': 162, '\xA3': 163, '\xA4': 164, '\xA5': 165, '\xA6': 166, '\xA7': 167,
#     '\xA8': 168, '\xA9': 169, '\xAA': 170, '\xAB': 171, '\xAC': 172, '\xAD': 173, '\xAE': 174, '\xAF': 175,
#     '\xB0': 176, '\xB1': 177, '\xB2': 178, '\xB3': 179, '\xB4': 180, '\xB5': 181, '\xB6': 182, '\xB7': 183,
#     '\xB8': 184, '\xB9': 185, '\xBA': 186, '\xBB': 187, '\xBC': 188, '\xBD': 189, '\xBE': 190, '\xBF': 191,
#     '\xC0': 192, '\xC1': 193, '\xC2': 194, '\xC3': 195, '\xC4': 196, '\xC5': 197, '\xC6': 198, '\xC7': 199,
#     '\xC8': 200, '\xC9': 201, '\xCA': 202, '\xCB': 203, '\xCC': 204, '\xCD': 205, '\xCE': 206, '\xCF': 207,
#     '\xD0': 208, '\xD1': 209, '\xD2': 210, '\xD3': 211, '\xD4': 212, '\xD5': 213, '\xD6': 214, '\xD7': 215,
#     '\xD8': 216, '\xD9': 217, '\xDA': 218, '\xDB': 219, '\xDC': 220, '\xDD': 221, '\xDE': 222, '\xDF': 223,
#     '\xE0': 224, '\xE1': 225, '\xE2': 226, '\xE3': 227, '\xE4': 228, '\xE5': 229, '\xE6': 230, '\xE7': 231,
#     '\xE8': 232, '\xE9': 233, '\xEA': 234, '\xEB': 235, '\xEC': 236, '\xED': 237, '\xEE': 238, '\xEF': 239,
#     '\xF0': 240, '\xF1': 241, '\xF2': 242, '\xF3': 243, '\xF4': 244, '\xF5': 245, '\xF6': 246, '\xF7': 247,
#     '\xF8': 248, '\xF9': 249, '\xFA': 250, '\xFB': 251, '\xFC': 252, '\xFD': 253, '\xFE': 254, '\xFF': 255,
# }

# def get_decimal_value_from_char(char=''):
#     # Iterate through the string and look up each character's CP1252 decimal value
#     decimal_value = None
#     if char:
#         decimal_value = cp1252_to_decimal.get(char, None)
#         if decimal_value is not None:
#             print(f"Character: {char} => CP1252 Decimal Value: {decimal_value}")
#         else:
#             print(f"Character: {char} => Not found in CP1252 mapping")
#     return decimal_value

# def get_decimals_from_string(input_string=''):
#     # Convert the string to a list of decimal values
#     decimal_values = []
#     if input_string:
#         for char in input_string:
#             decimal_value = get_decimal_value_from_char(char)
#             if decimal_value is not None:
#                 decimal_values.append(decimal_value)
#     return decimal_values
