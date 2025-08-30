from confluent_kafka import Consumer, KafkaException, KafkaError
import sys
import argparse
import time

# Function to read all messages from the beginning of the topic


def run_historical_consumer(topic_name, bootstrap_servers):
  """
  A consumer that reads all available messages from the beginning of the topic
  using a unique group ID.
  """
  # Use a unique group ID to ensure it's treated as a new consumer group
  # A new group will always start from 'earliest'
  conf = {
      'bootstrap.servers': bootstrap_servers,
      'group.id': f'historical-reader-{int(time.time())}',
      'auto.offset.reset': 'earliest',
      'enable.auto.commit': False
  }

  consumer = Consumer(conf)
  consumer.subscribe([topic_name])

  print("Starting historical consumer. Reading all previous messages...")

  try:
    while True:
      msg = consumer.poll(1.0)

      if msg is None:
        print("End of historical messages. Exiting historical mode.")
        break

      if msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF:
          print(
              f"Reached end of partition {msg.partition()}. Waiting for new messages.")
          # In a real app, you would stop here or transition to a different mode.
        else:
          raise KafkaException(msg.error())

      print(
          f"Consumed historical message from partition {msg.partition()}: key={msg.key().decode('utf-8')}, value={msg.value().decode('utf-8')}")
      consumer.commit(asynchronous=False)

  except KeyboardInterrupt:
    print("Stopping historical consumer...")
  finally:
    consumer.close()

# Function to read messages in real-time with the main group


def run_realtime_consumer(topic_name, bootstrap_servers, group_id):
  """
  A consumer that reads new messages as they arrive, as part of the main group.
  """
  conf = {
      'bootstrap.servers': bootstrap_servers,
      'group.id': group_id,
      'auto.offset.reset': 'earliest',
      'enable.auto.commit': False
  }

  consumer = Consumer(conf)
  consumer.subscribe([topic_name])

  print(
      f"Starting real-time consumer for group '{group_id}'. Waiting for new messages...")

  try:
    while True:
      msg = consumer.poll(1.0)

      if msg is None:
        continue

      if msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF:
          sys.stderr.write('%% %s [%d] reached end of offset %s\n' %
                           (msg.topic(), msg.partition(), msg.offset()))
          continue
        else:
          raise KafkaException(msg.error())

      print(
          f"Consumed real-time message from partition {msg.partition()}: "
          f"key={msg.key().decode('utf-8')}, value={msg.value().decode('utf-8')}")

      consumer.commit(asynchronous=False)
      print("Offsets manually committed.")

  except KeyboardInterrupt:
    print("Stopping real-time consumer...")
  finally:
    consumer.close()


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Kafka Consumer')
  parser.add_argument('--mode', type=str, default='realtime', choices=['realtime', 'historical'],
                      help='Choose consumer mode: historical (reads all messages) or realtime (joins the main group)')

  args = parser.parse_args()

  # Configuration for your Kafka broker
  topic_name = 'my_first_topic'
  bootstrap_servers = 'localhost:9092'
  group_id = 'my_first_consumer_group_python'

  if args.mode == 'historical':
    run_historical_consumer(topic_name, bootstrap_servers)
  else:
    run_realtime_consumer(topic_name, bootstrap_servers, group_id)

# How to Use and Test
#
# 1. ** Produce Messages**: First, make sure you have some messages in your `my_first_topic`. You can use the `producer.py` file we've already created.
# 2. ** Simulate a New User Catching Up**: In a terminal, run the consumer with the `historical` mode.
# ```bash
# python consumer.py - -mode historical
# ```
# This will start a new consumer that will read all the messages from the beginning, as you'd expect from a new user joining.
#
# 3. ** Simulate Real-Time Consumption**: Once a user has "caught up," your application would then switch to the real-time mode. You can test this by opening a new terminal and running:
#  ```bash
#  python consumer.py - -mode realtime
