# NetScout

Lightweight network reconnaissance and TCP port scanning tool built with Python.

## Overview

NetScout is a command-line cybersecurity utility for authorized network reconnaissance.

It can discover responsive hosts on a local IPv4 `/24` network and scan a specific IPv4 target for selected TCP ports.

## Features

- Local `/24` network discovery
- IPv4 target scanning
- TCP port scanning
- Concurrent network operations
- Common TCP service identification
- Custom port selection
- Configurable connection timeout
- Input validation
- Command-line interface
- Automated tests
- GitHub Actions CI

## Usage

### Show Help

    python netscout.py --help

### Discover Local Hosts

    python netscout.py --discover

Example:

    Local IP: 192.168.1.100
    Network:  192.168.1.0/24

    Discovering hosts...

    HOST
    ----
    192.168.1.1
    192.168.1.10

### Scan a Specific Host

    python netscout.py --target 192.168.1.1

Example:

    Target: 192.168.1.1

    PORT    STATE    SERVICE
    80      OPEN     http
    443     OPEN     https

### Scan Custom Ports

    python netscout.py --target 192.168.1.1 --ports 22,80,443

### Configure Timeout

    python netscout.py --target 192.168.1.1 --timeout 1

## Command Options

| Option | Description |
|---|---|
| `--discover` | Discover responsive hosts on the local `/24` network |
| `--target` | Scan a specific IPv4 address |
| `--ports` | Comma-separated TCP ports |
| `--timeout` | Connection timeout in seconds |
| `--help` | Display command help |

## How It Works

### Network Discovery

NetScout determines the local IPv4 address and derives the local `/24` network.

It attempts TCP connections to port 80 on network hosts to identify responsive systems.

### Port Scanning

For a selected target, NetScout attempts TCP connections to the requested ports.

Open ports are reported with their TCP service name when available.

### Concurrency

Thread pools are used for host discovery and port scanning to perform network operations concurrently.

## Testing

The project includes automated tests covering:

- Port parsing
- Duplicate port handling
- Invalid port rejection
- TCP connection success and failure
- Host availability
- Service identification
- Host scanning
- Network discovery

Run the test suite:

    python -m pytest -v

Current test result:

    12 passed in 0.16s

The automated tests mock network connections, so the test suite does not depend on access to a real network.

## Requirements

- Python 3.11+
- `pytest` for development and testing

## Installation

Clone the repository:

    git clone https://github.com/shreyashbandekar/net-scout.git
    cd net-scout

Install the test dependency:

    python -m pip install pytest

## Project Structure

    net-scout/
    ├── .github/
    │   └── workflows/
    │       └── python-ci.yml
    ├── .gitignore
    ├── netscout.py
    ├── test_netscout.py
    ├── README.md
    └── LICENSE

## Security Considerations

NetScout is intended for authorized security testing, network administration, and defensive reconnaissance.

Only scan systems and networks you own or have explicit permission to assess.

The project does not include:

- Exploitation
- Credential attacks
- Vulnerability exploitation
- Stealth or evasion functionality
- Packet injection
- UDP scanning

## CI/CD

GitHub Actions automatically:

1. Checks out the repository.
2. Sets up Python 3.14.
3. Installs `pytest`.
4. Checks Python syntax.
5. Runs the automated test suite.

## Roadmap

Potential future improvements:

- CIDR network selection
- Additional service detection
- JSON result export
- CSV result export
- Optional banner grabbing
- Improved host discovery methods
- IPv6 support

These features are intentionally outside the current v1 scope.

## Responsible Use

NetScout is a reconnaissance tool intended for legitimate cybersecurity learning, network administration, and authorized security assessments.

Use it only against systems and networks where you have permission to perform scanning.

The author is not responsible for misuse of this software.

## Limitations

The current version has several intentional limitations:

- Host discovery uses TCP port 80.
- Network discovery assumes a local `/24` IPv4 network.
- Only IPv4 targets are supported.
- Port scanning currently supports TCP.
- Service identification relies on the operating system's TCP service database.
- No vulnerability detection is performed.
- No exploitation functionality is included.

These limitations keep the first version focused and lightweight.

## Development

Run the syntax check:

    python -m py_compile netscout.py

Run the automated tests:

    python -m pytest -v

The project uses GitHub Actions to automatically perform both checks on pushes and pull requests targeting the `main` branch.

## License

This project is licensed under the MIT License.

## Author

**Shreyash Bandekar**

Cybersecurity / SOC Analyst

GitHub: `ShreyashBandekar`

---

Built for cybersecurity learning, network reconnaissance, and defensive security practice.