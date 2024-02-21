from pymongo import MongoClient
import sys
import re
from ControllerAdministrador import ControllerAdministrador

cliente = MongoClient("mongodb+srv://cemor8:12q12q12@cluster0.3yldjuk.mongodb.net/")
baseDatos = cliente["bar"]

coleccion_bebidas = baseDatos["bebidas"]
coleccion_facturas = baseDatos["facturas"]
coleccion_menusDia = baseDatos["menusDia"]
coleccion_pedido = baseDatos["platos"]
coleccion_platos = baseDatos["platos"]

controllerAdmin = ControllerAdministrador(
    administrador=None,
    baseDatos= baseDatos,
)
controllerAdmin.mostrarMenu()
