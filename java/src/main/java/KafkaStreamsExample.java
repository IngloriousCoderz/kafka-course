import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.streams.KafkaStreams;
import org.apache.kafka.streams.StreamsBuilder;
import org.apache.kafka.streams.StreamsConfig;
import org.apache.kafka.streams.kstream.KStream;

import java.util.Properties;

public class KafkaStreamsExample {

  public static void main(final String[] args) {
    // Step 1: Application configuration
    Properties props = new Properties();
    props.put(StreamsConfig.APPLICATION_ID_CONFIG, "streams-simple-filter");
    props.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
    props.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG, Serdes.String().getClass());
    props.put(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG, Serdes.String().getClass());

    // Step 2: Create the topology (the processing "flow")
    final StreamsBuilder builder = new StreamsBuilder();
    KStream<String, String> sourceStream = builder.stream("input-topic");

    // Step 3: Define the business logic
    KStream<String, String> errorStream = sourceStream.filter((key, value) -> value.contains("error"));

    // Step 4: Send the result to an output topic
    errorStream.to("output-topic");

    // Step 5: Build and start the application
    final KafkaStreams streams = new KafkaStreams(builder.build(), props);
    streams.start();

    // Step 6: Add a shutdown hook to close the application cleanly
    Runtime.getRuntime().addShutdownHook(new Thread(streams::close));
  }
}
