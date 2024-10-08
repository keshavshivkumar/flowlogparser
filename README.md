# flowlogparser
> By Keshav Shivkumar

## Overview:

- The Flow Log parser takes in an input log CSV file and a lookup table CSV file as inputs, and produces an output text file that contains the counts for tags as well as port-protocol pairs.
- The log is of the format described [here](https://docs.aws.amazon.com/vpc/latest/userguide/flow-log-records.html#flow-logs-fields), in specific, version 2.
- To ensure consistency in the protocol, a dictionary `protocol_map` was made as a global variable, using data from the [International Assigned Numbers Authority (IANA)](https://www.iana.org/assignments/protocol-numbers/protocol-numbers-1.csv). The protocol numbers are mapped to their respective names.
- Test cases are written in `parser_test.py` using the `unittest` library to ensure the correctness of the code.

## Run the program:

- To run the program, run the command in the terminal:
    - ```python parser.py <input_log.ext> <lookup_table.ext> <output_filename.ext>```
    - replace `<input_log.ext>` with the input log file, `<lookup_table.ext>` with the lookup table file, and `<output_filename.ext>` with the name of the output file (where `ext` is the extension, either `csv` or `txt`).
- To run the test cases, run the command in the terminal:
    - ```python -m unittest parser_test.py```
    - The test file requires a `sampleinput.csv` and `samplelookuptable.csv`.

## Assumptions:

- The input and lookup table files are of CSV format, at least the data should be in the comma-separated format.
- The protocol names are case insensitive.
- The logs are of the fixed specified format. The program should be able to handle from Versions 2-7 as long as the fields in V2 are in the same order and not null.
- The matches are case-insensitive.
- The tags can map to more than one port-protocol combinations: multiple dstport-protocol entries with common tag names will fall under the same count of the tag name, but will have separate counts in the port-protocol counts.
- In the port-protocol pairs, `dstport` was taken to be the port.
- The file written to will be of TXT/CSV format.
- The test case file deletes the files it creates. If any existing file exists in the directory and happens to have the same name as one of the files being used in the code, it will get overwritten then deleted.

## Analysis and Conclusion:

- The code depends on the positions on the `dstport` and `protocol` in each row, and will fail/work inconsistently if this is violated.
- The program can be improved using a tabular approach, possibly one that incorporates `pandas`.
- The program should run in O(n) time complexity.