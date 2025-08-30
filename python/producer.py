from confluent_kafka import Producer

# Configuration for your Kafka broker
conf = {'bootstrap.servers': 'localhost:9092'}

# Create a producer instance
producer = Producer(conf)

# The topic you want to send the message to
topic_name = 'my_first_topic'

# The message you want to send
message_key = 'my-key'
message_value = 'Hello from the producer!'

# Produce the message to the topic
producer.produce(topic_name, key=message_key.encode('utf-8'), value=message_value.encode('utf-8'))

# Wait for the message to be delivered to the broker
producer.flush()

print(f"Message '{message_value}' sent to topic '{topic_name}' with key '{message_key}'.")
