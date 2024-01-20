import java.io.Serializable;

public class Libro implements Serializable{
    private String titulo;
    private String autor;
    private Integer paginas;
    private String fecha;

    public Libro(String titulo, String autor, Integer paginas, String fecha) {
        this.titulo = titulo;
        this.autor = autor;
        this.paginas = paginas;
        this.fecha = fecha;
    }

    public String getTitulo() {
        return titulo;
    }

    public String getAutor() {
        return autor;
    }

    public Integer getPaginas() {
        return paginas;
    }

    public String getFecha() {
        return fecha;
    }

    public void setTitulo(String titulo) {
        this.titulo = titulo;
    }

    public void setAutor(String autor) {
        this.autor = autor;
    }

    public void setPaginas(Integer paginas) {
        this.paginas = paginas;
    }

    public void setFecha(String fecha) {
        this.fecha = fecha;
    }

    @Override
    public String toString() {
        return " Titulo: " + titulo +"\n"+
                " Autor: " + autor +"\n"+
                " Páginas: " + paginas +"\n"+
                " Fecha: " + fecha;
    }
}
