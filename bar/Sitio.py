class Sitio: 
    def __init__(self,nombre,ocupado):
        self._nombre = nombre,
        self._ocupado = ocupado
        
    @property
    def nombre(self):
        return self._nombre
    @property
    def capacidad(self):
        return self._capacidad
    @property
    def ocupado(self):
        return self._ocupado  
    @ocupado.setter
    def ocupado(self,valor):
        self._ocupado = valor
    def __str__(self):
        return (f"Nombre: {self.nombre}, "
                f"Ocupado: {self.ocupado} ")