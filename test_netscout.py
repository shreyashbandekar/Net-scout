import argparse
import ipaddress
import json
from unittest.mock import patch

import pytest

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
        ipaddress.ip_address("192.168.1.1"),
        [22, 80, 443],
    ) is True

    assert mock_connection.call_count == 1


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
    ports = [22, 80, 443]

    result = netscout.discover_hosts(
        network,
        ports,
    )

    assert result == [
        "192.168.1.1",
        "192.168.1.2",
    ]

    assert mock_alive.call_count == 2

    for call in mock_alive.call_args_list:
        assert call.args[1] == ports


def test_parse_network():
    assert netscout.parse_network(
        "192.168.1.0/24"
    ) == ipaddress.ip_network("192.168.1.0/24")


def test_parse_network_ipv6():
    with pytest.raises(argparse.ArgumentTypeError):
        netscout.parse_network("2001:db8::/64")

def test_discovery_arguments_are_mutually_exclusive():
    with patch(
        "sys.argv",
        ["netscout.py", "--discover", "--network", "192.0.2.0/30"],
    ):
        try:
            netscout.parse_args()
        except SystemExit as error:
            assert error.code == 2
        else:
            raise AssertionError(
                "Conflicting discovery arguments were accepted"
            )

def test_save_json_report(tmp_path):
    path = tmp_path / "report.json"

    data = {
        "target": "192.168.1.1",
        "ports": [
            {
                "port": 443,
                "service": "https",
            }
        ],
    }

    netscout.save_json_report(path, data)

    with open(path, encoding="utf-8") as file:
        result = json.load(file)

    assert result == data

def test_network_json_report(tmp_path):
    path = tmp_path / "network.json"

    data = {
        "network": "192.0.2.0/30",
        "hosts": [],
    }

    netscout.save_json_report(path, data)

    with open(path, encoding="utf-8") as file:
        result = json.load(file)

    assert result == data

def test_discover_json_report(tmp_path):
    path = tmp_path / "discover.json"

    data = {
        "network": "192.168.29.0/24",
        "hosts": ["192.168.29.1"],
    }

    netscout.save_json_report(path, data)

    with open(path, encoding="utf-8") as file:
        result = json.load(file)

    assert result == data

def test_save_json_report_invalid_path():
    data = {
        "test": True,
    }

    try:
        netscout.save_json_report(
            "missing_folder/report.json",
            data,
        )
    except OSError:
        pass
    else:
        raise AssertionError(
            "Invalid report path did not raise an error"
        )

@patch("netscout.socket.create_connection")

def test_is_host_alive_checks_multiple_ports(mock_connection):
    successful_connection = mock_connection.return_value
    mock_connection.side_effect = [
        OSError,
        OSError,
        successful_connection,
    ]

    assert netscout.is_host_alive(
        ipaddress.ip_address("192.168.1.1"),
        [22, 80, 443],
    ) is True

    assert mock_connection.call_count == 3

@patch(
    "netscout.socket.create_connection",
    side_effect=OSError,
)
def test_is_host_alive_all_ports_closed(mock_connection):
    assert netscout.is_host_alive(
        ipaddress.ip_address("192.168.1.1"),
        [22, 80, 443],
    ) is False

    assert mock_connection.call_count == 3

def test_parse_discovery_ports():
    with patch(
        "sys.argv",
        ["netscout.py", "--discover", "--discovery-ports", "443,80"],
    ):
        args = netscout.parse_args()

    assert args.discovery_ports == [80, 443]

def test_default_discovery_ports():
    with patch(
        "sys.argv",
        ["netscout.py", "--discover"],
    ):
        args = netscout.parse_args()

    assert args.discovery_ports == [22, 80, 443]

def test_parse_ipv6_target():
    target = ipaddress.ip_address("2001:db8::1")

    assert target.version == 6
    assert str(target) == "2001:db8::1"

def test_parse_network_allows_small_ipv6_network():
    network = netscout.parse_network("2001:db8::/120")

    assert network.version == 6
    assert network.num_addresses == 256


def test_parse_network_rejects_large_ipv6_network():
    with pytest.raises(argparse.ArgumentTypeError):
        netscout.parse_network("2001:db8::/112")

def test_target_and_network_arguments_are_mutually_exclusive():
    with patch(
        "sys.argv",
        [
            "netscout.py",
            "--network",
            "192.168.1.0/24",
            "--target",
            "192.168.1.1",
        ],
    ):
        with pytest.raises(SystemExit) as exc_info:
            netscout.parse_args()

    assert exc_info.value.code == 2
