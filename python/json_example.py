import json

# 1. Create a Python data structure (a dictionary)
user_data = {
    "name": "Mario",
    "id": 123
}

# 2. SERIALIZATION to a JSON string
# json.dumps() converts the dictionary to a JSON string
json_string = json.dumps(user_data)
print("JSON Serialized (string): " + json_string)
print("Length in bytes: " + str(len(json_string.encode('utf-8'))))

# 3. DESERIALIZATION from the JSON string
# json.loads() converts the JSON string to a Python dictionary
deserialized_user_data = json.loads(json_string)
print("Deserialized Dictionary:")
print(deserialized_user_data)
print("Name: " + deserialized_user_data['name'])
