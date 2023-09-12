from pymongo.database import Database
from reportes.mongo_data import get_db

def send_report(report: dict[str, str], db: Database=get_db(), collection: str= "reportes")->bool:
    """Esta función va a enviar un reporte a la base de datos"""
    reported = db[collection].insert_one(report).acknowledged
    return reported


def get_mock_data( db: Database=get_db(), collection: str= "mock_data"):
    curse =db[collection].find()
    print(curse)
    return curse
