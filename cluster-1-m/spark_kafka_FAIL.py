'''
This is failing due to Kafka connetion, if I remember correctly.
Add error output here:

'''

import os
arg = '--packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.0.2 pyspark-shell'
os.environ['PYSPARK_SUBMIT_ARGS'] = arg

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

# Set up the Spark context and the streaming context
sc = SparkContext(appName="PCAP test")
sc.setLogLevel("WARN")
ssc = StreamingContext(sc, 1)

# Connection details
host_ip = '10.150.0.6'
host_port = 9092
host = host_ip + ':' + str(host_port)
topic = 'instance-1-pcap'

# Create stream from kafka
kstm = KafkaUtils.createStream(ssc, host, 'spark-streaming', {topic:1} )

# Check stream in stdout
kstm.pprint()

ssc.start()
sleep(5)
ssc.stop(stopSparkContext=True, stopGraceFully=True)
