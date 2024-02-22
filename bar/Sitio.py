class Sitio: 
    def __init__(self,nombre,ocupado):
        self._nombre = nombre
        self._ocupado = ocupado
        
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