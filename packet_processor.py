# For testing packets captured like:
# record traffic
# on 1.0: sudo tcpdump -i eth0 -nn -c 5 -vvvv > tmp.txt
#
# on 1:1: sudo tcpreplay -i eth0 -K --loop 1 messenger.pcap

with open('tmp.txt', 'r') as f:
    pcap = f.read()
    pcap = pcap.replace('\n    ', ' ') # In triple verbose, newline made
    pcap = pcap.split('\n')[:-1]

time_pat = re.compile('^(\d{2}:\d{2}:\d{2}.\d+)\s')
src_pat = re.compile('\s([\d\.]+)\s>')
dst_pat = re.compile('>\s([\d\.]+):')
flags_pat = re.compile('Flags \[([^\]]+)\]')
ip_pat = re.compile('^\d{2}:\d{2}:\d{2}.\d+\s([^\s]+)\s')
proto_pat = re.compile('proto[^\(]+\((\d{1,3})\)')

#ttl_pat = re.compile('ttl (\d+),')

fields = (
  {
  name:    'time'
  re_pat:  '^(\d{2}:\d{2}:\d{2}.\d+)\s'}

  src:
    pat: src_pat
  }
)

class Packet(object):
    def __init__(self, fields):
        pass

need to install pip3 on instance-1 #here

time = time_pat.search(packet).group(1)
src = source_pat.search(pcap[0]).group(1)
dst = dst_pat.search(pcap[0]).group(1)
flags = flag_pat.search(pcap[0]).group(1)
ip = ip_pat.search(pcap[0]).group(1)
ttl = ttl_pat.search(pcap[0]).group(1)
proto = proto_pat.search(pcap[0]).group(1)

try: #code
except Exception as e: log_error(e, field, packet)
