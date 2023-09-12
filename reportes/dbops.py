from pymongo.database import Database


def send_report(report: dict[str, str], db: Database, collection: str= "reportes")->bool:
    """Esta función va a enviar un reporte a la base de datos"""
    reported = db[collection].insert_one(report).acknowledged
    return reported




