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
            3. Liberar Mesa
            4. Ver Pedidos
            5. Cambiar Estado Pedido
            6. Ver Facturas
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
                        nombre= str(sitio["nombre"]),
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
        coleccion_reservas = self._baseDatos["reservas"]
        
        documentosMesas = coleccion_mesas.find({"ocupada":False})
        
        #Buscar mesas en la base de datos
        
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
        
        dni = ""
        try:
            dni = self.devolverString("dni","Introduce el dni de la reserva: ")
        except ValueError:
            print("Error al introducir ubicación")
            return
        
        
        #se comprueba que haya capacidad suficiente actualmente en el restaurante
        
        capacidadActual = 0
        for mesa in listaMesas:
            if mesa.ocupada == False and mesa.ubicacion == lugar:
                capacidadActual+= mesa.capacidad
        
        if capacidadActual < capacidadDeseada:
            print("No hay capacidad en el restaurante")
            return
        
        
        
        #Como la barra es diferente porque cada sitio es individual, se comprueba la barra
        
        if lugar == "barra":
            #se busca la instancia de la barra en la lista de mesas y los sitios libres de esta
            mesa = next((mesa for mesa in listaMesas if mesa.ubicacion == lugar),None)
            sitiosLibres = filter(lambda sitio: sitio.ocupado == False,mesa.sitios)
            sitiosLibres = list(sitiosLibres)
            # si no hay sitios libres o hay menos que la capacidad deseada, no hay sitio en la barra
            if mesa is None or not sitiosLibres or len(sitiosLibres) < capacidadDeseada or mesa.ocupada == True:
                print("No hay espacio suficiente en la barra")
                return
            # se recorre la lista de sitios libres tantas veces como clientes haya
            listaSitios = []
            for i,sitio in enumerate(sitiosLibres):
                if i < capacidadDeseada:
                    sitio.ocupado = True
                    coleccion_mesas.update_many({"nombre_mesa" : mesa.nombre_mesa},{"$set": {"sitios.$[sitio].ocupado": True}},array_filters=[{"sitio.nombre":sitio.nombre}])
                    listaSitios.append(sitio)
                else:
                    coleccion_reservas.insert_one({"dni" : dni,"mesas" : [sitio.to_dict() for sitio in listaSitios]})   
                    break
            # si despues de reservar los sitios, no quedan sitios libres, se ocupa la barra
            if  len(sitiosLibres) - capacidadDeseada == 0:
                mesa.ocupada = True
                coleccion_mesas.update_one({"nombre_mesa" : mesa.nombre_mesa},{"$set" : {"ocupada" : True}})
                return
            
            print(capacidadDeseada , "espacios reservados en la barra")
            return
        
        
        # si hay una mesa de esa capacidad se reserva
                      
        for mesa in listaMesas:
            if mesa.capacidad == capacidadDeseada and mesa.ubicacion == lugar:
                mesa.ocupada = True
                coleccion_mesas.update_one({"nombre_mesa" : mesa.nombre_mesa},{"$set" : {"ocupada" : True}})
                coleccion_reservas.insert_one({"dni" : dni,"mesas" : [mesa]})   
                print("Reserva completada, se ha reservado :"+mesa.nombre_mesa + " en : "+lugar)
                return
        
        #se buscan las posibles combinaciones de mesas para cumplir la capacidad deseada
        
        mesasDisponibles = self.buscarCombinacionMesa(capacidadDeseada,0,[],listaMesas,lugar)
        print(mesasDisponibles)
        #si no hay
        if mesasDisponibles == None:
            #se intenta meter a la gente en una mesa mas grande
            mesasOrdenadas = listaMesas.copy()
            mesasOrdenadas.sort(key = lambda mesa: mesa.capacidad, reverse=True)
            for mesa in mesasOrdenadas:
                if mesa.capacidad > capacidadDeseada and mesa.ubicacion == lugar:
                    mesa.ocupada = True
                    coleccion_mesas.update_one({"nombre_mesa" : mesa.nombre_mesa},{"$set" : {"ocupada" : True}})
                    coleccion_reservas.insert_one({"dni" : dni,"mesas" : [mesa]})   
                    print("Reserva completada, se ha reservado :"+mesa.nombre_mesa + " en : "+lugar)
                    return
            # si no hay ninguna mesa grande en la que puedan entrar todos, se buscan combinaciones de mesas
            # aumentando la cantidad de 1 en 1 para intentar desperdiciar el menor numero de asientos posibles
            i = 1
            mesasDisponibles = self.buscarCombinacionMesa(capacidadDeseada + i,0,[],listaMesas,lugar)     
            while mesasDisponibles == None and i < capacidadActual:
                   mesasDisponibles = self.buscarCombinacionMesa(capacidadDeseada + i,0,[],listaMesas,lugar)
                   i+=1     
        
        texto = ""
        
        print(mesasDisponibles)
        # se reservan las mesas disponibles
        for mesa in mesasDisponibles:
            print(mesa.nombre_mesa)
            texto += mesa.nombre_mesa+"\n"
            mesa.ocupada = True
            coleccion_mesas.update_one({"nombre_mesa" : mesa.nombre_mesa},{"$set" : {"ocupada" : True}})
            
        coleccion_reservas.insert_one({"dni" : dni,"mesas" : [mesa.to_dict() for mesa in mesasDisponibles]})    
            
        print("Se han reservado correctamente las mesas: "+texto)
        
    def buscarCombinacionMesa(self,capacidad,posicion,listaMesas,mesas,lugar):
        """
        Método que se encarga de buscar posibles combinaciones de mesas para agrupar y cumplir
        la capacidad establecida en el parámetro capacidad.
        
        Parámetros: 
        capacidad (int) : capacidad que debe cumplir la combinacion, se va restando hasta llegar a 0
        posicion (int) : posicion por la que empezar a buscar elementos de la lista para agrupar
        listaMesas([Mesa]) : lista de mesas que están en la combinacion actual
        mesas([Mesa]) : lista de mesas disponibles sobre la que iterar
        lugar(str) : ubicacion de donde se quiere sentar el cliente dentro del bar
        
        """
        
        if capacidad == 0:
            return listaMesas.copy()
        
        for i in range(posicion,len(mesas)):
            if capacidad - mesas[i].capacidad >= 0 and mesas[i].ubicacion == lugar:
                if mesas[i] in listaMesas:
                    continue
                listaMesas.append(mesas[i])
                listaCombinaciones = self.buscarCombinacionMesa(capacidad - mesas[i].capacidad,posicion + 1,listaMesas,mesas,lugar)
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