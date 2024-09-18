import codecs
import sys

from config_file_converter import ConfigFileConverter
from ipv4_prefix import IPv4Prefix
from topology import TopologyBuilder

def main(argv):
    topology_builder = TopologyBuilder()
    filenames = argv[1:]
    for filename in filenames:
        # Original configs are NOT UTF-8. Latin1 seems to decode correctly,
        # so we shall use that instead.
        fh = codecs.open(filename, "rb", encoding="latin1")
        converter = ConfigFileConverter(fh.readlines(), topology_builder)
        try:
            converter.parse()
        except Exception as e:
            print(f"Error in {filename}")
            print(e)
        fh.close()
    topology_builder.write_topology(None)


if __name__ == "__main__":
    main(sys.argv)
