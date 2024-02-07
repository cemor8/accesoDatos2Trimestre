class Club:
    def __init__(self, nombre, cartas):
        self._nombre_club = nombre
        self._cartas = cartas


    def mostrar_info(self):
        print(f"Nombre: {self._nombre_club}")
        print("Cartas:")
        for carta in self._cartas.items():
            carta.mostrar_info
            print("---")
            
    def to_dict(self):
        return {
            "nombre_club": self._nombre_club,
            "cartas": [carta.to_dict() for carta in self._cartas]
        }