#python3

import socket

version = __version__ = "0.0.2 Released 12-12-2023"

_change_log = """
    Changelog since 0.0.1 released 4-7-2022
        - Initial Release
    Changelog since 0.0.2 released 12-12-2023
        - added incrementing sequence number 1-255 to send function
        
        
"""

# Global sequence number
seq = 0

def send(data: bytearray, uni: int | None = 1, ip: str | None = "2.255.255.255", port: int | None = 6454):
    """
    Sends artnet data to a device.

    Parameters:
    - data: array of ints 0-255 representing the Art-Net data
    - uni: universe of artnet device
    - ip: IP address of artnet device. Defaults to '2.255.255.255' if not provided
    - port: Port of artnet device. Defaults to 6454 if not provided
    """
    global seq  # Use the global sequence number

    # Increment seq and reset to 0 if it reaches 256
    seq = (seq + 1) % 256

    # Art-Net packet construction
    Phy = 0
    id = bytearray('Art-Net', 'utf8')
    null = b"\x00"
    opCode = (0x5000).to_bytes(2, byteorder="little")
    proVerHi = b"\x00"
    proVerLo = b"\x0e"
    
    Sequence = (seq).to_bytes(1, byteorder="big")
    Physical = (Phy).to_bytes(1, byteorder="little")
    SubUni = (uni).to_bytes(2, byteorder="little")
    length = len(data).to_bytes(2, byteorder="big")

    header = bytearray()
    header.extend(id)
    header.extend(null)
    header.extend(opCode)
    header.extend(proVerHi)
    header.extend(proVerLo)
    header.extend(Sequence)
    header.extend(Physical)
    header.extend(SubUni)
    header.extend(length)
    packet = bytearray()
    packet.extend(header)
    packet.extend(data)

    # Sending the packet
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(packet, (ip, port))
    sock.close()

    return packet

def getVersion():
    return "Artnetutil version: " + version

# Example usage
# send(bytearray([0, 255, 128]), 1, "2.0.0.1", 6454)
