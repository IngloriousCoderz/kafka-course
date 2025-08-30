# How many partitions should I create?

First, estimate the maximum number of messages you'll need to process per second.

- Producer Throughput (P): Determine how many messages your producers can generate per second.
- Consumer Throughput (C): Determine how many messages a single consumer can process per second.

Your number of partitions needs to accommodate both your producer and consumer capacity. You'll need at least P / C partitions.

For example, if your application needs to handle 1000 messages per second (P = 1000) and a single consumer can process 100 messages per second (C = 100), you would need at least 1000 / 100 = 10 partitions to keep up.

The number of partitions is fixed once a topic is created (you can add more, but you can't reduce them). For this reason, it's a best practice to over-partition.

A good starting point: Many experts recommend starting with a number of partitions that is a power of 2 (e.g., 2, 4, 8, 16, 32, etc.).

Consider your broker count: It's a good idea to have more partitions than brokers to distribute the data evenly and allow for future scaling. A common recommendation is to have at least 2 \* number of brokers partitions.

# Python Commands

```bash
python -m venv .venv
pip install confluent-kafka
pip list > requirements.txt
```

# Creating a CLUSTER_ID

The command to run is `docker run --rm confluentinc/confluent-local:7.5.0 kafka-storage random-uuid`.

# Java Commands

```bash
mvn clean package
java -jar ./target/kafka-producer-consumer-1.0-SNAPSHOT.jar
```

# Manual Commits

To commit an offset is like putting a bookmark: "I read up to this point". The consumer can auto-commit (which is the default), but for better fault-tolerance it is better to commit manually.

# New User Reads Past Messages

If a new user that enters a group chat, to allow them to read past messages we need to assign the user to a temporary group (this will make it consume all past messages), and then reassign them to the original group.

# Why Polling Instead Of Real-Time?

1. Connection Management & Scalability: With Kafka's pull model, the consumer only opens a connection when it needs to poll for data. This is an intermittent, short-lived connection. When you have thousands or even millions of consumers, the broker doesn't have to manage a persistent, open socket for each one (or face the burden of re-establishing the connection every time). This is highly efficient and scales well.

2. Resource Consumption and Cost: By pulling data in batches, the network overhead is significantly reduced. Instead of sending a tiny message for every single new chat message, the consumer fetches a handful of messages in a single request, which is far more efficient. This saves on network bandwidth and processing power.

3. Backpressure and Reliability: The consumer controls the flow. If a user's device is slow or their network connection is poor, the consumer can simply stop polling for a moment without a "down" message from the server. Once the device catches up, it can resume polling. This is a robust mechanism for handling backpressure and ensuring reliability.

# Monitoring And Logging

Kafka sends metrics through JMX. Prometheus can collect them and Grafana can show them. Kafka UI and AKHQ are ok, but they don't give historical data nor alert in case of issues.

# Geographical Distribution

One area should have one cluster. But if producers are in the US and consumers are in Europe, they need a cluster for each continent plus Kafka MirrorMaker, which should reside close to the origin cluster (so the US in our example).

In case producers and consumers are scattered between both continents, we need two MirrorMaker instances.

# Kafka Streams

It's just a Java library that connects to Kafka. It allows to retrieve, join, filter, and organize data. In Python there's Faust which does the same thing.

It's a higher-level library compared to kafka-clients, and uses kafka-clients under the hood.
