import re

from ipv4_prefix import IPv4Prefix


class ConfigFileConverter:
    ip_notation_re = r"\d+\.\d+\.\d+\.\d+"

    hostname_instruction = re.compile(r"hostname (\S+)\s*$")
    interface_instruction = re.compile(r"interface (\S+)\s*$")
    macro_instruction = re.compile(r"macro .*$")
    end_block_instruction = re.compile(r"(!|@)\s*$")

    no_ip_or_shutdown_instruction = re.compile(r"\s+(shutdown|no ip address)\s*$")
    ip_address_instruction = re.compile(
            f"\\s+ip address ({ip_notation_re}) ({ip_notation_re})"
    )

    
    def __init__(self, config_lines, topology_tracker=None):
        self._config_lines = config_lines
        self._current_hostname = None

    def parse(self):
        lines_iter = iter(self._config_lines)
        print_next = False
        for line in lines_iter:
            if self.hostname_instruction.match(line):
                self._handle_hostname_instruction(line)
            elif self.interface_instruction.match(line):
                self._handle_interface_instruction(
                        self._gather_block_lines(lines_iter, line)
                )
            elif self.macro_instruction.match(line):
                # Discard the macro.
                self._gather_block_lines(lines_iter, line)

    def _gather_block_lines(self, iterator, first_line):
        """Consumes lines from an iterator until the block ends. Returns
        all lines in the block when completed. Note that this will affect
        any for loop operating over the iterator - it will continue after
        the block ends. The first line must be passed because it cannot be
        re-read."""
        interface_block_lines = [first_line]
        line = first_line
        while not self.end_block_instruction.match(line):
            line = next(iterator)
            interface_block_lines.append(line)
        return interface_block_lines

    def _handle_hostname_instruction(self, instruction):
        hostname = self.hostname_instruction.match(instruction).group(1)
        self._current_hostname = hostname
        print(f"Hostname found: {hostname}")

    def _handle_interface_instruction(self, block_lines):
        block_iter = iter(block_lines)
        first_line = next(block_iter)
        interface_name = self.interface_instruction.match(first_line).group(1)
        prefix = None
        for line in block_iter:
            if self.no_ip_or_shutdown_instruction.match(line):
                return
            else:
                match = self.ip_address_instruction.match(line)
                if match:
                    prefix = IPv4Prefix.from_string(match.group(1), match.group(2))
        if prefix:       
            print(f"\t{interface_name}: {prefix}")

