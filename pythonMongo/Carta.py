class Carta:
    def __init__(self, nombre_jugador, calidad, club, dorsal, posicion, habilidades):
        self._nombre_jugador = nombre_jugador
        self._calidad = calidad
        self._club = club
        self._dorsal = dorsal
        self._posicion = posicion
        self._habilidades = habilidades

    # Getters
    @property
    def nombre_jugador(self):
        return self._nombre_jugador

    @property
    def calidad(self):
        return self._calidad

    @property
    def club(self):
        return self._club

    @property
    def dorsal(self):
        return self._dorsal

    @property
    def posicion(self):
        return self._posicion

    @property
    def habilidades(self):
        return self._habilidades

    # Setters
    @nombre_jugador.setter
    def nombre_jugador(self, valor):
        self._nombre_jugador = valor

    @calidad.setter
    def calidad(self, valor):
        self._calidad = valor

    @club.setter
    def club(self, valor):
        self._club = valor

    @dorsal.setter
    def dorsal(self, valor):
        self._dorsal = valor

    @posicion.setter
    def posicion(self, valor):
        self._posicion = valor

    @habilidades.setter
    def habilidades(self, valor):
        self._habilidades = valor

    def mostrar_info(self):
        print(f"Jugador: {self._nombre_jugador}")
        print(f"Calidad: {self._calidad}")
        print(f"Club: {self._club}")
        print(f"Dorsal: {self._dorsal}")
        print(f"Posición: {self._posicion}")
        print("Habilidades:")
        for habilidad, valor in self._habilidades.items():
            print(f"  {habilidad}: {valor}")
            
    def to_dict(self):
        return {
            "nombre_jugador": self._nombre_jugador,
            "calidad": self._calidad,
            "club": self._club,
            "dorsal": self._dorsal,
            "posicion": self._posicion,
            "habilidades": self._habilidades
        }