from Mesa import Mesa
from Sitio import Sitio
from datetime import datetime, timedelta
from Pedido import Pedido
from Reserva import Reserva
from Consumicion import Consumicion
from Factura import Factura
import re
import sys
class ControllerAdministrador:
    def __init__(self, administrador, baseDatos):
        self._administrador = administrador
        self._baseDatos = baseDatos
        self._exrpesiones = {
            "lugar" : "^(interior|terraza|barra)$",
            "dni" : "^[0-9]{8}[A-HJ-NP-TV-Z]$",
            "nombreConsumicion" : ""

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
            6. Comprobar Reservas
            7. Ver Reservas
            8. Gestionar Stock
            9. Salir
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
        elif numero == 3:
            self.verPedidos()
        elif numero == 4:
            self.cambiarEstadoPedido()
        elif numero == 5:
            self.verFacturas()
        elif numero == 6:
            self.comprobarReservas()
        elif numero == 7:
            self.verReservas()
        elif numero == 8:
            self.stock()
        elif numero == 9:
            sys.exit(0)
        self.mostrarMenu()
    def mostrarMesas(self):
        """
        Método que se encarga de mostrar las mesas del bar
        """
        coleccion_mesas = self._baseDatos["mesas"]
        documentosMesas = coleccion_mesas.find()
        listaMesas = []
        for documento in documentosMesas:
            sitios = []
            if documento.get("sitios") is not None:
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
        coleccion_reservas = self._baseDatos["reservas"]
        
        documentosMesas = coleccion_mesas.find({"ocupada":False})
        
        #Buscar mesas en la base de datos
        
        listaMesas = []
        for documento in documentosMesas:
            sitios = []
            if documento.get("sitios") is not None:
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
        
        coleccion_reservas = self._baseDatos["reservas"]
        listaReservas = coleccion_reservas.find()
        reservas = [Reserva.from_dict(reserva) for reserva in listaReservas]
        for reserva in reservas:
            if reserva.dni == dni:
                print("Ya hay una reserva con ese dni")
                return
        print(dni)
        
        #se comprueba que haya capacidad suficiente actualmente en el restaurante
        
        capacidadActual = 0
        for mesa in listaMesas:
            if mesa.ocupada == False and mesa.ubicacion == lugar:
                capacidadActual+= mesa.capacidad
        
        print(capacidadActual)
        print(listaMesas)
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
                    mesa.sitios = listaSitios
                    coleccion_reservas.insert_one({"dni" : dni,"mesas" : [mesa.to_dict()],"atendido": False,"creada": datetime.utcnow()})   
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
                coleccion_reservas.insert_one({"dni" : dni,"mesas" : [mesa.to_dict()],"atendido": False,"creada": datetime.utcnow()})   
                print("Reserva completada, se ha reservado la mesa con nombre: "+ mesa.nombre_mesa + " en: "+lugar)
                return
        
        #se buscan las posibles combinaciones de mesas para cumplir la capacidad deseada
        
        mesasDisponibles = self.buscarCombinacionMesa(capacidadDeseada,0,[],listaMesas,lugar)
        print(mesasDisponibles)
        #si no hay
        if mesasDisponibles == None:
            #se intenta meter a la gente en una mesa mas grande
            mesasOrdenadas = listaMesas.copy()
            mesasOrdenadas.sort(key = lambda mesa: mesa.capacidad, reverse=False)
            for mesa in mesasOrdenadas:
                if mesa.capacidad > capacidadDeseada and mesa.ubicacion == lugar:
                    mesa.ocupada = True
                    coleccion_mesas.update_one({"nombre_mesa" : mesa.nombre_mesa},{"$set" : {"ocupada" : True}})
                    coleccion_reservas.insert_one({"dni" : dni,"mesas" : [mesa.to_dict()],"atendido": False,"creada": datetime.utcnow()})   
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
            
        coleccion_reservas.insert_one({"dni" : dni,"mesas" : [mesa.to_dict() for mesa in mesasDisponibles],"atendido": False,"creada": datetime.utcnow()})    
            
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
    
    def verReservas(self):
        """
        Método que muestra las reservas actuales en el restaurante
        """
        coleccion_reservas = self._baseDatos["reservas"]
        listaReservas = coleccion_reservas.find()
        reservas = [Reserva.from_dict(reserva) for reserva in listaReservas]
        for reserva in reservas:
            print(reserva)
    def comprobarReservas(self):
        """
        Método que comprueba las reservas, si ha pasado mas de una hora desde que se hizo y 
        el cliente no ha llegado, se elimina la reserva
        """
        coleccion_reservas = self._baseDatos["reservas"]
        coleccion_mesas = self._baseDatos["mesas"]
        
        una_hora_atras = datetime.utcnow() - timedelta(hours=1)

        consultaReserva = {
            "atendido": False,
            "creada": {"$lt": una_hora_atras}
        }

        reservas =  coleccion_reservas.find(consultaReserva)
        
        
        for reserva in reservas:
            for mesa_reservada in reserva.get('mesas', []):
                mesa =  coleccion_mesas.find_one({"nombre_mesa": mesa_reservada["nombre_mesa"]})
                if mesa:
                    print("hay mesa")
                    sitios_actualizados = []
                    for sitio in mesa.get('sitios', []):
                        
                        if sitio['nombre'] in mesa_reservada.get('sitios', []):
                            sitio['ocupado'] = False
                        sitios_actualizados.append(sitio)


                    coleccion_mesas.update_one(
                        {"nombre_mesa": mesa_reservada["nombre_mesa"]},
                        {"$set": {"sitios": sitios_actualizados,"ocupada": False}}
                    )

            
            coleccion_reservas.delete_one({"dni": reserva['dni']})
            print("Reserva de "+reserva["dni"]+" eliminada")

    def verPedidos(self):
        """
        Método que muestra todos los pedidos en curso en el restaurante
        """
        coleccion_pedidos = self._baseDatos["pedidos"]
        listaPedidos = coleccion_pedidos.find()
        pedidos = [Pedido.from_dict(pedido) for pedido in listaPedidos]
        for pedido in pedidos:
            print(pedido)
    def cambiarEstadoPedido(self):
        """
        Método que cambia el estado de un pedido
        """
        coleccion_pedidos = self._baseDatos["pedidos"]
        idPedidoCambiar = self.devolverInt("Introduce el id del pedido: ")
        pedidoCambiar = coleccion_pedidos.find_one({"id": idPedidoCambiar})
        if pedidoCambiar:
            print("""
                1. Libre
                2. Confirmado
                3. Preparando
                4. Servido
                """)
            estado = self.devolverInt("Introduce una opcion: ")

            estados = {
                1: "Libre",
                2: "Confirmado",
                3: "Preparando",
                4: "Servido"
            }
            estado_seleccionado = estados.get(estado, None)

            if estado_seleccionado:
                resultado = coleccion_pedidos.update_one({"id": idPedidoCambiar}, {"$set": {"estado": estado_seleccionado}})
                if resultado.modified_count > 0:
                    print("El estado del pedido ha sido actualizado a:", estado_seleccionado)
                else:
                    print("No se ha podido actualizar el estado del pedido.")
            else:
                print("Opción no válida.")
        else:
            print("Pedido no encontrado.")
    def verFacturas(self):
        """
        Método que muestra todas las facturas
        """
        coleccion_pedidos = self._baseDatos["facturas"]
        listaFacturas = coleccion_pedidos.find()
        facturas = [Factura.from_dict(factura) for factura in listaFacturas]
        for factura in facturas:
            print(factura)
    def stock(self):
        """
        Método que se encarga de mostrar el menú para modificar el stock de 
        los pedidos
        """
        
        print("""
            1. Añadir consumicion
            2. Eliminar consumicion
            3. Modificar consumicion
            4. Modificar Menu
            5. Volver
            """)
        try:
            numero = int(input("Selecciona una opcion: \n"))
            if numero<1 or numero > 5:
                self.mostrarMenu()
                
        except ValueError:
            print("error al introducir numero")
            self.stock()
        if numero == 1:
            self.meterConsumicion()
        elif numero == 2:
            self.eliminarConsumicion()
        elif numero == 3:
            self.modificarConsumicion()
        elif numero == 4:
            self.modificarMenu()
        elif numero == 5:
            self.mostrarMenu()
        self.stock()
        
        
    def meterConsumicion(self):
        """
        Método que se encarga de meter una consumicion en la base de datos, ya sea un plato o una bebida
        """
        print("""
            1. Plato
            2. Bebida
            """)
        opcion = self.devolverInt("Introduce el tipo de consumicion: ")
        if opcion != 1 and opcion != 2:
            print("opción inválida")
            return
        coleccion = None
        if opcion == 1:
            coleccion = self.baseDatos["platos"]
        elif opcion == 2:
            coleccion = self.baseDatos["bebidas"]
                
        listaDocs = coleccion.find()
        consumiciones = [Consumicion.from_dict(consumicion) for consumicion in listaDocs]
        
        
        nombre = self.devolverString("nombreConsumicion","Introduce el nombre de la consumicion: ")
        
        if any(consumicion.nombre == nombre for consumicion in consumiciones):
            print("Ya existe una consumición con ese nombre. Por favor, introduce un nombre diferente.")
            return
        
        precio = self.devolverDouble("Introduce el precio de la consumicion: ")
        cantidad = self.devolverDouble("Introduce la cantidad de la consumcion: ")
        try:
            if cantidad < 1 or precio < 2:
                print("Datos inválidos")
                return
        except:
            print("Error")
            return
        nueva_consumicion = {"nombre": nombre, "precio": precio, "cantidad": cantidad}
        coleccion.insert_one(nueva_consumicion)
        print("Consumición añadida correctamente.")
        
    def eliminarConsumicion(self):
        """
        Método que se encarga de eliminar una consumicion de la base de datos, ya sea bebida o plato, lo elimina tambien de los
        menus
        """
        print("""
            1. Plato
            2. Bebida
            """)
        opcion = self.devolverInt("Introduce el tipo de consumicion: ")
        if opcion != 1 and opcion != 2:
            print("opción inválida")
            return
        coleccion = None
        if opcion == 1:
            coleccion = self.baseDatos["platos"]
        elif opcion == 2:
            coleccion = self.baseDatos["bebidas"]
                
        listaDocs = coleccion.find()
        consumiciones = [Consumicion.from_dict(consumicion) for consumicion in listaDocs]
        nombre = self.devolverString("nombreConsumicion","Introduce el nombre de la consumicion: ")
        if any(consumicion.nombre == nombre for consumicion in consumiciones):
            coleccion.delete_one({"nombre": nombre})
            
            coleccionMenus = self.baseDatos["menus"]
            coleccionMenus.update_many({}, {"$pull": {"primeros": {"nombre": nombre},"segundos": {"nombre": nombre},"bebidas": {"nombre": nombre}}})
            
            print("Consumicion eliminada correctamente")
            return
        else:
            print("Consumicion no encontrada")
    def modificarConsumicion(self):
        """
        Método que se encarga de modificar una consumicion
        """
        print("""
            1. Plato
            2. Bebida
            """)
        opcion = self.devolverInt("Introduce el tipo de consumicion: ")
        if opcion != 1 and opcion != 2:
            print("opción inválida")
            return
        coleccion = None
        if opcion == 1:
            coleccion = self.baseDatos["platos"]
        elif opcion == 2:
            coleccion = self.baseDatos["bebidas"]    
        
        nombre = self.devolverString("nombreConsumicion","Introduce el nombre de la consumicion a modificar")
        consumicion = coleccion.find_one({"nombre": nombre})
        if consumicion:
            nuevoNombre = self.devolverString("nombreConsumicion","Introduce el nombre nuevo")
            consumicionTest = coleccion.find_one({"nombre": nuevoNombre})
            if consumicionTest and nombre != nuevoNombre:
                print("nombre inválido")
                return
            precio = self.devolverDouble("Introduce el precio de la consumicion")
            cantidad = self.devolverDouble("Introduce la cantidad de la consumcion")
            try:
                if cantidad < 1 or precio < 2:
                    print("Datos inválidos")
                    return
            except:
                print("Error")
                return
            coleccion.update_one({"nombre": nombre}, {"$set" : { "nombre" : nuevoNombre, "cantidad" : cantidad, "precio" : precio}})
            coleccionMenus = self.baseDatos["menus"]
            coleccionMenus.menus.update_many({"primeros.nombre": nombre},[{"$set": {"primeros.$[elem].nombre": nuevoNombre,"primeros.$[elem].cantidad": cantidad,"primeros.$[elem].precio": precio}}],array_filters=[{"elem.nombre": nombre}],upsert=False)
            print("Consumicion actualizada correctamente")
        else:
            print("Consumicion no encontrada")
        
    def modificarMenu(self):
        """
        Método que se encarga de añadir o eliminar una consumicion en un menú
        """
            
        print("""
            1. Primeros
            2. Segundos
            3. Bebidas
            """)
        
        opcion = self.devolverInt("Introduce la opcion correspondiente a la lista modificar: ")
        coleccion_consumiciones = None
        lista = None
        if opcion == 1:
            coleccion_consumiciones = self.baseDatos["platos"]
            lista = "primeros"
        elif opcion == 2: 
            coleccion_consumiciones = self.baseDatos["platos"]
            lista = "segundos"
        elif opcion == 3:
            coleccion_consumiciones = self.baseDatos["bebidas"]
            lista = "bebidas"
        else:
            print("Opción inválida")
            return
        print("""
            1. Añadir
            2. Eliminar
            """)
        opcion = self.devolverInt("Introduce la opcion correspondiente ")
        operacion = None
        if opcion == 1:
            operacion = "añadir"
        elif opcion == 2: 
            operacion = "eliminar"
        else:
            print("Opción inválida")
            return
        
        nombre = self.devolverString("nombreConsumicion","Introduce el nombre de la consumicion")
        diaMenu = self.devolverString("diaMenu","Introduce el día del menú")
        consumicion = coleccion_consumiciones.find_one({"nombre": nombre})
        
        if consumicion:
            if operacion == "añadir":
                #añadir sin duplicado addToSet
                self.baseDatos["menus"].update_one(
                    {"dia" : diaMenu},
                    {"$addToSet": {lista: consumicion}}
                )
                print("Consumición añadida correctamente.")
            elif operacion == "eliminar":
                documento = self.baseDatos["menus"].find_one({"dia": diaMenu, lista: {"$elemMatch": {"nombre": consumicion["nombre"]}}})
                
                if not documento:
                    print("La lista no contiene esa consumicion")
                    return
                
                self.baseDatos["menus"].update_one(
                    {"dia" : diaMenu }, 
                    {"$pull": {lista:{"nombre" : consumicion["nombre"]}}}
                )
                print("Consumición eliminada correctamente.")
        else:
            print("Consumicion no encontrada")
        
    def devolverString(self,campo,textoMostrar):
        """
        Método que devuelve una string
        """
        try:
            valor= str(input(textoMostrar))
            if re.match(self._exrpesiones.get(campo),valor,re.IGNORECASE):
                return valor
            else:
                raise ValueError
        except ValueError:
            print("Contenido inválido")
            return self.devolverString(campo,textoMostrar)

    def devolverInt(self,textoMostrar):
        """
        Método que devuelve un numero entero
        """
        try:
            valor= int(input(textoMostrar))
            return valor
        except ValueError:
            print("Error al pedir int")
            return self.devolverInt(textoMostrar)
    def devolverDouble(self,textoMostrar):
        """
        Método que devuelve un double
        """
        try:
            valor= float(input(textoMostrar))
            if valor < 1:
                raise ValueError
            return valor
        except ValueError:
            print("Error al pedir int")
            return self.devolverDouble(textoMostrar)