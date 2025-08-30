public

import com.fasterxml.jackson.databind.ObjectMapper;

public class JsonExample {

    public static class User {
        public String name;
        public int id;

        // Contstructor, getters and setters omitted for brevity
    }

    public static void main(String[] args) throws Exception {
        ObjectMapper objectMapper = new ObjectMapper();

        // SERIALIZATION
        User user = new User();
        user.name = "Mario";
        user.id = 123;

        // The object is converted into a JSON string.
        String jsonString = objectMapper.writeValueAsString(user);
        System.out.println("JSON Serializzato: " + jsonString);

        // DESERIALIZATION
        // The JSON string is re-converted back into a User object.
        User deserializedUser = objectMapper.readValue(jsonString, User.class);
        System.out.println("Nome Deserializzato: " + deserializedUser.name);
    }
}{

}
