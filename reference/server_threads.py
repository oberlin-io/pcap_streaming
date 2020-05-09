import subprocess
import threading


def conf_mtu():
    '''
    Noticed at least one PCAP file requires greater MTU
    Needs set each restart of server instance
    '''
    mtu = 1500
    cmd = 'sudo ip link set eth0 mtu {}'.format(mtu)
    subprocess.run(cmd, shell=True)


def tcpdump_to_netcat(host_port=4444):
    '''
    Sniff traffic on interface and pipe to netcat
    '''
    cmd = 'sudo tcpdump -i eth0 -nn -vvvv '
    cmd += '|netcat -lk -p {}'.format(host_port)
    subprocess.run(cmd, shell=True)


def tcpreplay():
    '''
    Simulate network traffic on the interface with tcpreplay
    '''
    pcap_file = 'smallFlows.pcap'
    cmd = 'sudo tcpreplay -i eth0 -K --loop 1 {}'.format(pcap_file)
    subprocess.run(cmd, shell=True)


if __name__ == '__main__':

    conf_mtu()

    tre = threading.Thread(target=tcpreplay)
    tre.start()

    t2n = threading.Thread(target=tcpdump_to_netcat)
    t2n.start()
