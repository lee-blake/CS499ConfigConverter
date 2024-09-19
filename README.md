# Config Converter
Converts router config files into a description of router connections to subnets. 

# Usage
## Replication
Clone or download zip. Only files in the `src` directory are necessary to run

## Running
Run via `python src/main.py file1 file2 file3 --out-file output_file` to write the output to `output_file`. Depending on where you invoke from, you may need to change the path to `main.py`.

## Tips and tricks
To run on all files in a directory, shell expansions can be useful: `python src/main.py path/to/config/directory/*.cfg`
