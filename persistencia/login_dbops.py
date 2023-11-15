from pymongo.database import Database
from persistencia.mongo_data import get_db
import functools
from pymongo import MongoClient
from datetime import datetime

def getdata():
    try:
        client = MongoClient("mongodb+srv://medbuser:YppbFDwNGXoI6x6J@medecluster.izhjskf.mongodb.net/?retryWrites=true&w=majority")
        db = client['Medetrics']
        return db
    except Exception as e:
        print(f"Error al conectar a MongoDB: {e}")
        raise
        

def buscar_coincidencia_credenciales(correo, contraseña):
    try:
        # Obtenemos la base de datos utilizando la función getdata()
        db = getdata()

        # Accedemos a la colección específica
        collection = db['usuarios']

        # Realizamos la búsqueda con los campos de correo y contraseña
        query = {"correo": correo, "contraseña": contraseña}
        resultado = collection.find_one(query)

        # Verificamos si hay un resultado (coincidencia)
        if resultado:
            print("Credenciales válidas:")
            print(resultado)  # Imprimir el documento que coincide
            return True
        else:
            print("Credenciales inválidas.")
            return False
    except Exception as e:
        print(f"Error al buscar coincidencias en la colección: {e}")
        return False
