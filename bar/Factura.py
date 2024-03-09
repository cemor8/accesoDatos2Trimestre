from Consumicion import Consumicion
from MenuComprar import MenuComprar
class Factura:
    def __init__(self, id, nombre_mesa, consumiciones, menus, precio):
        self._id = id
        self._nombre_mesa = nombre_mesa
        self._consumiciones = consumiciones  # Suponemos que es una lista de instancias de Consumicion
        self._menus = menus  # Suponemos que es una lista de instancias de Menu
        self._precio = precio
    @classmethod
    def from_dict(cls, data):
        """
        Crea una instancia de Factura a partir de un diccionario.
        """
        consumiciones = [Consumicion.from_dict(c) for c in data.get('consumiciones', [])]
        menus = [MenuComprar.from_dict(m) for m in data.get('menus', [])]

        return cls(
            id=data.get('id'),
            nombre_mesa=data.get('nombre_mesa', ''),
            consumiciones=consumiciones,
            menus=menus,
            precio=data.get('precio', 0.0)
        )
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, valor):
        self._id = valor

    @property
    def nombre_mesa(self):
        return self._nombre_mesa

    @nombre_mesa.setter
    def nombre_mesa(self, valor):
        self._nombre_mesa = valor

    @property
    def consumiciones(self):
        return self._consumiciones

    @consumiciones.setter
    def consumiciones(self, valor):
        self._consumiciones = valor

    @property
    def menus(self):
        return self._menus

    @menus.setter
    def menus(self, valor):
        self._menus = valor

    @property
    def precio(self):
        return self._precio

    @precio.setter
    def precio(self, valor):
        self._precio = valor

    def to_dict(self):
        return {
            "id": self._id,
            "nombre_mesa": self._nombre_mesa,
            "consumiciones": [consumicion.to_dict() for consumicion in self._consumiciones],
            "menus": [menu.to_dict() for menu in self._menus],
            "precio": self._precio,
        }

    def __str__(self):
        consumiciones_str = "\n      ".join([consumicion.to_string_cantidad() for consumicion in self._consumiciones]) if self._consumiciones else "Ninguna"
        menus_str = "\n      ".join([str(menu) for menu in self._menus]) if self._menus else "Ninguno"
        return (
            "Factura:\n"
            f"  ID: {self._id}\n"
            f"  Mesa: {self._nombre_mesa}\n"
            f"  Consumiciones:\n      {consumiciones_str}\n"
            f"  Menús:\n      {menus_str}\n"
            f"  Precio: {self._precio}\n"
            "──────────────────────────────────"
        )