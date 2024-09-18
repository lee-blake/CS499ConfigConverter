import codecs
import sys

from config_file_converter import ConfigFileConverter
from ipv4_prefix import IPv4Prefix

def main(argv):
    filename = argv[1]
    # Original configs are NOT UTF-8. Latin1 seems to decode correctly,
    # so we shall use that instead.
    fh = codecs.open(filename, "rb", encoding="latin1")
    converter = ConfigFileConverter(fh.readlines())
    converter.parse()
    fh.close()


if __name__ == "__main__":
    main(sys.argv)
