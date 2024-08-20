import sys


def log_parser(filename, lookup_table):
    with open(lookup_table, 'r') as lookup:
        table = [x.strip().split(',') for x in lookup.readlines()]
        if not table[0][0].isdigit():
            table = table[1:]

    with open(filename, 'r') as logs:
        loglist = [x.strip().split(',') for x in logs.readlines()]
        if not loglist[0][0].isdigit():
            loglist = loglist[1:]
    
    tag_counts = {}
    port_protocol_counts = {}
    for log in loglist:
        dstport = log[10]
        protocol_index = log[13]
        protocol_name = protocol_map.get(str(protocol_index), protocol_index)
        
        tag_found = False
        
        for d, p, tag in table:
            # print(f'd: {d}, dstport: {dstport}, p: {protocol_map[p]}, protocol_name: {protocol_name}')
            if d == dstport and protocol_map[p] == protocol_name:
                key = f'{dstport},{protocol_name}'
                port_protocol_counts[key] = port_protocol_counts.get(key, 0) + 1
                if tag not in tag_counts:
                    tag_counts[tag] = 0
                tag_counts[tag] += 1
                tag_found = True
        
        if not tag_found:
            if 'Untagged' not in tag_counts:
                tag_counts['Untagged'] = 0
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
            f.write(f'{p},{c}\n')

    print(f'Tag Counts: {tag_counts}\nPort-Protocol Counts:{port_protocol_counts}\nWrote to output.txt...\nExiting\n')


if __name__ == '__main__':
    protocol_map = {}
    with open('protocol-numbers.csv', 'r') as p:
        for protocol in p.readlines()[1:]:
            data = protocol.strip().split(',')
            if len(data) > 1 and data[0].isdigit():
                if data[1]:
                    protocol_map[data[0]] = data[1]
    inputfile = sys.argv[1]
    lookup = sys.argv[2]
    log_parser(inputfile, lookup)