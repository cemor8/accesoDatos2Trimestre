class Club:
    def __init__(self, nombre_club, cartas):
        self._nombre_club = nombre_club
        self._cartas = cartas


    def mostrar_info(self):
        print("*************************")
        print(f"Nombre: {self._nombre_club}")
        print("Cartas:")
        print("\t", end="")
        if not self._cartas:
            print("\tVacío")
        for carta in self._cartas:
            carta.mostrar_info()
            
            
    def to_dict(self):
        return {
            "nombre_club": self._nombre_club,
            "cartas": [carta.to_dict() for carta in self._cartas]
        }
    @property
    def cartas(self):
        return self._cartas