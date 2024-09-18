import codecs
import sys

from config_file_converter import ConfigFileConverter
from ipv4_prefix import IPv4Prefix
from topology import TopologyBuilder

def main(argv):
    filename = argv[1]
    # Original configs are NOT UTF-8. Latin1 seems to decode correctly,
    # so we shall use that instead.
    fh = codecs.open(filename, "rb", encoding="latin1")
    topology_builder = TopologyBuilder()
    converter = ConfigFileConverter(fh.readlines(), topology_builder)
    converter.parse()
    fh.close()
    topology_builder.write_topology(None)


if __name__ == "__main__":
    main(sys.argv)
