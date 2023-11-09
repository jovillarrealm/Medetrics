import functools
from pathlib import Path
import pandas as pd
from sodapy import Socrata
from pandas import DataFrame
from pyarrow import feather
from pyarrow import csv
from datetime import datetime, date

@functools.lru_cache(maxsize=1)
def get_creds(file:str):

    #from Medetrics.settings import BASE_DIR
    from json import load as jload
    BASE_DIR = Path(__file__).resolve().parent
    with open(BASE_DIR / file) as socratica_secrets:
        credentials = jload(socratica_secrets)
        return credentials



def download_data(limit=50000):
    credentials = get_creds("socratica_secrets.json")
    # Unauthenticated client only works with public data sets. Note 'None'
    # in place of application token, and no username or password:
    client = Socrata("www.datos.gov.co", app_token= credentials['APP_TOKEN'])

    # Example authenticated client (needed for non-public datasets):
    # client = Socrata(www.datos.gov.co,
    #                  MyAppToken,
    #                  username="user@example.com",
    #                  password="AFakePassword")

    # First 10 results, returned as JSON from API / converted to Python list of
    # dictionaries by sodapy.
    results = client.get("gt2j-8ykr", limit=limit, select="id_de_caso, fecha_de_notificaci_n, departamento_nom, ciudad_municipio_nom, edad, unidad_medida, sexo, fuente_tipo_contagio, ubicacion, estado, recuperado")
    
    # Convert to pandas DataFrame
    results_df = pd.DataFrame.from_records(results)
    #results_df['edad'] = results_df['edad'].astype("uint8[pyarrow]")
    
    
    #results_df = pa.
    return results_df


def download_feather(new_feather_path:Path):
    csv_path=new_feather_path.parent.parent/ "csv" / "covid_data.csv"
    if csv_path.is_file():
        last_modified_local = datetime.fromtimestamp(csv_path.stat().st_mtime).date()
        if (date.today() - last_modified_local).days > 15:
            df = download_data()
            df.to_csv(csv_path)
            print(f"Se actualiza un csv {csv_path}")
        else:
            df = csv.read_csv(csv_path)
    else:
        df = download_data()
        df.to_csv(csv_path)
        print(f"Se descarga un csv {csv_path}")
    feather.write_feather(df=df, dest=new_feather_path)
    print(f"Nuevo dataset {new_feather_path}")
    df = feather.read_feather(new_feather_path)
    return df


def get_dataset():
    # Check if file exists and is up to date
    file = "covid_data"
    new_feather_file = file + ".feather"
    BASE_DIR = Path(__file__).resolve().parent
    new_feather_path = BASE_DIR / "datasets" / new_feather_file
    full_path=new_feather_path.parent.parent/ "csv" / "Casos_positivos_de_COVID-19_en_Colombia._20231013.csv"
    if full_path.is_file():
        print("usando el dataset entero")
        if new_feather_path.is_file():
            df: DataFrame = feather.read_feather(new_feather_path)
        else:
            df = csv.read_csv(full_path)
            feather.write_feather(df =df,dest=new_feather_path)
            df: DataFrame = feather.read_feather(new_feather_path)
    else:
        if new_feather_path.is_file():
            last_modified_local = datetime.fromtimestamp(new_feather_path.stat().st_mtime).date()
            if (date.today() - last_modified_local).days > 1:
                df = download_feather(new_feather_path)
            df: DataFrame = feather.read_feather(new_feather_path)
        else:
            df = download_feather(new_feather_path)
            print(f"Hubo que descargar archivos de covid en {new_feather_path}")
    return df