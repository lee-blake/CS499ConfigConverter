import re

from math import floor


class IPv4Prefix:
    def __init__(self, address, length):
        self._length = length
        self._address = address

    def __eq__(self, other):
        if not isinstance(other, IPv4Prefix):
            return False
        return self._length == other._length \
                and self._address == other._address

    def __hash__(self):
        return hash(self._length)

    def __str__(self):
        return f"{self._address}/{self._length}"

    def from_string(address_string, mask_string=None):
        if not IPv4Prefix._string_is_ipv4_format(address_string):
            raise ValueError(f"Not a valid IPv4 address: {address_string}")
        if not mask_string:
            mask_string = "255.255.255.255"
        if not IPv4Prefix._string_is_ipv4_format(mask_string):
            raise ValueError(f"Not a valid mask: {mask_string}")
        overextended = not IPv4Prefix._check_address_does_not_exceed_mask(
            address_string,
            mask_string
        )
        if overextended:
            raise ValueError("The address extends beyond the mask!")
        prefix_length = IPv4Prefix._length_from_string(mask_string)
        return IPv4Prefix(address_string, prefix_length)

    def rationalize_from_string(address_string, mask_string=None):
        if mask_string:
            address_int = IPv4Prefix._convert_ip_string_to_int(address_string)
            mask_int = IPv4Prefix._convert_ip_string_to_int(mask_string)
            rationalized_address_int = address_int & mask_int
            address_string = IPv4Prefix._get_ip_string_from_int(rationalized_address_int)
        return IPv4Prefix.from_string(address_string, mask_string)

    def _length_from_string(mask_string):
        mask_value = IPv4Prefix._convert_ip_string_to_int(mask_string)
        last_1_index = 0
        for i in range(32, 0, -1):
            digit = mask_value % 2
            if digit == 1:
                if not last_1_index:
                    last_1_index = i
            else:
                if last_1_index:
                    raise ValueError(
                            "Not a valid mask because there is a 0 between 1s!"
                    )
            mask_value //= 2
        return last_1_index

    def _convert_ip_string_to_int(ip_string):
        segment_values = [int(value) for value in ip_string.split(".")]
        place_value = 1
        total = 0
        for segment_value in reversed(segment_values):
            total += segment_value*place_value
            place_value *= 256
        return total

    def _string_is_ipv4_format(address):
        ipv4_regex = re.compile(r"\d+\.\d+\.\d+\.\d+$")
        if not re.match(ipv4_regex, address):
            return False
        values = [int(value) for value in address.split(".")]
        for value in values:
            if not (value >= 0 and value <= 255):
                return False
        return True

    def _check_address_does_not_exceed_mask(address, mask):
        address_int = IPv4Prefix._convert_ip_string_to_int(address)
        mask_int = IPv4Prefix._convert_ip_string_to_int(mask)
        overextended_bits_int = address_int & ~mask_int
        return overextended_bits_int == 0
        
    def _get_ip_string_from_int(ip_int):
        string_components = []
        for i in range(0, 4):
            component = ip_int % 256
            string_components.append(f"{component}")
            ip_int = floor(ip_int / 256)
        return ".".join(reversed(string_components))



