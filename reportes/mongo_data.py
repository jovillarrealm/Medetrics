from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from Medetrics.settings import BASE_DIR


import functools
from threading import local
from pymongo.database import Database



@functools.lru_cache(maxsize=1)
def get_mongo_credentials():
    """Basicamente, queremos tener las credenciales por fuera del proyecto, en este caso vamos con json.
    Esta función lee ese json y retorna la URI para conectar a Mongo.
    Para no andar dependiendo de leer un archivo cada vez que se va a usar esta URI entonces también se
    lrucachea el resultado para no ser descarados d=====(￣▽￣*)b"""
    with open(BASE_DIR / "reportes" / "mongo.json") as mongo_data:
        from json import load as jload

        credentials = jload(mongo_data)
        uri = [
            "mongodb+srv://",
            credentials["user"],
            ":",
            credentials["pwd"],
            "@",
            credentials["cluster"],
            ".izhjskf.mongodb.net/?retryWrites=true&w=majority",
        ]
    return "".join(uri)


# MONGO_URI = "mongodb+srv://medbuser:<password>@medecluster.izhjskf.mongodb.net/?retryWrites=true&w=majority"
MONGO_URI = get_mongo_credentials()

def get_db() -> Database:
    """Sacar una conexión que aparentemente pymongo se encargará de cerrar"""
    client = mongo_client()
    db = client.Medetrics
    return db


_mongo_client = local()
def mongo_client():
    """
    Mantiene una conexión persistente con la base de datos (en un thread local ಠಿ_ಠ).
    En vez de hacer un cliente por cada request a las views que los usan.
    https://stackoverflow.com/questions/57875852/persistent-mongodb-connection-with-django
    """
    client = getattr(_mongo_client, 'client', None)
    if client is None:
        client = MongoClient(MONGO_URI)
        _mongo_client.client = client
    return client


if __name__ == "__main__":
    print(MONGO_URI)
    # Create a new client and connect to the server
    client = MongoClient(MONGO_URI, server_api=ServerApi("1"))

    # Send a ping to confirm a successful connection
    try:
        client.admin.command("ping")
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

