#!/bin/python
import argparse
import codecs
import sys

from config_file_converter import ConfigFileConverter
from ipv4_prefix import IPv4Prefix
from topology import TopologyBuilder



class PrintWriter:
        def write(self, stuff):
            print(stuff, end="")

        def close(self):
            pass

def setup_parser():
    parser = argparse.ArgumentParser(prog="python src/main.py")
    parser.add_argument("input_files", nargs="+", help="Path to the files to parse to build the topology.")
    parser.add_argument("--out-file", help="Path to the file to output the converted config.")
    return parser

def get_output_handle(output_filename):
    if not output_filename:
        return PrintWriter()
    return open(output_filename, "wt")

def main(argv):
    # Throw away this file if "python *main.py" is invoked, it should
    # not be an argument at all.
    if "main.py" in argv[0]:
        argv = argv[1:]
    arg_parser = setup_parser()
    args = arg_parser.parse_args()
    topology_builder = TopologyBuilder()
    filenames = args.input_files
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
    output_handle = get_output_handle(args.out_file)
    topology_builder.write_topology(output_handle)
    output_handle.close()


if __name__ == "__main__":
    main(sys.argv)
