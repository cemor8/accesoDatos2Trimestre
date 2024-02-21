from Mesa import Mesa
from Sitio import Sitio

class ControllerAdministrador:
    def __init__(self, administrador, baseDatos):
        self._administrador = administrador
        self._baseDatos = baseDatos
        self._exrpesiones = {
            "lugar" : ""
        }
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
        if numero == 1:
            self.mostrarMesas()
        elif numero == 2:
            self.reservarMesa()
        self.mostrarMenu()
    def mostrarMesas(self):
        """
        Método que se encarga de mostrar las mesas del bar
        """
        coleccion_mesas = self._baseDatos["mesas"]
        documentosMesas = coleccion_mesas.find()
        listaMesas = []
        for documento in documentosMesas:
            sitios = None
            if documento.get("sitios") is not None:
                sitios = []
                for sitio in documento["sitios"]:
                    sitio = Sitio(
                        nombre=sitio["nombre"],
                        ocupado=sitio["ocupado"]
                    )
                    sitios.append(sitio)
                
            mesa = Mesa(
                nombre_mesa=documento["nombre_mesa"],
                ocupada= documento["ocupada"],
                ubicacion=documento["ubicacion"],
                capacidad=documento["capacidad"],
                sitios=sitios
            )
            listaMesas.append(mesa)
        for mesa in listaMesas:
            print(mesa)
    def reservarMesa(self):
        """
        Método que se encarga de reservar una mesa para un cliente,
        si no hay mesas de capacidad suficiente pero juntando mesas se podría
        realizar la reserva, se marcan esas mesas como reservadas, si no es posible,
        se descarta debido a que no hay espacio, permite reservar una mesa de una capacidad mayor,
        selecciona la mas cercana a la capacidad establecida 
        """
        coleccion_mesas = self._baseDatos["mesas"]
        
        documentosMesas = coleccion_mesas.find({"ocupada":False})
        listaMesas = []
        for documento in documentosMesas:
            sitios = None
            if documento.get("sitios") is not None:
                sitios = []
                for sitio in documento["sitios"]:
                    sitio = Sitio(
                        nombre=sitio["nombre"],
                        ocupado=sitio["ocupado"]
                    )
                    sitios.append(sitio)
                
            mesa = Mesa(
                nombre_mesa=documento["nombre_mesa"],
                ocupada= documento["ocupada"],
                ubicacion=documento["ubicacion"],
                capacidad=documento["capacidad"],
                sitios=sitios
            )
            listaMesas.append(mesa)
        if not listaMesas:
            print("No hay mesas disponibles")
            return
        capacidadDeseada = 0
        try:
            capacidadDeseada = int(input("Introduce el número de comensales de la reserva: \n"))
            if capacidadDeseada == 0 or capacidadDeseada == None:
                raise ValueError
        except ValueError:
            print("Error al introducir los datos de la reserva")
            return
        
        lugar = ""
        try:
            lugar = self.devolverString("lugar","Introduce ubicacion deseada: ")
        except ValueError:
            print("Error al introducir ubicación")
            return
        
        if lugar == "barra":
            mesa = next((mesa for mesa in listaMesas if mesa.ubicacion == lugar),None)
            sitiosLibres = []
            #metodo que devuelva los sitios libros
            for sitio in mesa.sitios:
                if sitio.ocupado == False:
                    sitios.append(sitio)
            
            if mesa is None or not sitiosLibres or len(sitiosLibres) < capacidadDeseada or mesa.ocupada == True:
                print("No hay espacio suficiente en la barra")
                return
            for sitio in sitiosLibres:
                sitio.ocupado = True
                coleccion_mesas.update_many({"nombre_mesa" : mesa.nombre_mesa},{"$set": {"sitios.$[sitio].ocupado": True}},array_filters=[{"sitio.nombre":sitio.nombre}])
            
            if  len(sitiosLibres) - capacidadDeseada == 0:
                mesa.ocupada = True
                coleccion_mesas.update_one({"nombre_mesa" : mesa.nombre_mesa},{"$set" : {"ocupada" : True}})
                coleccion_mesas.update_one({"nombre_mesa" : mesa.nombre_mesa},{"$set" : {"capacidadActual" : 0}})
                return
            
            coleccion_mesas.update_one({"nombre_mesa" : mesa.nombre_mesa},{"$set" : {"capacidadActual" : mesa.capacidadActual}})
            print(capacidadDeseada + "espacion reservados en la barra")
            return

                      
        for mesa in listaMesas:
            if mesa.capacidad == capacidadDeseada and mesa.ubicacion == lugar:
                mesa.ocupada = True
                coleccion_mesas.update_one({"nombre_mesa" : mesa.nombre_mesa},{"$set" : {"ocupada" : True}})
                print("Reserva completada, se ha reservado :"+mesa.nombre_mesa + " en : "+lugar)
                return
        
        
           
        mesasDisponibles = self.buscarCombinacionMesa(capacidadDeseada,0,[],listaMesas,lugar)
        
        if mesasDisponibles == None:
            mesasOrdenadas = listaMesas.copy()
            mesasOrdenadas.sort(key = lambda mesa: mesa.capacidad, reverse=True)
            for mesa in mesasOrdenadas:
                if mesa.capacidad > capacidadDeseada and mesa.ubicacion == lugar:
                    mesa.ocupada = True
                    coleccion_mesas.update_one({"nombre_mesa" : mesa.nombre_mesa},{"$set" : {"ocupada" : True}})
                    print("Reserva completada, se ha reservado :"+mesa.nombre_mesa + " en : "+lugar)
                    return
                
                
            print("No se ha encontrado una mesa que se adecúe a la capacidad")    
            return
        
        texto = ""
        
        for mesa in mesasDisponibles:
            texto += mesa.nombre_mesa+"\n"
            mesa.ocupada = True
            coleccion_mesas.update_one({"nombre_mesa" : mesa.nombre_mesa},{"$set" : {"ocupada" : True}})
            
        print("Se han reservado correctamente las mesas: "+texto)
        
    def buscarCombinacionMesa(self,capacidad,posicion,listaMesas,mesas,lugar):
        if capacidad == 0:
            return listaMesas.copy()
        
        for i in range(posicion,len(mesas)):
            if capacidad - mesas[i].capacidad >= 0 and mesas[i].ubicacion == lugar:
                listaMesas.append(mesas[i])
                listaCombinaciones = self.buscarCombinacionMesa(self,capacidad - mesas[i].capacidad,posicion + 1,listaMesas,mesas,lugar)
                if listaCombinaciones:
                    return listaCombinaciones
                listaMesas.pop()
        return None
    def devolverString(self,campo,textoMostrar):
        try:
            valor= str(input(textoMostrar))
            #if re.match(self._expresionesRegulares.get(campo),valor):
            return valor
            #else:
                #raise ValueError
        except ValueError:
            print("Contenido inválido")
            self.devolverString(campo,textoMostrar)