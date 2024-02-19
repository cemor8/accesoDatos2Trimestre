class Mesa:
    def __init__(self, nombre_mesa, estado, ubicacion, capacidad):
        self.nombre_mesa = nombre_mesa
        self.estado = estado
        self.ubicacion = ubicacion
        self.capacidad = capacidad

    @property
    def nombre_mesa(self):
        return self._nombre_mesa

    @nombre_mesa.setter
    def nombre_mesa(self, valor):
        self._nombre_mesa = valor

    @property
    def estado(self):
        return self._estado

    @estado.setter
    def estado(self, valor):
        if isinstance(valor, bool):
            self._estado = valor
        else:
            raise ValueError("El estado debe ser un valor booleano.")

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

    def __str__(self):
        estado_str = "Ocupada" if self.estado else "Libre"
        return (f"Mesa: {self.nombre_mesa}, "
                f"Estado: {estado_str}, "
                f"Ubicación: {self.ubicacion}, "
                f"Capacidad: {self.capacidad} personas")