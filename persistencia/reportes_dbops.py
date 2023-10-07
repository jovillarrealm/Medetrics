from pymongo.database import Database
from persistencia.mongo_data import get_db
import functools


def send_report(
    report: dict[str, str], db: Database = get_db(), collection: str = "reportes"
) -> bool:
    """Esta función va a enviar un reporte a la base de datos"""
    reported = db[collection].insert_one(report).acknowledged
    return reported


def get_input_data(db: Database = get_db(), collection: str = "reportes"):
    enfermedades = ["Enfermedades"]+ db[collection].distinct("disease")
    municipio = ["Municipio"]+ db[collection].distinct("municipio")
    barrio = ["Barrio"]+ db[collection].distinct("barrio")
    pack = lambda li: ((field, field) for field in li)
    listpack= lambda li: (pack(i) for i in li)
    return listpack((enfermedades, municipio, barrio))



# TODO Reemplazar con datos de DIVIPOLA
@functools.lru_cache(maxsize=1)
def t_input_data(db: Database = get_db(), collection: str = "mock_data"):
    # Requires the PyMongo package.
    # https://api.mongodb.com/python/current

    places = db["places"].aggregate(
        [
            {
                "$group": {
                    "_id": "$Departamento",
                    "municipios": {"$addToSet": "$Municipio"},
                }
            },
            {"$project": {"departamento": "$_id", "municipios": 1, "_id": 0}},
        ]
    )
    pack = lambda field: (field, field)
    packlist = lambda thing: [list(map(pack, i)) for i in thing]
    if places:
        disease = ["Enfermedades"] + places["disease"]
        municipios = ["Municipios"] + places["municipios"]
        barrios = ["Barrios"] + ["medellin_barrios"]
    else:
        disease = ["Enfermedades"]
        municipios = ["Municipios"]
        barrios = ["Barrios"]
    result = packlist((disease, municipios, barrios))
    return result
