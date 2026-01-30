# TCP Messaging Toolkit

A collection of network programming assignments demonstrating socket programming, protocol buffers, encryption, and packet analysis in Python.

---

## Project Structure

```
network2021-master/
├── mp2/                    # Echo Server
├── mp3/                    # Basic Instant Messaging
├── mp4/                    # Encrypted Instant Messaging
└── mp5/                    # PCAP Network Traffic Analysis
```

---

## Requirements

- **Python 3.7+**
- **Dependencies:**

```bash
pip install pycryptodome protobuf scapy numpy pandas
```

---

## MP2: Echo Server

A TCP echo server that listens on a specified port and echoes back any data received from clients.

### Features
- Echoes received data back to the client
- Optional **reverse mode** — returns data in reverse order
- Handles multiple sequential client connections

### Usage

```bash
# Start the echo server on port 8080
python mp2/echo_server.py -p 8080

# Start with reverse mode enabled
python mp2/echo_server.py -p 8080 -r
```

### Arguments
| Flag | Description |
|------|-------------|
| `-p`, `--port` | Port to listen on (required) |
| `-r`, `--reverse` | Enable reverse echo mode |

---

## MP3: Basic Instant Messaging

A multi-client chat application using TCP sockets and Protocol Buffers for message serialization.

### Architecture
- **Server** (`basicIMserver.py`): Accepts multiple client connections and broadcasts messages to all connected clients
- **Client** (`basicIMclient.py`): Connects to the server, sends and receives messages with a nickname

### Protocol
Messages are serialized using Protocol Buffers with the following schema:

```protobuf
message Message {
    required string nickname = 1;
    required string message = 2;
}
```

### Usage

**Start the server:**
```bash
python mp3/basicIMserver.py
```
> Server listens on port **9999** by default

**Connect clients:**
```bash
python mp3/basicIMclient.py -s <server_ip> -n <nickname>

# Example
python mp3/basicIMclient.py -s localhost -n Alice
python mp3/basicIMclient.py -s localhost -n Bob
```

### Client Commands
- Type a message and press Enter to send
- Type `exit` to disconnect

### Examples
The `mp3/examples/` folder contains helpful reference code:
- `example_argparse.py` — Demonstrates command-line argument parsing
- `example_select.py` — Demonstrates using `select()` for I/O multiplexing

---

## MP4: Encrypted Instant Messaging

An encrypted version of the IM system using **AES-256-CBC** for confidentiality and **HMAC-SHA256** for message authentication.

### Security Features
- **Confidentiality**: AES-256-CBC encryption with random IVs
- **Integrity**: HMAC-SHA256 message authentication codes
- **Key Derivation**: SHA-256 hashing for key normalization

### Protocol Structure

```
┌─────────────────────────────────┐
│       EncryptedPackage          │
├─────────────────────────────────┤
│  iv (16 bytes)                  │
│  encryptedMessage ──────────────┼──┐
└─────────────────────────────────┘  │
                                     ▼
                    ┌─────────────────────────────────┐
                    │      PlaintextAndMAC            │
                    ├─────────────────────────────────┤
                    │  paddedPlaintext ───────────────┼──┐
                    │  mac (32 bytes HMAC-SHA256)     │  │
                    └─────────────────────────────────┘  │
                                                         ▼
                                        ┌─────────────────────────────────┐
                                        │             IM                  │
                                        ├─────────────────────────────────┤
                                        │  nickname                       │
                                        │  message                        │
                                        └─────────────────────────────────┘
```

### Usage

**Start the server:**
```bash
python mp4/encryptedIMserver.py -p 9999
```

**Connect clients (all clients must use the same keys):**
```bash
python mp4/encryptedIMclient.py -s <server_ip> -n <nickname> -c <conf_key> -a <auth_key> -p <port>

# Example
python mp4/encryptedIMclient.py -s localhost -n Alice -c "secretkey123" -a "authkey456" -p 9999
python mp4/encryptedIMclient.py -s localhost -n Bob -c "secretkey123" -a "authkey456" -p 9999
```

### Arguments
| Flag | Description |
|------|-------------|
| `-s`, `--servername` | Server IP or hostname (required) |
| `-n`, `--nickname` | User's display name (required) |
| `-c`, `--confidentiality-key` | AES encryption key (required) |
| `-a`, `--authenticity-key` | HMAC authentication key (required) |
| `-p`, `--port` | Server port (required) |

### Demo Script
`mp4/demo.py` provides a walkthrough of the encryption/packaging process for educational purposes.

---

## MP5: PCAP Network Traffic Analysis

A tool for analyzing network packet captures (PCAP files) using Scapy, with statistical analysis of traffic patterns.

### Features
- Parse and analyze PCAP files
- Distinguish between incoming and outgoing traffic (based on `192.168.x.x` source IPs)
- Calculate packet counts, byte totals, and timing statistics
- Export analysis results to CSV

### Usage

**Analyze a single PCAP file:**
```bash
python mp5/read_pcap.py -f google.pcap
```

**Analyze all PCAP files in the `pcap_files/` directory:**
```bash
python mp5/read_pcap.py
```

### Output
- Individual file analysis: `<filename>_out.csv` with per-packet details
- Batch analysis: `out.csv` with aggregate statistics

### Statistics Computed
| Metric | Description |
|--------|-------------|
| `packets_in` / `packets_out` | Total packet counts |
| `bytes_in` / `bytes_out` | Total byte counts |
| `time_in_mean` / `time_out_mean` | Mean inter-arrival time |
| `time_in_median` / `time_out_median` | Median inter-arrival time |
| `time_in_std` / `time_out_std` | Standard deviation of inter-arrival times |

### Sample PCAP Files
The `pcap_files/` directory includes captures from:
- `georgetown.pcap`
- `google.pcap`
- `nat_geo.pcap`
- `wikipedia.pcap`
- `yahoo_finance.pcap`

---

## Compiling Protocol Buffers

If you modify the `.proto` files, recompile them with:

```bash
# For MP3
protoc -I=mp3 --python_out=mp3 mp3/broadcastMsg.proto

# For MP4
protoc -I=mp4 --python_out=mp4 mp4/encrypted_package.proto
```

---

## Key Concepts Demonstrated

| Concept | Location |
|---------|----------|
| TCP Socket Programming | All projects |
| `select()` I/O Multiplexing | MP3, MP4 |
| Protocol Buffers Serialization | MP3, MP4 |
| AES-256-CBC Encryption | MP4 |
| HMAC Message Authentication | MP4 |
| Packet Capture Analysis | MP5 |
| Network Traffic Statistics | MP5 |

---

## License

Educational project — Georgetown University COSC435 Network Security.
