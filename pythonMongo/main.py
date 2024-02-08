from pymongo import MongoClient
from Carta import Carta
from Club import Club
import sys

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
        8. Ver clubes
        9. Eliminar club y cartas
        10. Modificar club
        11. Salir
""")
    try:
        numero = int(input("Selecciona una opcion: \n"))
        if numero<1 or numero > 11:
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
        eliminarClub()
    elif numero == 10:
        modificarClub()
    elif numero == 11:
        sys.exit()
        
    menu()


def mostrarCartas():
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
    nombre_jugador = devolverString("nombre_jugador","Introduce el nombre del jugador: ")
    calidad = devolverString("calidad","Introduce una calidad de la carta: ")
    club = devolverString("autor","Introduce el club del jugador: ")
    
    documento = coleccion_clubes.find_one({"nombre_club" : club})
    if not documento:
        print("No existe un club con ese nombre, crealo")
        return
    
    dorsal = devolverString("dorsal","Introduce el dorsal del jugador: ")
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
        print("Ya hay una carta de ese jugador con esa calidad, modificala o eliminala")


def mostrarCartaPropiedad(propiedad):
    valor = devolverString(propiedad,"Introduce el valor")
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
    nombre_jugador = devolverString("nombre_jugador","Introduce el nombre del jugador a borrar: ")
    calidad = devolverString("calidad","Introduce su calidad: ")
    club = devolverString("club","Introduce su club: ")
    documento = coleccion_cartas.find_one({"nombre_jugador": nombre_jugador, "calidad": calidad, "club": club})
    if documento is None:
        print("Carta no encontrada")
        return
    else:
        nuevo_nombre_jugador = devolverString("nombre_jugador","Introduce el nombre del jugador: ")
        nueva_calidad = devolverString("calidad","Introduce una calidad de la carta: ")
        nuevo_club = devolverString("autor","Introduce el club del jugador: ")
    
        documento = coleccion_clubes.find_one({"club" : club})
        if documento is None:
            print("Carta no encontrada")
            return
    
        dorsal = devolverString("dorsal","Introduce el dorsal del jugador: ")
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
    nombre_club = devolverString("nombre_club","Introduce el nombre del jugador: ")

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
    nombre_club = devolverString("nombre_club","Introduce el nombre del club: ")
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
    nombre_club = devolverString("nombre_club","Introduce el nombre del club a borrar: ")
    documentos = coleccion_clubes.find({"nombre_club":nombre_club})
    if not documentos:
        print("Club no encontrado")
    else:
        coleccion_clubes.delete_one({"nombre_club": nombre_club})
        
        coleccion_cartas.delete_many({"club": nombre_club})
        
def modificarClub():
    nombre_club = devolverString("nombre_club","Introduce el nombre del club a modificar: ")
    documentos = coleccion_clubes.find({"nombre_club":nombre_club})
    if not documentos:
        print("Club no encontrado")
    else:
        nuevo_nombre = devolverString("nombre_club","Introduce el nombre del club a modificar: ")
        coleccion_cartas.update_many({"club":nombre_club},{"$set":{"club":nuevo_nombre}})
        coleccion_clubes.update_one({"nombre_club":nombre_club},{"$set":{"nombre_club":nuevo_nombre}})


def devolverString(campo,textoMostrar):
    try:
        valor= str(input(textoMostrar))
        return valor
    except ValueError:
        print("Error al introducir un valor")
        devolverString(campo,textoMostrar)

def devolverInt(textoMostrar):
    try:
        valor= int(input(textoMostrar))
        return valor
    except ValueError:
        print("Error al introducir un valor")
        devolverInt()
        
menu()