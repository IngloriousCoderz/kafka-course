public

import org.apache.avro.Schema;
import org.apache.avro.generic.GenericData;
import org.apache.avro.generic.GenericRecord;
import org.apache.avro.io.DatumReader;
import org.apache.avro.io.DatumWriter;
import org.apache.avro.io.Encoder;
import org.apache.avro.io.Decoder;
import org.apache.avro.io.BinaryEncoder;
import org.apache.avro.io.BinaryDecoder;
import org.apache.avro.specific.SpecificDatumReader;
import org.apache.avro.specific.SpecificDatumWriter;
import java.io.ByteArrayOutputStream;
import java.io.ByteArrayInputStream;

public class AvroExample {

  public static void main(String[] args) throws Exception {
    // 1. Schema definition (here as a string for simplicity)
    String schemaStr = "{"
        + "\"type\": \"record\","
        + "\"name\": \"User\","
        + "\"fields\": ["
        + "{\"name\": \"name\", \"type\": \"string\"},"
        + "{\"name\": \"id\", \"type\": \"int\"}"
        + "]"
        + "}";
    Schema schema = new Schema.Parser().parse(schemaStr);
    // This is how you would parse the schema in production:
    // Schema schema = new Schema.Parser().parse(new File("User.avsc"));

    // 2. CREATION of a data object (GenericRecord)
    GenericRecord user = new GenericData.Record(schema);
    user.put("name", "Mario");
    user.put("id", 123);

    // 3. SERIALIZATION into a byte array
    DatumWriter<GenericRecord> datumWriter = new SpecificDatumWriter<>(schema);
    ByteArrayOutputStream outputStream = new ByteArrayOutputStream();
    Encoder encoder = new BinaryEncoder(outputStream);
    datumWriter.write(user, encoder);
    encoder.flush();
    byte[] avroBytes = outputStream.toByteArray();
    outputStream.close();

    System.out.println("Avro Serialized (bytes): " + avroBytes.length + " bytes");

    // 4. DESERIALIZATION of the byte array
    DatumReader<GenericRecord> datumReader = new SpecificDatumReader<>(schema);
    ByteArrayInputStream inputStream = new ByteArrayInputStream(avroBytes);
    Decoder decoder = new BinaryDecoder(inputStream);
    GenericRecord deserializedUser = datumReader.read(null, decoder);
    inputStream.close();

    System.out.println("Nome Deserialized: " + deserializedUser.get("name"));
  }
}

// Avro schemas usually allow to auto-generate classes:
class User extends SpecificRecordBase {
  public String name;
  public int id;

  // Constructor and methods for schema, get, put, etc. would be generated
  public Schema getSchema() {
    String schemaStr = "{"
        + "\"type\": \"record\","
        + "\"name\": \"User\","
        + "\"fields\": ["
        + "{\"name\": \"name\", \"type\": \"string\"},"
        + "{\"name\": \"id\", \"type\": \"int\"}"
        + "]"
        + "}";
    return new Schema.Parser().parse(schemaStr);
  }

  public Object get(int field) {
    switch (field) {
      case 0:
        return name;
      case 1:
        return id;
      default:
        throw new org.apache.avro.AvroRuntimeException("Bad index");
    }
  }

  public void put(int field, Object value) {
    switch (field) {
      case 0:
        name = (String) value;
        break;
      case 1:
        id = (Integer) value;
        break;
      default:
        throw new org.apache.avro.AvroRuntimeException("Bad index");
    }
  }
}
