class Consumicion:
    def __init__(self, nombre, precio, cantidad):
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad  

    def to_dict(self):
        return {
            'nombre': self.nombre,
            'precio': self.precio,
            'cantidad': self.cantidad  
        }
    def __str__(self):
        return f"Consumicion(nombre={self.nombre}, precio={self.precio}, cantidad={self.cantidad})"