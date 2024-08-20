import sys

def log_parser(input_file, lookup_table):
    '''
    Takes in an input log file and lookup table file, both in comma-separated format, 
    and matches the dsport-protocol_name pairs to their counts as well as their tags, 
    which is also matched to their counts.
    '''
    with open(lookup_table, 'r') as lookup:
        table = [x.strip().split(',') for x in lookup.readlines()]
        if not table[0][0].isdigit(): # if the column headings are provided
            table = table[1:]

    with open(input_file, 'r') as logs:
        loglist = [x.strip().split(',') for x in logs.readlines()]
        if not loglist[0][0].isdigit(): # if the column headings are provided
            loglist = loglist[1:]
    
    port_protocol_tag_map = {}
    for d, p, tag in table:
        protocol = protocol_map.get(p, p).lower()
        port_protocol_tag_map[(d, protocol)] = tag.lower()

    tag_counts = {} # stores the counts for the corresponding tag
    port_protocol_counts = {} # stores the counts for the corresponding port-protocol pair

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

    with open('output.txt', 'w') as f:
        f.write('Tag Counts:\n')
        f.write('Tag, Count\n')
        for t, c in tag_counts.items():
            f.write(f'{t},{c}\n')
        f.write('\n')
        f.write('Port/Protocol Combination Counts:\n')
        f.write('Port,Protocol,Count\n')
        for p, c in port_protocol_counts.items():
            f.write(f'{p[0]},{p[1]},{c}\n')
    print(tag_counts, port_protocol_counts, port_protocol_tag_map)
    print(f'Tag Counts: {tag_counts}\nPort-Protocol Counts:{port_protocol_counts}\nWrote to output.txt...\nExiting\n')


if __name__ == '__main__':
    protocol_map = {}
    with open('protocol-numbers.csv', 'r') as p:
        for protocol in p.readlines()[1:]:
            data = protocol.strip().split(',')
            if len(data) > 1 and data[0].isdigit():
                if data[1]: # some protocol names are empty, so avoiding those protocols
                    protocol_map[data[0]] = data[1].lower()

    inputfile = sys.argv[1]
    lookup = sys.argv[2]
    log_parser(inputfile, lookup)