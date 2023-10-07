from pymongo.database import Database
from persistencia.mongo_data import get_db
import functools


def send_report(
    report: dict[str, str], db: Database = get_db(), collection: str = "reportes"
) -> bool:
    """Esta función va a enviar un reporte a la base de datos"""
    reported = db[collection].insert_one(report).acknowledged
    return reported

@functools.lru_cache(maxsize=1)
def get_input_data(db: Database = get_db(), collection: str = "reportes"):
    enfermedades = ["Enfermedades"]+ db[collection].distinct("disease")
    municipio = ["Municipio"]+ db[collection].distinct("municipio")
    barrio = ["Barrio"]+ db[collection].distinct("barrio")
    pack = lambda li: ((field, field) for field in li)
    listpack= lambda li: (pack(i) for i in li)
    return listpack((enfermedades, municipio, barrio))



