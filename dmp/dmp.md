# Resources
## References and resources
- Packet capture (pcap) is a performant C++ probe that captures network packets and
streams them into Kafka. A pcap Storm topology then streams them into Cloudera
Cybersecurity Platform (CCP)
https://docs.cloudera.com/ccp/2.0.1/add-new-telemetry-data-source/topics/ccp-pcap.html
- Stream Processing vs. Continuous PCAP: The Big Shift in
https://www.extrahop.com/company/blog/2016/stream-processing-vs-continuous-pcap-the-big-shift-in-network-monitoring-architectures/
- Radford. Network Traffic Anomaly Detection Using Recurrent Neural Networks.
28 Mar 2018.
url: https://arxiv.org/pdf/1803.10769.pdf
-
- Iman Sharafaldin, Arash Habibi Lashkari, and Ali A. Ghorbani.
"Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization".
4th International Conference on Information Systems Security and Privacy (ICISSP),
Portugal, January 2018.
- https://www.digitalocean.com/community/tutorials/how-to-install-apache-kafka-on-debian-9
- https://cloudwafer.com/blog/installing-apache-kafka-on-debian-9/
- Python kafka
- https://opensource.com/article/18/10/introduction-tcpdump
- AppNeta http://tcpreplay.appneta.com/wiki/tcpreplay-man.html
- ref: Protocol Numbers
https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml
- ref: Description of the Internet Protocol, IP
https://www.eit.lth.se/ppplab/IPHeader.htm
- ref: pcaptools
https://github.com/caesar0301/awesome-pcaptools
- https://alvinalexander.com/linux-unix/linux-processor-cpu-memory-information-commands/
- smallFlows.pcap
https://tcpreplay.appneta.com/wiki/captures.html
- Datasets http://205.174.165.80/CICDataset/CIC-IDS-2017/Dataset/
GeneratedLabelledFlows.zip
This is already processed PCAPs and its resolution is only minutes.
- http://205.174.165.80/CICDataset/CIC-IDS-2017/Dataset/PCAPs/
Friday-WorkingHours.pcap (http://205.174.165.80/CICDataset/CIC-IDS-2017/Dataset/PCAPs/Friday-WorkingHours.pcap)
- Protocol numbers
https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xml

# Pipe capture to Kafka, suggested
It is suggested to pipe tshark (or tcpdump?) output
as JSON to netcat on a port, eg here 8888.
netcat listens on port x and data is piped to Kafka producer script.
```
session 1 > nc -l 8888 | ./producer.sh
session 2 > sudo tshark -l | nc 127.1 8888
```

Or use a named pipe:
```
session 1 > mkfifo tsharkpipe
session 1 > tail -f -c +0 tsharkpipe | producer.sh
session 2 > sudo tshark -l > tsharkpipe
```

# PCAP replay and capture example
In one session, listen to the interface.
```
sudo tcpdump -i eth0 -nn -s0 -v port 80
sudo tcpdump -i eth0 -nn -c 5
```

On session 1, filter to a known host.
```
sudo tcpdump -i eth0 -nn -v host 192.168.3.131
```

<!-- This is capturing the SSH traffic, so filter that out,
but that may filter out network SSH [?] -->

On session 2, replay a PCAP at speed captured.
```
sudo tcpreplay -i eth0 -K --loop 1 smallFlows.pcap
```

Host 192.168.3.131 is known in smallFlows by:
```
sudo tcpdump -v -r smallFlows.pcap > smallFlows.txt
less smallFlows.txt
```

If tcpreplay is throwing, and it will for isntance-a, errors that packets are too large,
increase the MTU setting.
"the maximum transmission unit (MTU) is the size of the largest
protocol data unit (PDU) that can be communicated in a
single network layer transaction.
The MTU relates to, but is not identical to the maximum frame size
that can be transported on the data link layer, e.g. Ethernet frame"
```
ip link list |grep eth0
sudo ip link set eth0 mtu 1500
```

# tcpreplay switches
Some may be tcpdump.

- ```-i``` the interface
- ```-nn``` to disable IP and port name resolution
- ```-c``` number of packets
- ```-l``` number of loops
- ```-K``` "This option loads the specified pcap(s) into RAM
before starting to send in order to improve replay performance
while introducing a startup performance hit."
- ```--pktlen``` "By specifying this option, tcpreplay will ignore
the snaplen field and instead try to send packets based
on the original packet length. Bad things may happen"
- ```--netmap``` "will detect netmap capable network drivers on Linux
and BSD systems. If detected, the network driver is bypassed for
the execution duration, and network buffers will be written to directly.
This will allow you to achieve full line rates on commodity network adapters,
similar to rates achieved by commercial"


# tcpdump or tcpreplay switches?
- ```-c``` number of packets
- ```-l``` number of loops
- ```-K``` "This option loads the specified pcap(s) into RAM
before starting to send in order to improve replay performance
while introducing a startup performance hit."


# System stats
```
sudo apt-get install sysstat
```


# Kafka usage
Make topics.
```
~/kafka/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic exampleTopic
~/kafka/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic instance-1-heartbeat
```

List topics.
```
~/kafka/bin/kafka-topics.sh --list --bootstrap-server localhost:9092
```

Delete topics.
```
~/kafka/bin/kafka-topics.sh --zookeeper localhost:2181 --delete --topic exampleTopic
```

Publish a message.
```
echo "beep" | ~/kafka/bin/kafka-console-producer.sh --broker-list localhost:9092 --topic instance-1-heartbeat > /dev/null
```

Consume the message in another session.
```
~/kafka/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic instance-1-heartbeat --from-beginning
```
