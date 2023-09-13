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
def get_mock_data(db: Database = get_db(), collection: str = "mock_data") :
    curse = list(db[collection].find())
    pack = lambda field: (field, field)
    packlist = lambda a, b, c: (tuple(map(pack,a)), tuple(map(pack,b)), tuple(map(pack,c)))
    return packlist(
        curse[0]["disease"],
        curse[0]["municipios"],
        curse[0]["medellin_barrios"],
    )
