import com.mongodb.client.MongoClients;
import com.mongodb.client.MongoClient;
import com.mongodb.client.MongoDatabase;

public class Main {
    public static void main(String[] args) {
        MongoClient mongoClient = MongoClients.create("mongodb://localhost:27017");


        MongoDatabase database = mongoClient.getDatabase("Biblioteca");

        // Realizar operaciones con la base de datos aquí
        // Por ejemplo, obtener una colección, insertar documentos, etc.

        // Cerrar la conexión con la base de datos al final
        mongoClient.close();
    }
}
