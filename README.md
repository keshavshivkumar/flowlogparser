# flowlogparser
> By Keshav Shivkumar

## Overview:

- The Flow Log parser takes in an input log CSV file and a lookup table CSV file as inputs, and produces an output text file that contains the counts for tags as well as port-protocol pairs.
- The log is of the format described [here](https://docs.aws.amazon.com/vpc/latest/userguide/flow-log-records.html#flow-logs-fields), in specific, version 2.
- To ensure consistency in the protocol, a dictionary `protocol_map` was made as a global variable, using data from the [International Assigned Numbers Authority (IANA)](https://www.iana.org/assignments/protocol-numbers/protocol-numbers-1.csv). The protocol numbers are mapped to their respective names.

## Run the program:

- To run the program, run the command in the terminal:
    - ```python parser.py <input_log.csv> <lookup_table.csv>```
    - replace `input_log.csv` with the input log file and `lookup_table.csv` with the lookup table file.

## Assumptions:

- The input and lookup table files are of CSV format, at least the data should be in the comma-separated format.
- The protocol names are case insensitive.
- The logs are of the fixed specified format. The program should be able to handle from Versions 2-7 as long as the fields in V2 are in the same order and not null.
- The matches are case-insensitive.
- The tags can map to more than one port-protocol combinations.