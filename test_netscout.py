import ipaddress
from unittest.mock import patch

import netscout


def test_parse_ports():
    assert netscout.parse_ports("80,443,22") == [22, 80, 443]


def test_parse_ports_removes_duplicates():
    assert netscout.parse_ports("80,80,443") == [80, 443]


def test_parse_ports_rejects_invalid_port():
    try:
        netscout.parse_ports("0")
    except Exception:
        pass
    else:
        raise AssertionError("Invalid port was accepted")


def test_parse_ports_rejects_non_numeric_port():
    try:
        netscout.parse_ports("http")
    except Exception:
        pass
    else:
        raise AssertionError("Invalid port was accepted")


@patch("netscout.socket.create_connection")
def test_scan_port_open(mock_connection):
    assert netscout.scan_port("192.168.1.1", 80) is True
    mock_connection.assert_called_once()


@patch(
    "netscout.socket.create_connection",
    side_effect=OSError,
)
def test_scan_port_closed(mock_connection):
    assert netscout.scan_port("192.168.1.1", 80) is False


@patch("netscout.socket.create_connection")
def test_is_host_alive(mock_connection):
    assert netscout.is_host_alive(
        ipaddress.ip_address("192.168.1.1")
    ) is True


@patch(
    "netscout.socket.create_connection",
    side_effect=OSError,
)
def test_is_host_not_alive(mock_connection):
    assert netscout.is_host_alive(
        ipaddress.ip_address("192.168.1.1")
    ) is False


@patch("netscout.socket.getservbyport", return_value="https")
def test_service_name(mock_service):
    assert netscout.service_name(443) == "https"


@patch(
    "netscout.socket.getservbyport",
    side_effect=OSError,
)
def test_unknown_service(mock_service):
    assert netscout.service_name(9999) == "unknown"


@patch("netscout.scan_port", return_value=True)
def test_scan_host(mock_scan):
    result = netscout.scan_host(
        "192.168.1.1",
        [443, 80],
    )

    assert result == [
        (80, "http"),
        (443, "https"),
    ]


@patch("netscout.is_host_alive", return_value=True)
def test_discover_hosts(mock_alive):
    network = ipaddress.ip_network("192.168.1.0/30")

    result = netscout.discover_hosts(network)

    assert result == [
        "192.168.1.1",
        "192.168.1.2",
    ]