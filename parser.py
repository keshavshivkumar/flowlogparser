import sys

def log_parser(input_file, lookup_table, output_file):
    '''
    Takes in an input log file and lookup table file, both in comma-separated format, 
    and matches the dsport-protocol_name pairs to their counts as well as their tags, 
    which is also matched to their counts.
    '''
    try:
        with open(lookup_table, 'r') as lookup:
            table = [x.strip().split(',') for x in lookup.readlines()]
            if not table[0][0].isdigit(): # if the column headings are provided
                table = table[1:]
    except FileNotFoundError:
        print(f"Error: The lookup table file was not found.")
        sys.exit(1)
    except IndexError:
        print(f"Lookup table is empty!")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred while reading the lookup table: {e}")
        sys.exit(1)

    try:
        with open(input_file, 'r') as logs:
            loglist = [x.strip().split(',') for x in logs.readlines()]
            if not loglist[0][0].isdigit(): # if the column headings are provided
                loglist = loglist[1:]
    except FileNotFoundError:
        print(f"Error: The log file was not found.")
        sys.exit(1)
    except IndexError:
        print(f"Log input is empty!")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred while reading the logs: {e}")
        sys.exit(1)
    
    tag_counts = {} # stores the counts for the corresponding tag
    port_protocol_counts = {} # stores the counts for the corresponding port-protocol pair
    port_protocol_tag_map = {}
    for d, p, tag in table:
        protocol = protocol_map.get(p, p).lower()
        port_protocol_tag_map[(d, protocol)] = tag.lower()

    try:
        for log in loglist:
            dstport = log[10]
            protocol_index = log[13]
            protocol_name = protocol_map.get(str(protocol_index), protocol_index).lower() # mapping protocol number to name (lower-case) if it is not in name format already
            
            key = (dstport, protocol_name)

            if key in port_protocol_tag_map:
                tag = port_protocol_tag_map[key].lower()
                port_protocol_counts[key] = port_protocol_counts.get(key, 0) + 1
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
            else:
                tag_counts['Untagged'] += 1

    except KeyError as e:
        print(f"KeyError: {e} was not found.")
        sys.exit(1)

    except IndexError as e:
        print(f"IndexError: {e}")
        sys.exit(1)

    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

    try:
        write_data(tag_counts, port_protocol_counts, output_file)
    except IOError as e:
        print(f"Error writing to output file: {e}")
        sys.exit(1)

def write_data(tag_counts, port_protocol_counts, output_file):
    '''
    Writes the data obtained from the input logs and lookup table to an output file.
    The two dictionaries and output file name are the parameters.
    '''
    with open(output_file, 'w') as f: # writing to output file
        f.write('Tag Counts:\n')
        f.write('Tag, Count\n')
        for t, c in tag_counts.items():
            f.write(f'{t},{c}\n')
        f.write('\n')
        f.write('Port/Protocol Combination Counts:\n')
        f.write('Port,Protocol,Count\n')
        for p, c in port_protocol_counts.items():
            f.write(f'{p[0]},{p[1]},{c}\n')
    print(f'Tag Counts: {tag_counts}\nPort-Protocol Counts:{port_protocol_counts}\nWrote to {output_file}...\nExiting\n')

    

protocol_map = {}
with open('protocol-numbers.csv', 'r') as p:
    for protocol in p.readlines()[1:]:
        data = protocol.strip().split(',')
        if len(data) > 1 and data[0].isdigit():
            if data[1]: # some protocol names are empty, so avoiding those protocols
                protocol_map[data[0]] = data[1].lower()

if __name__ == '__main__':
    inputfile = sys.argv[1]
    lookup = sys.argv[2]
    output = sys.argv[3]
    log_parser(inputfile, lookup, output)