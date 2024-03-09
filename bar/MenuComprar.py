from Consumicion import Consumicion
class MenuComprar:
    def __init__(self, primero, segundo, bebida, dia, precio, cantidad):
        self._primero = primero
        self._segundo = segundo
        self._bebida = bebida
        self._dia = dia
        self._precio = precio
        self._cantidad = cantidad

    @classmethod
    def from_dict(cls, dict_data):
        primero = dict_data.get('primero')
        primero = Consumicion.from_dict(primero)
        segundo = dict_data.get('segundo')
        segundo = Consumicion.from_dict(segundo)
        bebida = dict_data.get('bebida')
        bebida = Consumicion.from_dict(bebida)
        return cls(
            primero=primero,
            segundo=segundo,
            bebida=bebida,
            dia=dict_data.get('dia', ''),
            precio=dict_data.get('precio', 0),
            cantidad=dict_data.get('cantidad', 0)
        )
    @property
    def cantidad(self):
        return self._cantidad

    @cantidad.setter
    def cantidad(self, valor):
        self._cantidad = valor
    
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
            "cantidad": self._cantidad
        }

    def __str__(self):
        return (
            "Menú:\n"
            f"      Primero: {self._primero}\n"
            f"      Segundo: {self._segundo}\n"
            f"      Bebida: {self._bebida}\n"
            f"    Precio: {self._precio}\n"
            f"    Cantidad: {self._cantidad}\n"
        )