import faust

# Step 1: Application configuration
# Define the Faust app with a unique ID and the Kafka brokers
app = faust.App(
    'error-filter-app',
    broker='kafka://localhost:9092',
)

# Step 2: Define the input and output topics
# Define the topic schemas (in this case, just strings)
input_topic = app.topic('input-topic', value_type=str)
output_topic = app.topic('output-topic', value_type=str)

# Step 3: Define the stream processing logic using a Faust agent


@app.agent(input_topic)
async def process_messages(messages):
  # This is the processing loop that reads from the input topic
  async for message in messages:
    # Step 4: Define the business logic (the filter)
    if 'error' in message:
      print(f"Filtering message: {message}")
      # Step 5: Send the result to the output topic
      await output_topic.send(value=message)

# To run the app, use this command in your terminal:
# faust -A faust_example worker -l info
