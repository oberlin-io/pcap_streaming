<!--
1. Collect requirements by outlining here

## Requirements

-->

# x
Keywords:
- x

## Abstract
<!--
real-time netflow analytics for cybersecurity
anomaly-based intrusion detection
text analytics, NLP (natural language processing)
unstructured data
attack vectors addressed
streaming data services
outcome/goal: detecting
or goal: PCAP processing with Kafka and Storm
flow vs PCAP

Considering scoping project to PCAP processing

1. Network sniffer, which we're not implementing, but simulating by rerunning
PCAP files.
1. PCAP data sent via Kafka to
1. Storm cluster, with Python library scapy, transforms, filters, and loads to
1. Storm analysis, such as NLP [? consider leaving this to last]
1. MongoDB or Cassandra on HDFS storage
1. Reporting and visualization

Producer machine
Pipe tshark output JSON (for us, simulated) to netcat on port x,
then netcat listening on port x, piped to Kafka producer script
```
shell1> nc -l 8888 | ./producer.sh
shell2> sudo tshark -l | nc 127.1 8888
```
tshark -l deals with buffering

Or use a named pipe
```
shell1> mkfifo tsharkpipe
shell1> tail -f -c +0 tsharkpipe | producer.sh
shell2> sudo tshark -l > tsharkpipe
```

Use scapy to replay the PCAP file.

Consumer machine
Consumer script ingests
Storm for PCAP processing (parse, reduce, filter, stats, model)

Store in HDFS via MongoDB

-->

## Relevancy to big data
<!--network flow and the Vs, supporting data services-->

## Stack architecture
<!--![stack](img/stack.png)-->
### Data capture

### Message service / data ingestion
Kafka

### Processing
Apache Storm
<!--rolling window-->

### Storage
HDFS (Hadoop distributed filesystem)

### Database <!--and querying-->
MongoDB or Cassandra [?choose]. Cassandra due to high availability
"It has multiple master nodes in a cluster. Because of these multiple nodes, if one goes down, another takes its place."
Whereas "In MongoDB, there is only one master node in a cluster. This master node control a number of slave nodes. During a failure, when the master node goes down, one of the slave nodes is elected as master. This process takes about 10 to 30 seconds. During this delay time, the cluster is down and cannot take any input."
As data types must be defined in Cassandra, and MOngoDB is scheemaless,
PCAP variables should be known beforehand. No need for scheemaless essentially.
Query language or CQL is very similar to SQL, so analysts should be
at ease with ad-hoc queries on Cassandra.

### Reporting
Python Pandas [?nec]

### Visualization
D3.js [best for realtime?]. Open source, web standards,, mobile version

## Network topology
<!--![topology](img/topology.png)-->

## Data simulation
<!--
datasets

http://205.174.165.80/CICDataset/CIC-IDS-2017/Dataset/
> GeneratedLabelledFlows.zip
This is already processed PCAPs and its resolution is only minutes.

http://205.174.165.80/CICDataset/CIC-IDS-2017/Dataset/PCAPs/
> Friday-WorkingHours.pcap

http://205.174.165.80/CICDataset/CIC-IDS-2017/Dataset/PCAPs/Friday-WorkingHours.pcap

-->

## tshark
Wireshark, network protocol sniffer and analyzer
```
apt-get install tshark
```



## Protocol numbers
https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xml

## References
-  Radford. Network Traffic Anomaly Detection Using Recurrent Neural Networks.
28 Mar 2018.
url: https://arxiv.org/pdf/1803.10769.pdf
- Intrusion Detection Evaluation Dataset (CICIDS2017).
University of New Brunswick: Canadian Institute for Cybersecurity.
url: https://www.unb.ca/cic/datasets/ids-2017.html
- Iman Sharafaldin, Arash Habibi Lashkari, and Ali A. Ghorbani.
"Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization".
4th International Conference on Information Systems Security and Privacy (ICISSP),
Portugal, January 2018.
