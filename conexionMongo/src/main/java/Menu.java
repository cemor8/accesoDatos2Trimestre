import com.mongodb.client.FindIterable;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;
import com.mongodb.client.model.Filters;
import com.mongodb.client.model.Updates;
import org.bson.Document;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Menu {
    private ArrayList<Libro> libros = new ArrayList<>();
    Map<String, String> columnasExpresiones = new HashMap<String, String>() {
        {
            put("fecha", "^(0[1-9]|[12][0-9]|3[01])[-/](0[1-9]|1[012])[-/](19|20)\\d\\d$");
            put("nombre", "^[\\w\\s.,!?-]{1,100}$");
            put("paginas","^\\d{1,5}$" );
            put("autor","^(?=.*[a-z])(?=.*[A-Z]).{4,30}$");
        }

    };
    private static final Logger logger = LoggerFactory.getLogger(Conexion.class);
    /**
     * Método que muestra el menú del programa por terminal
     * */
    public void mostrarMenu(){

        Integer opcion = null;
        while (opcion == null){
            Scanner opcionIN = new Scanner(System.in);
            System.out.println("\n");
            System.out.println("1. Crear Libro");
            System.out.println("2. Mostrar Libros");
            System.out.println("3. Eliminar Libros");
            System.out.println("4. Modificar Libros");
            System.out.println("5. Salir");
            System.out.println("\n");
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
                    this.mostrarLibros();
                    opcion = null;
                    break;
                case 3:
                    this.borrarLibro();
                    opcion = null;
                    break;
                case 4:
                    this.modificarLibro();
                    opcion = null;
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
     * Método que crea un libro en la base de datos, pide los datos por terminal y luego
     * los introduce como un documento en la coleccion de libros.
     * */
    public void crearLibro(){
        String nombreLibro = this.devolverString("Introduce el nombre para el libro ", this.columnasExpresiones.get("nombre"), true);
        String nombreAutor = this.devolverString("Introduce el nombre del autor del libro ", this.columnasExpresiones.get("autor"), true);
        Integer paginas = this.devolverInteger("Cantidad de páginas",false);
        String fecha = this.devolverString("Introduce la fecha de lanzamiento",this.columnasExpresiones.get("fecha"),true);
        MongoDatabase baseDatos = Conexion.getDatabase();
        MongoCollection<Document> coleccionLibros = baseDatos.getCollection("libros");

        Document libro = new Document("titulo", nombreLibro)
                .append("autor", nombreAutor)
                .append("paginas", paginas)
                .append("fecha", fecha);

        coleccionLibros.insertOne(libro);
        Conexion.close();
    }
    /**
     * Método que recibe los libros de la base de datos y crea objetos Libros
     * con estos documentos
     * */
    public void recibirLibros(){
        MongoDatabase baseDatos = Conexion.getDatabase();
        MongoCollection<Document> coleccionLibros = baseDatos.getCollection("libros");
        FindIterable<Document> documentos = coleccionLibros.find();
        Document primerDocumento = documentos.first();
        this.libros = new ArrayList<>();
        if (primerDocumento == null) {
            return;
        }
        for (Document documento : documentos) {
            String titulo = documento.getString("titulo");
            String autor = documento.getString("autor");
            Integer pags = documento.getInteger("paginas");
            String fecha = documento.getString("fecha");
            this.libros.add(new Libro(titulo,autor,pags,fecha));
        }
        Conexion.close();
    }
    /**
     * Método que muestra los libros por terminal
     * */
    public void mostrarLibros(){
        this.recibirLibros();
        if(this.libros.isEmpty()){
            System.out.println("No hay libros");
            return;
        }
        System.out.println("***************");
        System.out.println("\n");
        for (Libro libro : libros){
            System.out.println(libro);
            System.out.println("\n");
        }
        System.out.println("\n");
        System.out.println("***************");
    }


    /**
     * Método que modifica un libro, se conecta a la base de datos y obtiene la coleccion de libros,
     * luego busca un libro con el titulo que se ha pedido por terminal, si no encuentra ninguno lo indica,
     * pide un nuevo titulo para el libro, si ese titulo ya existe, lo indica, si no existe y es válido, pide
     * los demas datos para modificar el libro.
     * */
    public void modificarLibro(){
        this.recibirLibros();
        MongoDatabase baseDatos = Conexion.getDatabase();
        MongoCollection<Document> collection = baseDatos.getCollection("libros");
        String nombreLibro = this.devolverString("Introduce el titulo del libro a modificar ", this.columnasExpresiones.get("nombre"), true);
        FindIterable<Document> documento = collection.find(new Document("titulo", nombreLibro));
        Document document = documento.first();
        if (document == null) {
            System.out.println("No se encontró ningún documento con ese nombre.");
            return;
        }
        Object idActual = document.get("titulo");

        String nuevoNombre = this.devolverString("Introduce el nuevo nombre del libro ", this.columnasExpresiones.get("nombre"), true);
        FindIterable<Document> documentoConNuevoNombre = collection.find(new Document("titulo", nuevoNombre));
        Document otroDocumento = documentoConNuevoNombre.first();

        if (otroDocumento != null && !otroDocumento.get("titulo").equals(idActual)) {
            System.out.println("Ya existe otro libro con el nuevo nombre proporcionado.");
            return;
        }
        String nombreAutor = this.devolverString("Introduce el nombre del autor del libro ", this.columnasExpresiones.get("nombre"), true);

        Integer paginas = this.devolverInteger("Cantidad de páginas",false);
        String fecha = this.devolverString("Introduce la fecha de lanzamiento",this.columnasExpresiones.get("fecha"),true);


        collection.updateOne(Filters.eq("titulo", nombreLibro),Updates.set("paginas", paginas));
        collection.updateOne(Filters.eq("titulo", nombreLibro),Updates.set("fecha", fecha));
        collection.updateOne(Filters.eq("titulo", nombreLibro),Updates.set("autor", nombreAutor));
        collection.updateOne(Filters.eq("titulo", nombreLibro),Updates.set("titulo", nuevoNombre));
        Conexion.close();

    }
    /**
     * Método que se encarga de borrar un libro en una lisa de libros, muestra todos los libros por terminal
     * seguidos de un numero, pide el numero correspondiente al libro por terminal para ser eliminado, cuando es introducido
     * y este es válido, lo elimina.
     * */
    public void borrarLibro(){
        this.recibirLibros();
        MongoDatabase baseDatos = Conexion.getDatabase();
        MongoCollection<Document> coleccionLibros = baseDatos.getCollection("libros");
        FindIterable<Document> documentos = coleccionLibros.find();
        ArrayList<Document> listaDocumentos = new ArrayList<>();
        Document primerDocumento = documentos.first();

        if (primerDocumento == null) {
            System.out.println("No hay libros");
            return;
        }

        int index = 0;
        for (Document cada_documento : documentos) {
            listaDocumentos.add(cada_documento);
            System.out.println((index+1) + ": " + this.libros.get(index));
            System.out.println("\n");
            index+=1;
        }
        Integer posicionDocumento= this.devolverInteger("Introduce el libro a borrar",true);
        posicionDocumento-=1;
        if (posicionDocumento >= 0 && posicionDocumento < listaDocumentos.size()) {
            Document documento = listaDocumentos.get(posicionDocumento);

            if (documento != null) {

                if (coleccionLibros.deleteOne(documento).getDeletedCount() > 0) {
                    System.out.println("El libro ha sido borrado con éxito.");
                } else {
                    System.out.println("No se encontró ningún libro con ese título.");
                }

            } else {
                System.out.println("El documento en la posición indicada es null.");
            }
        } else {
            System.out.println("Libro no encontrado o índice fuera de rango.");
        }
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
    public Integer devolverInteger(String texto, boolean posicion) {
        Integer integerDevolver = null;
        while (integerDevolver == null) {
            System.out.println(texto);
            Scanner integerDevolverIn = new Scanner(System.in);
            try {
                integerDevolver = integerDevolverIn.nextInt();
                if(integerDevolver <=0 && !posicion){
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
