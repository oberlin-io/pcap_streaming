#p = '/mnt/c/Users/joberlin/Documents/pcap_streaming/pcap_streaming/appendix/dump_test.txt'
p = 'dump_test.txt'

with open(p, 'r') as f:
    dump = f.readlines()

from packet_parse import PacketParse
import json

p_parse = PacketParse()
p_parse.set_regex()

for line in dump:
    print(line)

    d = p_parse.get_values(line)
    for k, v in d.items():
        print(k, ':', v)
    print('')
