class MenuComprar:
    def __init__(self, primero, segundo, bebida, dia, precio):
        self._primero = primero
        self._segundo = segundo
        self._bebida = bebida
        self._dia = dia
        self._precio = precio

    @property
    def primero(self):
        return self._primero

    @primero.setter
    def primero(self, valor):
        self._primero = valor

    @property
    def segundo(self):
        return self._segundo

    @segundo.setter
    def segundo(self, valor):
        self._segundo = valor

    @property
    def bebida(self):
        return self._bebida

    @bebida.setter
    def bebida(self, valor):
        self._bebida = valor

    @property
    def dia(self):
        return self._dia

    @dia.setter
    def dia(self, valor):
        self._dia = valor

    @property
    def precio(self):
        return self._precio

    @precio.setter
    def precio(self, valor):
        self._precio = valor

    def to_dict(self):
        return {
            "primero": self._primero,
            "segundo": self._segundo,
            "bebida": self._bebida,
            "dia": self._dia,
            "precio": self._precio,
        }

    def __str__(self):
        return f"MenuComprar(primero={self._primero}, segundo={self._segundo}, bebida={self._bebida}, dia={self._dia}, precio={self._precio})"