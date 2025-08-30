from confluent_kafka import Consumer, KafkaException

# Configuration for your Kafka broker and consumer group
conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'my-first-consumer-group',
    'auto.offset.reset': 'earliest'
}

# Create a consumer instance
consumer = Consumer(conf)

# Subscribe to the topic
consumer.subscribe(['my_first_topic'])

try:
    while True:
        # Poll for new messages every second
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            # Handle any potential errors
            raise KafkaException(msg.error())
        else:
            # Print the message's key and value
            print(f"Consumed message: key={msg.key().decode('utf-8')}, value={msg.value().decode('utf-8')}")
except KeyboardInterrupt:
    pass
finally:
    # Close the consumer when done
    consumer.close()