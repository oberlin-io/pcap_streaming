import os; import time

topic = 'instance-1-heartbeat'
local_host = '9092'
freq = 4 # seconds

pub = '| ~/kafka/bin/kafka-console-producer.sh \
--broker-list localhost:{} \
--topic {} > /dev/null'.format(local_host, topic)

pub = 'echo "{}" ' + pub

while True:
    d = os.popen('date').read()[:-1]
    msg = '{}: beep'.format(d)
    pub_ = pub.format(msg)

    try:
        os.system(pub_)
        time.sleep(freq)

    except Exception as e:
        print(d + ': ' + e)
        exit()
