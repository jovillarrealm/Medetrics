from pymongo.database import Database
from reportes.mongo_data import get_db
import functools


def send_report(
    report: dict[str, str], db: Database = get_db(), collection: str = "reportes"
) -> bool:
    """Esta función va a enviar un reporte a la base de datos"""
    reported = db[collection].insert_one(report).acknowledged
    return reported


@functools.lru_cache(maxsize=1)
def get_input_data(db: Database = get_db(), collection: str = "mock_data"):
    curse = db[collection].find_one()
    pack = lambda field: (field, field)
    packlist = lambda a, b, c: [
        list(map(pack, a)),
        list(map(pack, b)),
        list(map(pack, c)),
    ]
    disease = ["Enfermedades"]+curse["disease"]
    municipios = ["Municipios"]+curse["municipios"]
    barrios = ["Barrios"]+curse["medellin_barrios"]
    result =  packlist(disease, municipios, barrios)
    return result
