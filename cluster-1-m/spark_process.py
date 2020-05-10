'''
Have to deal with multiple lines, whihc are part of same packet.
Identified by newline and spaces, so try something with:
.replace('\n    ', ' ')
'''

from pyspark import SparkConf
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from packet_parse import PacketParse
from time import sleep

'''
conf = SparkConf()
conf.setMaster('yarn-client')
conf.setAppName(app_name)
sc = SparkContext(conf=conf)
ref: https://docs.anaconda.com/anaconda-scale/howto/spark-yarn/

and/or this on run in command line:
./spark-submit --master yarn-cluster --queue default \
--num-executors 20 --executor-memory 1G --executor-cores 3 \
--driver-memory 1G \
--conf spark.yarn.appMasterEnv.SPARK_HOME=/dev/null \
--conf spark.executorEnv.SPARK_HOME=/dev/null \
--files  /home/user/script.py

conf = pyspark.SparkConf()
conf.setMaster('spark://head_node:56887')
conf.set('spark.authenticate', True)
conf.set('spark.authenticate.secret', 'secret-key')
sc = SparkContext(conf=conf)
'''

app_name = 'PCAP-processing'
# Create StreamingContext with ...
sc = SparkContext('local[*]', app_name)
ssc = StreamingContext(sc, 1) # batch interval of N second

host_ip = '10.150.0.6'
host_port = 4444

# Create a dstream connected to host
strm = ssc.socketTextStream(host_ip, host_port)

#strm = strm. # One packet has multiple lines. Like, if line startswith '\n    ', concat with previous line

# Get packet parser and run on stream
p_parse = PacketParse()
p_parse.set_regex()
values = strm.map(p_parse.get_values)

values.pprint()

#here
'''
file:///C:/Users/joberlin/Downloads/15_python.html
cassandra spark connector
df.write \
    .format("org.apache.spark.sql.cassandra") \
    .mode('append') \
    .options(table='kv', keyspace='test') \
    .save()

'''

ssc.start()
ssc.awaitTermination()
#sleep(10)
#ssc.stop()
