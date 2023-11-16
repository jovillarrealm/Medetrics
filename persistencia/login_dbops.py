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
        

def buscar_coincidencia_credenciales(email, contraseña):
    try:
        # Obtenemos la base de datos utilizando la función getdata()
        db = getdata()

        # Accedemos a la colección específica
        collection = db['usuarios']

        # Realizamos la búsqueda con los campos de correo y contraseña
        query = {"email": email, "contraseña": contraseña}
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

def buscar_numero_salud(email, contraseña):
    try:
        # Obtenemos la base de datos utilizando la función getdata()
        db = getdata()

        # Accedemos a la colección específica
        collection = db['usuarios']

        # Realizamos la búsqueda con los campos de correo y contraseña
        query = {"email": email, "contraseña": contraseña}
        resultado = collection.find_one(query)

        # Verificamos si hay un resultado (coincidencia)
        if resultado:
            print("Credenciales válidas:")
            print(resultado)  # Imprimir el documento que coincide
            # Devolver el valor de 'numero_salud' si existe en el documento
            return resultado.get('numero_salud')
        else:
            print("Credenciales inválidas.")
            return None  # No se encontraron coincidencias, devolver None
    except Exception as e:
        print(f"Error al buscar coincidencias en la colección: {e}")
        return None  # Manejar errores devolviendo None
    
def buscar_y_actualizar_contraseña(email, nueva_contraseña):
    try:
        # Obtenemos la base de datos utilizando la función getdata()
        db = getdata()

        # Accedemos a la colección específica
        collection = db['usuarios']

        # Realizamos la búsqueda con el campo de correo
        query = {"email": email}
        resultado = collection.find_one(query)

        # Verificamos si hay un resultado (coincidencia)
        if resultado:
            print("Usuario encontrado. Actualizando contraseña...")
            # Actualizamos el valor de la contraseña por el nuevo valor proporcionado
            collection.update_one({"email": email}, {"$set": {"contraseña": nueva_contraseña}})
            print("Contraseña actualizada exitosamente.")
            return True
        else:
            print("No se encontró ningún usuario con ese correo.")
            return False
    except Exception as e:
        print(f"Error al buscar o actualizar la contraseña: {e}")
        return False
