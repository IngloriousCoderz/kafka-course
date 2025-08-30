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

python -m venv .venv
pip install confluent-kafka
pip list > requirements.txt

# Creating a CLUSTER_ID

The command to run is `docker run --rm confluentinc/confluent-local:7.5.0 kafka-storage random-uuid`.
