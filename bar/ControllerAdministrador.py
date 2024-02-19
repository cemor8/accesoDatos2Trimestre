from Mesa import Mesa

class ControllerAdministrador:
    def __init__(self, administrador, baseDatos):
        self._administrador = administrador
        self._baseDatos = baseDatos
    @property
    def administrador(self):
        return self._administrador

    @administrador.setter
    def administrador(self, valor):
        # Aquí puedes añadir validaciones si es necesario
        self._administrador = valor
        
    @property
    def baseDatos(self):
        return self._baseDatos

    @baseDatos.setter
    def administrador(self, valor):
        # Aquí puedes añadir validaciones si es necesario
        self._baseDatos = valor
    
    def mostrarMenu(self):
        """
        Método que se encarga de mostrar el menú del 
        administrador
        """
        
        print("""
            1. Mostrar Mesas
            2. Reservar Mesa
            3. Ver Pedidos
            4. Cambiar Estado Pedido
            5. Ver Facturas
            """)
        try:
            numero = int(input("Selecciona una opcion: \n"))
            if numero<1 or numero > 12:
                self.mostrarMenu()
        except ValueError:
            print("error al introducir numero")
            self.mostrarMenu()
    def mostrarMesas(self):
        """
        Método que se encarga de mostrar las mesas del bar
        """
        coleccion_mesas = self._baseDatos["mesas"]
        documentosMesas = coleccion_mesas.find()
        listaMesas = []
        for documento in documentosMesas:
            mesa = Mesa(
                nombre_mesa=documento["nombre_mesa"],
                estado= documento["estado"],
                ubicacion=documento["ubicacion"],
                capacidad=documento["capacidad"]
            ) 
            listaMesas.append(mesa)
        for mesa in listaMesas:
            print(mesa)
    def reservarMesa(self):
        """
        Método que se encarga de reservar una mesa para un cliente,
        si no hay mesas de capacidad suficiente pero juntando mesas se podría
        realizar la reserva, se marcan esas mesas como reservadas, si no es posible,
        se descarta debido a que no hay espacio
        """
        coleccion_mesas = self._baseDatos["mesas"]
        
        documentosMesas = coleccion_mesas.find({"ocupada":False})
        listaMesas = []
        for documento in documentosMesas:
            mesa = Mesa(
                nombre_mesa=documento["nombre_mesa"],
                estado= documento["estado"],
                ubicacion=documento["ubicacion"],
                capacidad=documento["capacidad"]
            ) 
            listaMesas.append(mesa)
        if not listaMesas:
            print("No hay mesas disponibles")
            return
        capacidadDeseada
        try:
            capacidadDeseada = int(input("Introduce el número de comensales de la reserva: \n"))
            if capacidadDeseada == 0 or capacidadDeseada == None:
                raise ValueError
        except ValueError:
            print("Error al introducir los datos de la reserva")
            return   
        mesasDisponibles = self.buscarCombinacionMesa(0,0,capacidadDeseada,[],listaMesas)
        
    def buscarCombinacionMesa(self,capacidadActual,posicion,capacidadDeseada,listaMesas,mesas):
        if capacidadActual == capacidadDeseada:
            return listaMesas
        if capacidadActual > capacidadDeseada or posicion == len(mesas):
            return None
        