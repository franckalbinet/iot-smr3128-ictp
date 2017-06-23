# CRC
def crc(incoming):
    # convert to bytearray
    hex_data = incoming.decode("hex")
    msg = bytearray(hex_data)
    check = 0
    for i in msg:
        check = _addToCRC(i, check)
    return hex(check)

def _addToCRC(b, crc):
    if (b < 0):
        b += 256
    for i in range(8):
        odd = ((b^crc) & 1) == 1
        crc >>= 1
        b >>= 1
        if (odd):
            crc ^= 0x8C # this means crc ^= 140
    return crc
