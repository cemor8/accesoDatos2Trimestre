from Sitio import Sitio
class Mesa:
    def __init__(self, nombre_mesa, ocupada, ubicacion, capacidad,sitios):
        self._nombre_mesa = nombre_mesa
        self._ocupada = ocupada
        self._ubicacion = ubicacion
        self._capacidad = capacidad
        self._sitios = sitios

    @property
    def nombre_mesa(self):
        return self._nombre_mesa

    @nombre_mesa.setter
    def nombre_mesa(self, valor):
        self._nombre_mesa = valor

    @property
    def ocupada(self):
        return self._ocupada

    @ocupada.setter
    def ocupada(self, valor):
        if isinstance(valor, bool):
            self._ocupada = valor
        else:
            raise ValueError("El ocupada debe ser un valor booleano.")

    @property
    def ubicacion(self):
        return self._ubicacion

    @ubicacion.setter
    def ubicacion(self, valor):
        if valor in ["terraza", "interior", "barra"]:
            self._ubicacion = valor
        else:
            raise ValueError("Ubicación no válida. Debe ser 'terraza', 'interior' o 'barra'.")

    @property
    def capacidad(self):
        return self._capacidad

    @capacidad.setter
    def capacidad(self, valor):
        if isinstance(valor, int) and valor > 0:
            self._capacidad = valor
        else:
            raise ValueError("La capacidad debe ser un número entero positivo.")
    @property
    def sitios(self):
        return self._sitios
    @sitios.setter
    def sitios(self, valor):
        self._sitios = valor
        
    def to_dict(self):
        return {"nombre_mesa" : self._nombre_mesa, "ocupada" : self._ocupada, "ubicacion" : self._ubicacion, "capacidad" : self._capacidad, "sitios" : [sitio.to_dict() for sitio in self._sitios] }

    def __str__(self):
        return (f"Mesa: {self.nombre_mesa}, "
                f"Ocupada: {self.ocupada}, "
                f"Ubicación: {self.ubicacion}, "
                f"Capacidad: {self.capacidad} personas")