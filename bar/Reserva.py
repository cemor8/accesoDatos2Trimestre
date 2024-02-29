class Reserva:
    def __init__(self, dni, mesas):
        self._dni = dni
        self._mesas = mesas
        
    @property
    def dni(self):
        return self._dni

    @property
    def mesas(self):
        return self._mesas

    @dni.setter
    def dni(self, valor):
        self._dni = valor

    @mesas.setter
    def mesas(self, valor):
        self._mesas = valor

    def to_dict(self):
        return {"dni": self._dni, "mesas": [mesa.to_dict() for mesa in self._mesas]}
    def __str__(self):
        mesas_str = ', '.join(str(mesa) for mesa in self._mesas)
        return f"Reserva DNI: {self._dni}, Mesas: [{mesas_str}]"