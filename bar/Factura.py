class Factura:
    def __init__(self, id, nombre_mesa, consumiciones, menus, precio):
        self._id = id
        self._nombre_mesa = nombre_mesa
        self._consumiciones = consumiciones  # Suponemos que es una lista de instancias de Consumicion
        self._menus = menus  # Suponemos que es una lista de instancias de Menu
        self._precio = precio

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
        consumiciones_str = ", ".join([str(consumicion) for consumicion in self._consumiciones])
        menus_str = ", ".join([str(menu) for menu in self._menus])
        return f"Factura(id={self._id}, nombre_mesa={self._nombre_mesa}, consumiciones=[{consumiciones_str}], menus=[{menus_str}], precio={self._precio})"