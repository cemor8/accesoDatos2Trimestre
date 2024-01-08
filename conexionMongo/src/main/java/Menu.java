import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;
import org.bson.Document;

import java.util.Collections;
import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Menu {
    Map<String, String> columnasExpresiones = new HashMap<String, String>() {
        {
            put("fecha", "^(0[1-9]|[12][0-9]|3[01])[-/](0[1-9]|1[012])[-/](19|20)\\d\\d$");
            put("nombre", "^.{1,30}$");
        }

    };
    public void mostrarMenu(){

        Integer opcion = null;
        while (opcion == null){
            Scanner opcionIN = new Scanner(System.in);
            System.out.println("1. Crear Libro");
            System.out.println("2. Mostrar Libros");
            System.out.println("3. Eliminar Libros");
            System.out.println("4. Modificar Libros");
            System.out.println("5. Salir");
            try {
                opcion = opcionIN.nextInt();

            }catch (Exception err){
                System.out.println(err.getMessage());
                continue;
            }

            switch (opcion){
                case 1:
                    this.crearLibro();
                    opcion = null;
                    break;
                case 2:
                    this.opcionesRanking();
                    opcion = null;
                    break;
                case 3:
                    this.jugar();
                    this.obtenerClasificaciones();
                    opcion = null;
                    break;
                case 4:
                    this.borrarCuenta();
                    break;
                case 5:
                    System.exit(0);
                    break;
                default:
                    System.out.println("Opcion Inválida");
                    opcion = null;
                    break;
            }
        }
    }

    /**
     * Método que crea un libro en la base de datos, pide los datos por terminal.
     * */
    public void crearLibro(){
        String nombreLibro = this.devolverString("Introduce el nombre para el libro ", this.columnasExpresiones.get("nombre"), true);
        String nombreAutor = this.devolverString("Introduce el nombre del autor del libro ", this.columnasExpresiones.get("nombre"), true);
        Integer paginas = this.devolverInteger("Cantidad de páginas");
        String fecha = this.devolverString("Introduce la fecha de lanzamiento",this.columnasExpresiones.get("fecha"),true);
        MongoDatabase baseDatos = Conexion.getDatabase();
        MongoCollection<Document> coleccionLibros = baseDatos.getCollection("libros");

        Document libro = new Document("nombre", nombreLibro)
                .append("autor", nombreAutor)
                .append("numeroDePaginas", paginas)
                .append("fechaDeLanzamiento", fecha);

        coleccionLibros.insertOne(libro);
        Conexion.close();
    }


    /**
     * Método que pide una string por pantalla, si hay patron comprueba que el
     * texto cumpla los requisitos, pero si el texto introducido es null continua, aun que si
     * el texto introducido es null pero requerido es true, no valdra y tendras que cumplir los requisitos
     *
     * @param patron    expresion regular a validar
     * @param texto     texto a mostrar por pantalla
     * @param requerido si es texto debe cumplir los requisitos si este es null.
     */
    public String devolverString(String texto, String patron, boolean requerido) {
        String stringDevolver = null;
        while (stringDevolver == null) {
            System.out.println(texto);
            Scanner stringDevolverIn = new Scanner(System.in);
            try {
                stringDevolver = stringDevolverIn.nextLine();
                if (requerido && patron != null && !validarDatos(patron, stringDevolver)) {
                    throw new Exception("Contenido invalido");
                } else if ((patron != null && !validarDatos(patron, stringDevolver)) && !stringDevolver.equalsIgnoreCase("null")) {
                    throw new Exception("Contenido invalido");
                }
            } catch (Exception err) {
                System.out.println("Contenido inválido");
                stringDevolver = null;
            }
        }
        return stringDevolver;
    }
    /**
     * Método que pide un integer por terminal y lo devuelve.
     *
     * @param texto string a mostrar por pantalla
     */
    public Integer devolverInteger(String texto) {
        Integer integerDevolver = null;
        while (integerDevolver == null) {
            System.out.println(texto);
            Scanner integerDevolverIn = new Scanner(System.in);
            try {
                integerDevolver = integerDevolverIn.nextInt();
                if(integerDevolver <=0){
                    throw  new Exception("error");
                }

            } catch (Exception err) {
                System.out.println("Opcion inválida");
                integerDevolver = null;
            }
        }
        return integerDevolver;
    }

    /**
     * Método que se encarga de validar los datos para que se cumpla la
     * expresion regular.
     *
     * @param patronCumplir patron a cumplir
     * @param textoBuscar   string donde buscar el patron
     */
    public boolean validarDatos(String patronCumplir, String textoBuscar) {
        Pattern patron = Pattern.compile(patronCumplir);
        Matcher matcher = patron.matcher(textoBuscar);
        return matcher.matches();
    }
}
