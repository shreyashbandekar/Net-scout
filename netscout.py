import argparse
import ipaddress
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed


DEFAULT_PORTS = [22, 80, 443, 445, 3389]
DEFAULT_TIMEOUT = 0.5


def get_local_network():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)

    network = ipaddress.ip_network(
        f"{local_ip}/24",
        strict=False,
    )

    return local_ip, network


def is_host_alive(ip, timeout=DEFAULT_TIMEOUT):
    try:
        with socket.create_connection(
            (str(ip), 80),
            timeout=timeout,
        ):
            return True
    except (OSError, TimeoutError):
        return False


def discover_hosts(network, timeout=DEFAULT_TIMEOUT):
    hosts = []

    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = {
            executor.submit(is_host_alive, ip, timeout): ip
            for ip in network.hosts()
        }

        for future in as_completed(futures):
            ip = futures[future]

            try:
                if future.result():
                    hosts.append(str(ip))
            except OSError:
                continue

    return sorted(hosts, key=ipaddress.ip_address)


def scan_port(ip, port, timeout=DEFAULT_TIMEOUT):
    try:
        with socket.create_connection(
            (ip, port),
            timeout=timeout,
        ):
            return True
    except (OSError, TimeoutError):
        return False


def service_name(port):
    try:
        return socket.getservbyport(port, "tcp")
    except OSError:
        return "unknown"


def scan_host(ip, ports, timeout=DEFAULT_TIMEOUT):
    results = []

    with ThreadPoolExecutor(max_workers=len(ports)) as executor:
        futures = {
            executor.submit(scan_port, ip, port, timeout): port
            for port in ports
        }

        for future in as_completed(futures):
            port = futures[future]

            try:
                if future.result():
                    results.append(
                        (port, service_name(port))
                    )
            except OSError:
                continue

    return sorted(results)


def parse_ports(value):
    ports = []

    for item in value.split(","):
        try:
            port = int(item.strip())
        except ValueError:
            raise argparse.ArgumentTypeError(
                f"Invalid port: {item}"
            )

        if not 1 <= port <= 65535:
            raise argparse.ArgumentTypeError(
                f"Port out of range: {port}"
            )

        ports.append(port)

    if not ports:
        raise argparse.ArgumentTypeError(
            "At least one port is required."
        )

    return sorted(set(ports))


def parse_args():
    parser = argparse.ArgumentParser(
        description="NetScout - lightweight network reconnaissance tool."
    )

    parser.add_argument(
        "--discover",
        action="store_true",
        help="Discover live hosts on the local /24 network.",
    )

    parser.add_argument(
        "--target",
        help="Scan a specific IPv4 address.",
    )

    parser.add_argument(
        "--ports",
        type=parse_ports,
        default=DEFAULT_PORTS,
        help="Comma-separated TCP ports.",
    )

    parser.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_TIMEOUT,
        help="Connection timeout in seconds.",
    )

    return parser.parse_args()


def main():
    args = parse_args()

    if args.timeout <= 0:
        raise SystemExit("Timeout must be greater than zero.")

    if args.target:
        try:
            target = ipaddress.ip_address(args.target)
        except ValueError:
            raise SystemExit("Invalid IP address.")

        if target.version != 4:
            raise SystemExit("Only IPv4 targets are supported.")

        print(f"\nTarget: {target}\n")

        results = scan_host(
            str(target),
            args.ports,
            args.timeout,
        )

        if not results:
            print("No open ports found.")
            return

        print("PORT    STATE    SERVICE")
        for port, service in results:
            print(f"{port:<7} OPEN     {service}")

        return

    if args.discover:
        local_ip, network = get_local_network()

        print(f"\nLocal IP: {local_ip}")
        print(f"Network:  {network}")
        print("\nDiscovering hosts...\n")

        hosts = discover_hosts(
            network,
            args.timeout,
        )

        if not hosts:
            print("No responsive hosts found.")
            return

        print("HOST")
        print("----")

        for host in hosts:
            print(host)

        return

    print("Use --discover or --target <IP>.")


if __name__ == "__main__":
    main()