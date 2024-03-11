from pymongo import MongoClient
import sys
import re
from ControllerAdministrador import ControllerAdministrador

cliente = MongoClient("mongodb+srv://cemor8:12q12q12@cluster0.3yldjuk.mongodb.net/")
baseDatos = cliente["bar"]

coleccion_admins = baseDatos["administradores"]

while True:
    nombre_usuario = input("Introduce el nombre de usuario: ")
    contraseña = input("Introduce la contraseña: ")
    
    administrador = coleccion_admins.find_one({"nombre_usuario": nombre_usuario, "contraseña": contraseña})
        
    if administrador:
        print("Login exitoso.")
        controllerAdmin = ControllerAdministrador(administrador=None,baseDatos= baseDatos)
        controllerAdmin.mostrarMenu()
    else:
        print("Nombre de usuario o contraseña incorrectos. Por favor, inténtalo de nuevo.")
        opcion = input("¿Deseas intentar nuevamente? S/N: ")
        if opcion.lower() != 's':
            break



