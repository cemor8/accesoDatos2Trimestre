from datetime import datetime

class Reserva:
    def __init__(self, dni, mesas, atendido, creada):
        self._dni = dni
        self._mesas = mesas
        self._atendido = atendido
        self._creada = datetime.fromisoformat(creada)

    @property
    def dni(self):
        return self._dni

    @property
    def mesas(self):
        return self._mesas

    @property
    def atendido(self):
        return self._atendido

    @property
    def creada(self):
        return self._creada

    @dni.setter
    def dni(self, valor):
        self._dni = valor

    @mesas.setter
    def mesas(self, valor):
        self._mesas = valor

    @atendido.setter
    def atendido(self, valor):
        self._atendido = valor

    @creada.setter
    def creada(self, valor):
        self._creada = datetime.fromisoformat(valor)

    def to_dict(self):
        return {
            "dni": self._dni,
            "mesas": [mesa.to_dict() for mesa in self._mesas],
            "atendido": self._atendido,
            "creada": self._creada.isoformat() if self._creada else None
        }

    def __str__(self):
        mesas_str = ', '.join(str(mesa) for mesa in self._mesas)
        atendido_str = "Sí" if self._atendido else "No"
        creada_str = self._creada.strftime('%Y-%m-%d %H:%M:%S')
        return f"Reserva DNI: {self._dni}, Mesas: [{mesas_str}], Atendido: {atendido_str}, Creada: {creada_str}"