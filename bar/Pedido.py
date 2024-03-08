class Pedido:
    def __init__(self,nombre_mesa, id, consumiciones,menus,estado,precio):
        self._id = id
        self._nombre_mesa = nombre_mesa
        self._consumiciones = consumiciones
        self._menus = menus
        self._estado = estado
        self._precio = precio
        
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
        consumiciones_str = ", ".join([str(consumicion) for consumicion in self._consumiciones])
        menus_str = ", ".join([str(menu) for menu in self._menus])
        return f"Pedido(id={self._id}, Mesa={self._nombre_mesa} , consumiciones=[{consumiciones_str}], menus=[{menus_str}], estado={self._estado}, precio={self._precio})"