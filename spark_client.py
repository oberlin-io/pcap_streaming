from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext

'''
Make sure cluster instances are running

And first run get_cpu.py as example streaming data
Try to parse it
'''

#def datastream():
conf = SparkConf()
conf.setAppName('sys_cpu_usage')

sc = SparkContext(conf=conf)
sc.setLogLevel('ERROR')

ssc = StreamingContext(sc, 1) # interval size N seconds

# setting a checkpoint to allow RDD recovery [?]
ssc.checkpoint('checkpoint_TwitterApp')

# read data from port 9009
datastream = ssc.socketTextStream('localhost', 9009)

#return datastream
