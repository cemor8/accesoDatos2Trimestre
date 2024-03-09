class Sitio: 
    def __init__(self,nombre,ocupado):
        self._nombre = nombre
        self._ocupado = ocupado
    @classmethod
    def from_dict(cls, data):
        """
        Crea una instancia de Sitio a partir de un diccionario.
        """
        return cls(
            nombre=data.get('nombre', ''), 
            ocupado=data.get('ocupado', False)
        )
    @property
    def nombre(self):
        return self._nombre

    @property
    def ocupado(self):
        return self._ocupado  
    @ocupado.setter
    def ocupado(self,valor):
        self._ocupado = valor
    @nombre.setter
    def nombre(self,valor):
        self._nombre = valor
    def to_dict(self):
        return {"nombre" : self._nombre , "ocupado" : self._ocupado}
    def __str__(self):
        ocupado_str = "Ocupado" if self._ocupado else "Disponible"
        return (
            f"Sitio:\n"
            f"    Nombre: {self._nombre}\n"
            f"    Estado: {ocupado_str}\n"
            "───────────────────────────────"
        )