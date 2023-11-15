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
        

def send_register(registro: dict[str, str], db: Database = getdata(), collection: str = "usuarios") -> bool:
    try:
        # Convierte el campo 'fecha_de_nacimiento' a un formato compatible con MongoDB
        registro['fecha_de_nacimiento'] = datetime.combine(registro['fecha_de_nacimiento'], datetime.min.time())

        registrado = db[collection].insert_one(registro).acknowledged
        print(f"Registro exitoso: {registrado}")
        return registrado
    except Exception as e:
        print(f"Error al enviar el registro a MongoDB: {e}")
        return False