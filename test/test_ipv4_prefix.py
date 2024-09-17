import sys

sys.path.append("src")

import pytest

from ipv4_prefix import IPv4Prefix

@pytest.mark.parametrize(
        "address_string,expected",
        (
            ("255.127.63.31","255.127.63.31/32"),
            ("0.0.0.0","0.0.0.0/32")
        )
)
def test_simple_address_converts_correctly(address_string, expected):
    prefix = IPv4Prefix.from_string(address_string)
    assert str(prefix) == expected


@pytest.mark.parametrize(
        "address_string",
        (
            "not an ip address at all",
            "256.0.0.0",
            "5.-23.8.9",
            "1.2.3",
            "1.2.3.4.5",
        )
)
def test_simple_invalid_address_throws_error(address_string):
    with pytest.raises(ValueError):
        IPv4Prefix.from_string(address_string)


@pytest.mark.parametrize(
        "mask_string,expected",
        (
            ("0.0.0.0","0.0.0.0/0"),
            ("255.254.0.0","0.0.0.0/15"),
            ("255.255.255.255","0.0.0.0/32")
        )
)
def test_simple_address_with_mask_converts_correctly(mask_string, expected):
    prefix = IPv4Prefix.from_string("0.0.0.0", mask_string)
    assert str(prefix) == expected

@pytest.mark.parametrize(
        "mask_string",
        (
            "not a mask at all",
            "256.0.0.0",
            "255.-1.0.0",
            "0.0.0",
            "255.255.255.255.255",
            "255.0.0.1",
            "255.255.64.0"
        )
)
def test_invalid_mask_throws_error(mask_string):
    with pytest.raises(ValueError):
        IPv4Prefix.from_string("0.0.0.0", mask_string)

