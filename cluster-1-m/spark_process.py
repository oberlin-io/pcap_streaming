
from pyspark import SparkConf
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
#from pyspark.sql import SQLContext
from packet_parse import PacketParse
from time import sleep

app_name = 'PCAP-processing'
# Create StreamingContext with ...
sc = SparkContext('local[*]', app_name)
ssc = StreamingContext(sc, 1) # batch interval of N second
#sqlContext = SQLContext(sc)

# Adding open bracket to the json output file.
# Need to manually add the closing bracket
with open('parsed.json', 'w') as f: f.write('[\n')


host_ip = '10.150.0.6'
host_port = 4444

# Create a dstream connected to host
strm = ssc.socketTextStream(host_ip, host_port)

'''
If tcpdump is -v or higher verbosity, then
have to deal with multiple lines, which are part of same packet.
Identified by newline and spaces, so try something with:
.replace('\n    ', ' ')
'''

# Get packet parser and run on stream
p_parse = PacketParse()
p_parse.set_regex()
values = strm.map(p_parse.get_values)

values.pprint()

'''
def write(rdd):
    if not rdd.isEmpty():
        #rdd.toDF().write.save("parsed.json", format="json", mode="append") 
        #with open('parsed.json', 'a') as f:
        #    f.write(rdd.encode('utf-8'))
        rdd.saveAsTextFile('parsed.txt', )
values.foreachRDD(write)
'''


import json
def write(rdd):
    if not rdd.isEmpty():
        jrdd = rdd.map(json.dumps)
        jstr = jrdd.reduce(lambda x, y: x + ",\n" + y)
        with open("parsed.json", "a") as f:
            f.write(jstr.encode("utf-8"))

values.foreachRDD(write)


ssc.start()
ssc.awaitTermination()


