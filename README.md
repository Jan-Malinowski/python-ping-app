# Python Ping App using Socket library

A lightweight Python implementation of the `ping` utility. It uses raw sockets to build ICMP packets from scratch and handles network responses manually.

## How it works
The script bypasses high-level networking libraries and interacts directly with the network stack:
1. **Socket Creation**: Opens a `socket.SOCK_RAW` with the ICMP protocol.
2. **Packet Assembly**: Uses Python's `struct` module to pack the ICMP header (Type, Code, ID, Sequence, Checksum).
3. **Checksum Calculation**: Implements the 16-bit 1's complement sum of the entire packet.
4. **Listener**: Monitors the socket for incoming data, strips the IP header (for IPv4), and validates the ICMP ID to match the request.

---

### Command Line Arguments
* `-c <count>`: Number of packets to send (default: 5).
* `-t <ttl>`: Set the Time To Live (TTL) value.
* `-l`: Stop execution after the first successful response.
* `-h`: Show help message.

### Examples:
**Note:** Raw sockets require **root** or **administrator** permissions to create and send packets.

Custom settings (10 packets, TTL 64):
`sudo python3 ping.py -c 10 -t 64 127.0.0.1`

## Future improvements
* **Domain Resolution**: Automatically resolves hostnames to IP addresses.
* **IPv6 Support**: Pinging IPv6 addresses.
* **Response Handling**: Interprets and displays detailed reply stats (bytes, response time, and TTL).
* **New_flags**: Support for more advanced flags.
