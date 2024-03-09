from Consumicion import Consumicion
from MenuComprar import MenuComprar
class Pedido:
    def __init__(self,nombre_mesa, id, consumiciones,menus,estado,precio):
        self._id = id
        self._nombre_mesa = nombre_mesa
        self._consumiciones = consumiciones
        self._menus = menus
        self._estado = estado
        self._precio = precio

    @classmethod
    def from_dict(cls, doc):
        """
        Crea una instancia de Pedido a partir de un diccionario .
        """
        consumiciones = [Consumicion.from_dict(c) for c in doc.get("consumiciones", [])]
        menus = [MenuComprar.from_dict(m) for m in doc.get("menus", [])]

        return cls(
            id=doc["id"],
            nombre_mesa=doc.get("nombre_mesa"),
            consumiciones=consumiciones,
            menus=menus,
            estado=doc.get("estado"),
            precio=doc.get("precio")
        )
        
    @property
    def id(self):
        return self._id

    @property
    def nombre_mesa(self):
        return self._nombre_mesa
    @property
    def consumiciones(self):
        return self._consumiciones
    @id.setter
    def id(self, valor):
        self._id = valor
    @nombre_mesa.setter
    def nombre_mesa(self, valor):
        self._nombre_mesa = valor    

    @consumiciones.setter
    def consumiciones(self, valor):
        self._consumiciones = valor
    
    @property
    def menus(self):
        return self._menus

    @property
    def estado(self):
        return self._estado

    @menus.setter
    def menus(self, valor):
        self._menus = valor

    @estado.setter
    def estado(self, valor):
        self._estado = valor
    @property
    def precio(self):
        return self._precio 
    @precio.setter
    def precio(self, valor):
        self._precio = valor

    def to_dict(self):
        return {
            "id": self._id,
            "nombre_mesa" : self._nombre_mesa,
            "consumiciones": [consumicion.to_dict() for consumicion in self._consumiciones],
            "menus": [menu.to_dict() for menu in self._menus],
            "estado": self._estado,
            "precio": self._precio,
        }
    def __str__(self):
        
        if self._consumiciones:
            consumiciones_str = "\n    ".join([consumicion.to_string_cantidad() for consumicion in self._consumiciones])
        else:
            consumiciones_str = "Vacío"
        
        
        if self._menus:
            menus_str = "\n    ".join([str(menu) for menu in self._menus])
        else:
            menus_str = "Vacío"

        return (
            f"Pedido:\n"
            f"  ID: {self._id}\n"
            f"  Mesa: {self._nombre_mesa}\n"
            f"  Consumiciones:\n    {consumiciones_str}\n"
            f"  Menús:\n\n    {menus_str}\n"
            f"  Estado: {self._estado}\n"
            f"  Precio: {self._precio}\n"
            f"───────────────────────────────"
        )