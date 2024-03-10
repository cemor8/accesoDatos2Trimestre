from pymongo import MongoClient
from Carta import Carta
from Club import Club
import sys
import re

cliente = MongoClient("mongodb+srv://cemor8:12q12q12@cluster0.3yldjuk.mongodb.net/")

baseDatos = cliente["fifa"]

coleccion_cartas = baseDatos["cartas"]
coleccion_clubes = baseDatos["clubes"]

expresionesRegulares = {
    "nombre_jugador":  "^[a-zA-ZáéíóúÁÉÍÓÚñÑ\\s]+$",
    "calidad": "^(oro|plata|bronce|toty)$",
    "club": "^[a-zA-Z0-9 .-]+$",
    "dorsal": "^\\d{1,2}$",
    "posicion": "^(DEL|MED|DEF|POR)$",
    "habilidades": "^([0-9]|[1-9][0-9]|100)$"
    
}

libros = []

def menu():
    print("""
        1. Mostrar cartas
        2. Mostrar cartas de un club
        3. Mostrar carta de jugador
        4. Eliminar carta
        5. Modificar carta
        6. Crear carta
        7. Crear club
        8. Ver un club
        9. Mostrar Clubes
        10. Eliminar club y cartas
        11. Modificar club
        12. Salir
""")
    try:
        numero = int(input("Selecciona una opcion: \n"))
        if numero<1 or numero > 12:
            menu()
    except ValueError:
        print("error al introducir numero")
        menu()

    if numero == 1:
        mostrarCartas()
    elif numero == 2:
        mostrarCartaPropiedad("club")
    elif numero == 3:
        mostrarCartaPropiedad("nombre_jugador")
    elif numero == 4:
        eliminarCarta()
    elif numero == 5:
        modificarCarta()
    elif numero == 6:
        crearCarta()
    elif numero == 7:
        crearClub()
    elif numero == 8:
        mostrarClub()
    elif numero == 9:
        mostrarClubes()
    elif numero == 10:
        eliminarClub()
    elif numero == 11:
        modificarClub()
    elif numero == 12:
        sys.exit()
        
    menu()


def mostrarCartas():
    """
    Método que muestra todas las cartas de la
    base de datos
    """
    documentos = coleccion_cartas.find()
    cartas = []
    for doc in documentos:
        carta = Carta(
            nombre_jugador=doc['nombre_jugador'],
            calidad=doc['calidad'],
            club=doc['club'],
            dorsal=doc['dorsal'],
            posicion=doc['posicion'],
            habilidades=doc['habilidades']
        )
        cartas.append(carta)
    if not cartas:
        print("No hay cartas")
    else:
        for carta in cartas:
            carta.mostrar_info()


def crearCarta():
    """
    Método que se encarga de crear una nueva carta, no se puede crear una carta
    si ya hay una con el mismo nombre y calidad o si hay una que tenga el nombre diferente
    y el mismo dorsal
    """
    nombre_jugador = devolverString("nombre_jugador","Introduce el nombre del jugador: ")
    calidad = devolverString("calidad","Introduce una calidad de la carta: ")
    club = devolverString("club","Introduce el club del jugador: ")
    
    documento = coleccion_clubes.find_one({"nombre_club" : club})
    if not documento:
        print("No existe un club con ese nombre, crealo")
        return
    
    cartasDoc = []
    for carta in documento["cartas"]:
        cartaCrear = Carta(
            nombre_jugador=carta['nombre_jugador'],
            calidad=carta['calidad'],
            club=carta['club'],
            dorsal=carta['dorsal'],
            posicion=carta['posicion'],
            habilidades=carta['habilidades']
        )
        cartasDoc.append(cartaCrear)
        
    clubC = Club(
            nombre_club=documento["nombre_club"],
            cartas=cartasDoc
        )    
    dorsal = devolverString("dorsal","Introduce el dorsal del jugador: ")
    
    for carta in clubC.cartas:
        if carta.dorsal == dorsal and carta.nombre_jugador != nombre_jugador:
            print("Dorsal Repetido")
            return
        
    posicion = devolverString("posicion","Introduce la posicion del jugador: ")
    habilidades = {
        "fisico" : devolverString("habilidades","Introduce el físico del jugador: "),
        "defensa" : devolverString("habilidades","Introduce la defensa del jugador: "),
        "ritmo" : devolverString("habilidades","Introduce el ritmo del jugador: "),
        "disparo" : devolverString("habilidades","Introduce el disparo del jugador: "),
        "pase" : devolverString("habilidades","Introduce el pase del jugador: "),
        "regate" : devolverString("habilidades","Introduce el regate del jugador: ")
    }
    
    documentos = coleccion_cartas.find({"nombre_jugador" : nombre_jugador})
    if not documentos or not any(doc['nombre_jugador'] == nombre_jugador and doc["calidad"] == calidad for doc in documentos):
        carta = Carta(
            nombre_jugador=nombre_jugador,
            calidad=calidad,
            club=club,
            dorsal=dorsal,
            posicion=posicion,
            habilidades=habilidades
        )
        coleccion_cartas.insert_one(carta.to_dict())
        coleccion_clubes.update_one({"nombre_club":club},{"$push":{"cartas" : carta.to_dict()}})
        print("Carta creada con éxito")
    else:
        print("Carta inválida, comprueba repetidos o errores")


def mostrarCartaPropiedad(propiedad):
    """
    Método que se encarga de mostrar las cartas de un jugador
    o de un club
    """
    valor = devolverString(propiedad,"Introduce el valor: ")
    documentos = coleccion_cartas.find({propiedad:valor})
    cartas = []
    for doc in documentos:
        carta = Carta(
            nombre_jugador=doc['nombre_jugador'],
            calidad=doc['calidad'],
            club=doc['club'],
            dorsal=doc['dorsal'],
            posicion=doc['posicion'],
            habilidades=doc['habilidades']
        )
        cartas.append(carta)
    if not cartas:
        print("No hay cartas")
    else:
        for carta in cartas:
            carta.mostrar_info()

def eliminarCarta():
    """
    Método que se encarga de eliminar una carta
    de la coleccion de cartas y del club
    """
    nombre_jugador = devolverString("nombre_jugador","Introduce el nombre del jugador a borrar: ")
    calidad = devolverString("calidad","Introduce su calidad: ")
    club = devolverString("club","Introduce su club: ")
    documentos = coleccion_cartas.find({"nombre_jugador":nombre_jugador,"calidad":calidad,"club":club})
    if not documentos:
        print("Carta no encontrada")
    else:
        coleccion_cartas.delete_one({"nombre_jugador": nombre_jugador, "calidad": calidad, "club": club})
        coleccion_clubes.update_one({"nombre_club": club},{"$pull": {"cartas": {"nombre_jugador": nombre_jugador, "calidad": calidad}}})

def modificarCarta():
    """
    Método que se encarga de modificar una carta,
    actualiza el valor en la lista de cartas del club
    """
    nombre_jugador = devolverString("nombre_jugador","Introduce el nombre del jugador a modificar: ")
    calidad = devolverString("calidad","Introduce su calidad: ")
    club = devolverString("club","Introduce su club: ")
    documento = coleccion_cartas.find_one({"nombre_jugador": nombre_jugador, "calidad": calidad, "club": club})
    if documento is None:
        print("Carta no encontrada")
        return
    else:
        nuevo_nombre_jugador = devolverString("nombre_jugador","Introduce el nombre del jugador: ")
        nueva_calidad = devolverString("calidad","Introduce una calidad de la carta: ")
        nuevo_club = devolverString("club","Introduce el club del jugador: ")
    
        documento = coleccion_clubes.find_one({"nombre_club" : nuevo_club})
        if documento is None:
            print("Club no encontrado")
            return
    
        dorsal = devolverString("dorsal","Introduce el dorsal del jugador: ")


        cartasDoc = []
        for carta in documento["cartas"]:
            cartaCrear = Carta(
                nombre_jugador=carta['nombre_jugador'],
                calidad=carta['calidad'],
                club=carta['club'],
                dorsal=carta['dorsal'],
                posicion=carta['posicion'],
                habilidades=carta['habilidades']
            )
            cartasDoc.append(cartaCrear)
        
        clubC = Club(
            nombre_club=documento["nombre_club"],
            cartas=cartasDoc
        )      
       
        for carta in clubC.cartas:
            if (carta.dorsal == dorsal and carta.nombre_jugador != nuevo_nombre_jugador) or carta.calidad == nueva_calidad and carta.nombre_jugador == nuevo_nombre_jugador:
                print("Duplicado o contenido inválido")
                return
            
        posicion = devolverString("posicion","Introduce la posicion del jugador: ")
    
        habilidades = {
            "fisico" : devolverString("habilidades","Introduce el físico del jugador: "),
            "defensa" : devolverString("habilidades","Introduce la defensa del jugador: "),
            "ritmo" : devolverString("habilidades","Introduce el ritmo del jugador: "),
            "disparo" : devolverString("habilidades","Introduce el disparo del jugador: "),
            "pase" : devolverString("habilidades","Introduce el pase del jugador: "),
            "regate" : devolverString("habilidades","Introduce el regate del jugador: ")
        }
        coleccion_cartas.update_one({"nombre_jugador": nombre_jugador, "calidad": calidad, "club": club},
                                    {"$set": 
                                            {"nombre_jugador": nuevo_nombre_jugador,
                                             "calidad": nueva_calidad,
                                             "club": nuevo_club,
                                             "dorsal": dorsal,
                                             "posicion":posicion,
                                              "habilidades":habilidades
                                            }
                                    })
        coleccion_clubes.update_one({"nombre_club": club},{"$pull": {"cartas": {"nombre_jugador": nombre_jugador, "calidad": calidad}}})
        carta_actualizada = {
            "nombre_jugador": nuevo_nombre_jugador,
            "calidad": nueva_calidad,
            "club": nuevo_club,
            "dorsal": dorsal,
            "posicion": posicion,
            "habilidades": habilidades
        }
        coleccion_clubes.update_one({"nombre_club": club, "cartas.nombre_jugador": nombre_jugador, "cartas.calidad": calidad},
                                    {"$push": {
                                        "cartas" : carta_actualizada
                                    }})
        

def crearClub():
    """
    Método que se encarga de crear un club
    """
    nombre_club = devolverString("club","Introduce el nombre del club: ")

    documento = coleccion_clubes.find_one({"nombre_club":nombre_club})
    if not documento :
        club = Club (
           nombre_club = nombre_club,
            cartas = []
        )
        coleccion_clubes.insert_one(club.to_dict())
        print("Club creado")
    else:
        print("Club existente")

def mostrarClub():
    """
    Método que se encarga de mostrar todos los
    datos de un club
    """
    nombre_club = devolverString("club","Introduce el nombre del club: ")
    documentos = coleccion_clubes.find({"nombre_club":nombre_club})
    clubes = []
    for doc in documentos:
        cartasDoc = []
        for carta in doc["cartas"]:
            cartaCrear = Carta(
                nombre_jugador=carta['nombre_jugador'],
                calidad=carta['calidad'],
                club=carta['club'],
                dorsal=carta['dorsal'],
                posicion=carta['posicion'],
                habilidades=carta['habilidades']
            )
            cartasDoc.append(cartaCrear)
        club = Club(
            nombre_club = doc["nombre_club"],
            cartas = cartasDoc
        )
        clubes.append(club)
    if not clubes:
        print("No hay clubes")
    else:
        for club in clubes:
            club.mostrar_info()
            
def eliminarClub():
    """
    Método que se encarga de eliminar un club
    """
    nombre_club = devolverString("club","Introduce el nombre del club a borrar: ")
    documentos = coleccion_clubes.find({"nombre_club":nombre_club})
    if not documentos:
        print("Club no encontrado")
    else:
        coleccion_clubes.delete_one({"nombre_club": nombre_club})
        
        coleccion_cartas.delete_many({"club": nombre_club})
        
def modificarClub():
    """
    Método que se encarga de modificar los datos de un club, solo permite
    cambiar el nombre del club
    """
    nombre_club = devolverString("club","Introduce el nombre del club a modificar: ")
    documento = coleccion_clubes.find_one({"nombre_club":nombre_club})
    if not documento:
        print("Club no encontrado")
    else:
        nuevo_nombre = devolverString("club","Introduce el nuevo nombre del club: ")
        coleccion_cartas.update_many({"club":nombre_club},{"$set":{"club":nuevo_nombre}})
        coleccion_clubes.update_one({"nombre_club":nombre_club},{"$set":{"nombre_club":nuevo_nombre}})
        coleccion_clubes.update_one({"nombre_club":nuevo_nombre}, {"$set": {"cartas.$[].club": nuevo_nombre}})

def mostrarClubes():
    """
    Método que se encarga de mostrar los datos de 
    todos los clubes
    """
    documentos = coleccion_clubes.find()
    clubes = []
    for doc in documentos:
        cartasDoc = []
        for carta in doc["cartas"]:
            cartaCrear = Carta(
                nombre_jugador=carta['nombre_jugador'],
                calidad=carta['calidad'],
                club=carta['club'],
                dorsal=carta['dorsal'],
                posicion=carta['posicion'],
                habilidades=carta['habilidades']
            )
            cartasDoc.append(cartaCrear)
        club = Club(
            nombre_club = doc["nombre_club"],
            cartas = cartasDoc
        )
        clubes.append(club)
    if not clubes:
        print("No hay clubes")
    else:
        for club in clubes:
            club.mostrar_info()

def devolverString(campo,textoMostrar):
    try:
        valor= str(input(textoMostrar))
        if re.match(expresionesRegulares.get(campo),valor):
            return valor
        else:
            raise ValueError
    except ValueError:
        print("Contenido inválido")
        return devolverString(campo,textoMostrar)

def devolverInt(textoMostrar):
    try:
        valor= int(input(textoMostrar))
        return valor
    except ValueError:
        print("Error al introducir un valor")
        return devolverInt(textoMostrar)
        
menu()