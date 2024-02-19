class Administrador:
    def __init__(self, nombre_de_usuario, contraseña):
        self._nombre_de_usuario = nombre_de_usuario
        self._contraseña = contraseña

    @property
    def nombre_de_usuario(self):
        return self._nombre_de_usuario

    @nombre_de_usuario.setter
    def nombre_de_usuario(self, valor):
        # Aquí puedes añadir validaciones si es necesario
        self._nombre_de_usuario = valor

    @property
    def contraseña(self):
        return self._contraseña

    @contraseña.setter
    def contraseña(self, valor):
        # Aquí puedes añadir validaciones si es necesario
        self._contraseña = valor
    