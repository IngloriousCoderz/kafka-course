import avro.schema
from avro.io import DatumWriter, DatumReader
from io import BytesIO

# 1. Define the Avro schema as a string
schema_str = """
{
    "type": "record",
    "name": "User",
    "fields": [
        {"name": "name", "type": "string"},
        {"name": "id", "type": "int"}
    ]
}
"""
schema = avro.schema.parse(schema_str)

# 2. Create a Python data structure (a dictionary)
user_data = {
    "name": "Mario",
    "id": 123
}

# 3. SERIALIZATION into a byte stream
writer = DatumWriter(schema)
bytes_writer = BytesIO()
encoder = avro.io.BinaryEncoder(bytes_writer)
writer.write(user_data, encoder)
avro_bytes = bytes_writer.getvalue()
print("Avro Serialized (bytes): " + str(len(avro_bytes)) + " bytes")

# 4. DESERIALIZATION from the byte stream
reader = DatumReader(schema)
bytes_reader = BytesIO(avro_bytes)
decoder = avro.io.BinaryDecoder(bytes_reader)
deserialized_user_data = reader.read(None, decoder)
print("Deserialized Dictionary:")
print(deserialized_user_data)
print("Name: " + deserialized_user_data['name'])
