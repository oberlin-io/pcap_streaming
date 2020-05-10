import subprocess
import threading

netcat_port = 8888
pcap_file = 'smallFlows.pcap'

def tcpdump_to_netcat(netcat_port):
    '''
    Sniff traffic on interface and pipe to netcat
    '''
    cmd = 'sudo tcpdump -i eth0 -nn -vvvv '
    cmd += '|netcat localhost -p {}'.format(netcat_port)
    subprocess.run(cmd)


def tcpreplay(pcap_file):
    '''
    Simulate network traffic on the interface with tcpreplay
    '''
    cmd = 'sudo tcpreplay -i eth0 -K --loop 1 {}'.format(pcap_file)
    subprocess.run(cmd)


if __name__ == '__main__':

    t2n = threading.Thread(target=tcpdump_to_netcat)
    t2n.start()

    tre = threading.Thread(target=tcpreplay)
    tre.start()
