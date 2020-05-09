
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
