class Consumicion:
    def __init__(self, nombre, precio, cantidad):
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad  

    @classmethod
    def from_dict(cls, dict_data):
        return cls(
            nombre=dict_data.get('nombre', ''),
            precio=dict_data.get('precio', 0),
            cantidad=dict_data.get('cantidad', 0)
        )
    
    def to_dict(self):
        return {
            'nombre': self.nombre,
            'precio': self.precio,
            'cantidad': self.cantidad  
        }
    def __str__(self):
        return (
            f"\n"
            f"      Nombre: {self.nombre}\n"
            f"      Precio: {self.precio}\n"
        )
    def to_string_cantidad(self):
        return (
            f"{self.__str__()}"
            f"      Cantidad: {self.cantidad}\n"
        )