import functools
from pathlib import Path

import pandas as pd
from sodapy import Socrata
import plotly.express as px
import plotly.offline as opy
from pandas import DataFrame
from pyarrow import feather
from pyarrow import csv
from datetime import datetime, date
import pyarrow as pa
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


@functools.lru_cache(maxsize=1)
def download_feather(new_feather_path:Path, last_modified = None):
    csv_path=new_feather_path.parent.parent/ "csv" / "covid_data.csv"
    if last_modified and last_modified >1:
        df = download_data()
        df.to_csv(csv_path)
        print(f"Se descargó un csv {csv_path}")
    df:DataFrame = csv.read_csv(csv_path)
    feather.write_feather(df=df, dest=new_feather_path)
    print(f"Nuevo dataset {new_feather_path}")
    return df

def get_dataset():
    # Load .feather de
    file = "covid_data"
    new_feather_file = file + ".feather"
    BASE_DIR = Path(__file__).resolve().parent
    new_feather_path = BASE_DIR / "datasets" / new_feather_file
    if new_feather_path.is_file():
        last_modified_local = datetime.fromtimestamp(new_feather_path.stat().st_mtime).date()
        df: DataFrame = feather.read_feather(new_feather_path)
        since = (date.today() - last_modified_local).days
        if since > 1:
            df = download_feather(new_feather_path, since)
    else:
        df = download_feather(new_feather_path)
        print(f"Hubo que descargar archivos de covid en {new_feather_path}")
        
    return df


def chart_edad():
    # Sort the DataFrame by 'edad'
    results_df = get_dataset()
    results_df = results_df.sort_values(by='edad')
    
    # Create a custom ordering for the 'edad' column
    unique_edades = results_df['edad'].unique()
    edad_order = sorted(unique_edades)

    # Create a histogram
    fig = px.histogram(results_df, x='edad', color='sexo', category_orders={"edad": edad_order}, barmode='group')

    # Customize the plot
    fig.update_layout(title=f'Distribución de edades de casos de COVID-19 ({results_df.shape[0]} casos)', xaxis_title='Edad', yaxis_title='Número de casos')

    # Display the plot
    plot_div = opy.plot(fig, auto_open=False, output_type='div')

    return plot_div


def chart_lugar():
    results_df = get_dataset()
    pass