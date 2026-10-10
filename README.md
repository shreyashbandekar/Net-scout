# NetScout

Lightweight network reconnaissance and TCP port scanning tool built with Python.

## Overview

NetScout is a command-line cybersecurity utility for authorized network reconnaissance and defensive security testing.

It can discover responsive hosts on a local IPv4 `/24` network, scan explicitly selected IPv4 or IPv6 targets, discover hosts within a specified CIDR network, and export results as JSON.

IPv6 network discovery is deliberately restricted to networks containing no more than 256 addresses to prevent accidental scanning of enormous address spaces.

## Features

- Local IPv4 `/24` host discovery
- Custom IPv4 and IPv6 CIDR network discovery
- IPv4 and IPv6 target scanning
- Concurrent TCP port scanning
- Configurable host-discovery ports
- Custom target ports
- TCP service identification
- Configurable connection timeout
- JSON report export
- Input validation
- Automated tests with pytest
- GitHub Actions CI

## Requirements

- Python 3.11 or newer
- `pytest` for development and testing
- Network access to the authorized targets being assessed

NetScout uses Python's standard library for its scanning and reporting functionality. `pytest` is required only for running the test suite.

## Installation

Clone the repository:

    git clone https://github.com/shreyashbandekar/net-scout.git
    cd net-scout

Install the test dependency:

    python -m pip install pytest

## Usage

### Show Help

    python netscout.py --help

### Discover Hosts on the Local Network

    python netscout.py --discover

By default, NetScout checks TCP ports `22`, `80`, and `443` to identify responsive hosts.

### Discover Hosts in a CIDR Network

    python netscout.py --network 192.168.1.0/24

Use only networks you own or have explicit permission to assess.

### Configure Discovery Ports

    python netscout.py --discover --discovery-ports 80,443

### Scan a Specific Target

    python netscout.py --target 192.168.1.1

### Scan Custom TCP Ports

    python netscout.py --target 192.168.1.1 --ports 22,80,443

### Configure the Connection Timeout

    python netscout.py --target 192.168.1.1 --timeout 1

### Export Results as JSON

Target scan:

    python netscout.py --target 192.168.1.1 --ports 80,443 --json target-report.json

Network discovery:

    python netscout.py --network 192.168.1.0/24 --json network-report.json

### Scan an IPv6 Target

    python netscout.py --target 2001:db8::1 --ports 80,443

The address above is reserved for documentation and is an example, not a real scanning target.

### Discover Hosts in a Small IPv6 Network

    python netscout.py --network 2001:db8::/126 --discovery-ports 443

IPv6 network discovery rejects networks larger than `/120`. A `/120` network contains 256 addresses.

## Command Options

| Option | Description |
|---|---|
| `--discover` | Discover responsive hosts on the local IPv4 `/24` network |
| `--network` | Discover responsive hosts in a specified IPv4 or IPv6 CIDR network |
| `--target` | Scan a specific IPv4 or IPv6 address |
| `--discovery-ports` | Set the comma-separated TCP ports used for host discovery |
| `--ports` | Set the comma-separated TCP ports used for target scanning |
| `--timeout` | Set the TCP connection timeout in seconds |
| `--json` | Save scan or discovery results to a JSON file |
| `--help` | Display command-line help |

## How It Works

### Host Discovery

NetScout checks selected TCP ports to identify responsive hosts. By default, discovery checks ports `22`, `80`, and `443`.

Local discovery derives a `/24` network from the detected local IPv4 address. The `--network` option allows an explicit CIDR network to be selected.

### TCP Port Scanning

For a specified target, NetScout attempts TCP connections to the requested ports. Open ports are reported with their service names when available.

Both IPv4 and IPv6 target addresses are supported.

### Concurrency

Thread pools perform network operations concurrently to improve scanning efficiency.

### JSON Reporting

The `--json` option exports results to a JSON file.

Target scans include the target address and discovered open ports. Network discovery reports include the network and responsive hosts.

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

## Testing

Run the automated test suite:

    python -m pytest -v

The current test suite contains **27 tests** covering:

- Port parsing and validation
- Duplicate port handling
- TCP connection success and failure
- Host availability
- Service identification
- Target scanning
- Host discovery across multiple ports
- CIDR parsing
- IPv6 target support
- IPv6 network size restrictions
- JSON report creation and error handling
- Discovery CLI options

The tests mock network connections where appropriate, so automated testing does not depend on the availability of real network hosts.

Run the Python syntax check:

    python -m py_compile netscout.py test_netscout.py

## Security Considerations

NetScout is intended for authorized security testing, network administration, and defensive reconnaissance.

Only scan systems and networks you own or have explicit permission to assess.

The project does not include:

- Exploitation
- Credential attacks
- Stealth or evasion functionality
- Packet injection
- UDP scanning
- Vulnerability detection

## Limitations

The current version has the following limitations:

- Local discovery assumes a `/24` IPv4 network.
- Host discovery relies on TCP connection attempts to selected ports.
- IPv6 network discovery is limited to networks containing no more than 256 addresses.
- Port scanning supports TCP only.
- Service identification relies on the operating system's TCP service database.
- A host may be online but remain undetected if the selected ports do not respond.
- Network filtering, firewalls, and timeouts can affect results.

NetScout is a lightweight reconnaissance utility, not a comprehensive vulnerability scanner.

## CI/CD

GitHub Actions runs automated checks on pushes and pull requests targeting the `main` branch.

The workflow:

1. Checks out the repository.
2. Sets up Python 3.14.
3. Installs `pytest`.
4. Checks Python syntax.
5. Runs the automated test suite.

## Responsible Use

Use NetScout only for legitimate cybersecurity learning, network administration, and authorized security assessments.

You are responsible for ensuring that your scans comply with applicable laws, policies, and permissions. The author is not responsible for misuse of this software.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Author

**Shreyash Bandekar**

Cybersecurity / SOC Analyst

GitHub: [ShreyashBandekar](https://github.com/ShreyashBandekar)

---

Built for cybersecurity learning, network reconnaissance, and defensive security practice.