import functools
from pathlib import Path
@functools.lru_cache(maxsize=1)
def get_creds(file:str):

    #from Medetrics.settings import BASE_DIR
    from json import load as jload
    BASE_DIR = Path(__file__).resolve().parent.parent
    #with open(BASE_DIR / "exterior_data" / file) as socratica_secrets:
    with open(BASE_DIR / "exterior_data" / file) as socratica_secrets:
        credentials = jload(socratica_secrets)
        return credentials

soc_creds = get_creds("socratica_secrets.json")


import pandas as pd
from sodapy import Socrata
import plotly.express as px

def download_data(credentials):
    # Unauthenticated client only works with public data sets. Note 'None'
    # in place of application token, and no username or password:
    client = Socrata("www.datos.gov.co", app_token= soc_creds['APP_TOKEN'])

    # Example authenticated client (needed for non-public datasets):
    # client = Socrata(www.datos.gov.co,
    #                  MyAppToken,
    #                  username="user@example.com",
    #                  password="AFakePassword")

    # First 10 results, returned as JSON from API / converted to Python list of
    # dictionaries by sodapy.
    results = client.get("gt2j-8ykr", limit=10, select="id_de_caso, fecha_de_notificaci_n, departamento_nom, ciudad_municipio_nom, edad, unidad_medida, sexo, fuente_tipo_contagio, ubicacion, estado, recuperado")

    # Convert to pandas DataFrame
    results_df = pd.DataFrame.from_records(results)
    print(results_df)

download_data(soc_creds)