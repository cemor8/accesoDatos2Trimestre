from datetime import datetime
from Mesa import Mesa
class Reserva:
    def __init__(self, dni, mesas, atendido, creada):
        self._dni = dni
        self._mesas = mesas
        self._atendido = atendido
        self._creada = creada

    @classmethod
    def from_dict(cls, data):
        """
        Crea una instancia de Reserva a partir de un diccionario.
        """
        mesas = [Mesa.from_dict(mesa) for mesa in data.get('mesas', [])]

        return cls(
            dni=data.get('dni', ''),
            mesas=mesas,
            atendido=data.get('atendido', False),
            creada=data.get('creada', datetime.now().isoformat())
        )
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
        self._creada = valor

    def to_dict(self):
        return {
            "dni": self._dni,
            "mesas": [mesa.to_dict() for mesa in self._mesas],
            "atendido": self._atendido,
            "creada": self._creada.isoformat() if self._creada else None
        }

    def __str__(self):
        mesas_str = "\n    ".join([str(mesa) for mesa in self._mesas]) if self._mesas else "Ninguna"
        atendido_str = "Sí" if self._atendido else "No"
        creada_str = self._creada.strftime('%Y-%m-%d %H:%M:%S') if self._creada else "Desconocida"
        return (
            f"Reserva:\n"
            f"  DNI: {self._dni}\n"
            f"  Mesas:\n    {mesas_str}\n"
            f"  Atendido: {atendido_str}\n"
            f"  Creada: {creada_str}\n"
            "───────────────────────────────"
        )