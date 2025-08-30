from confluent_kafka import Consumer, KafkaException, KafkaError
import sys

# Configuration for your Kafka broker and consumer group
conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'my_first_consumer_group_python',
    'auto.offset.reset': 'earliest',
    # Disable automatic commit of offsets
    'enable.auto.commit': False
}

# Create a consumer instance
consumer = Consumer(conf)

# Subscribe to the topic
consumer.subscribe(['my_first_topic'])

print("Starting to consume messages...")

try:
  while True:
    # Poll for new messages every second
    msg = consumer.poll(1.0)

    if msg is None:
      continue

    if msg.error():
      # Handle any potential errors
      if msg.error().code() == KafkaError._PARTITION_EOF:
        # End of partition, this is normal and not an error
        sys.stderr.write('%% %s [%d] reached end of offset %s\n' %
                         (msg.topic(), msg.partition(), msg.offset()))
        continue
      else:
        # Other errors
        raise KafkaException(msg.error())

    # Process the message's key and value
    print(
        f"Consumed message from partition {msg.partition()}: "
        f"key={msg.key().decode('utf-8')}, value={msg.value().decode('utf-8')}")

    # Manually commit the offset of the message just processed.
    # This tells Kafka that we have successfully processed messages up to this point.
    # Using synchronous commit is a safe choice, but can be slow.
    consumer.commit(asynchronous=False)
    print("Offsets manually committed.")

except KeyboardInterrupt:
  # User interruption, graceful shutdown
  print("Stopping consumer...")

finally:
  # Close the consumer when done. This also triggers a rebalance.
  consumer.close()
