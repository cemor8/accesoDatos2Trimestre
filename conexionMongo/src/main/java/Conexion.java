import com.mongodb.client.MongoClients;
import com.mongodb.client.MongoClient;
import com.mongodb.client.MongoDatabase;

public class Conexion {

    private static MongoClient mongoClient = null;
    private static MongoDatabase database = null;

    public static MongoDatabase getDatabase() {
        if (mongoClient == null) {
            // me conecto al puerto de la base de datos

            mongoClient = MongoClients.create("mongodb://localhost:27017");

            // En mongo, la base de datos se crea sin necesidad de especificarlo si el nombre no existe
            database = mongoClient.getDatabase("Biblioteca");
        }
        return database;
    }

    public static void close() {
        if (mongoClient != null) {
            mongoClient.close();
            mongoClient = null;
        }
    }
}
