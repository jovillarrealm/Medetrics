import functools
from pathlib import Path

import pandas as pd
from sodapy import Socrata
import plotly.express as px
import plotly.offline as opy
from pandas import DataFrame
@functools.lru_cache(maxsize=1)
def get_creds(file:str):

    #from Medetrics.settings import BASE_DIR
    from json import load as jload
    BASE_DIR = Path(__file__).resolve().parent.parent
    #with open(BASE_DIR / "exterior_data" / file) as socratica_secrets:
    with open(BASE_DIR / "exterior_data" / file) as socratica_secrets:
        credentials = jload(socratica_secrets)
        return credentials





@functools.lru_cache(maxsize=1)
def download_data():
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
    results = client.get("gt2j-8ykr", limit=5, select="id_de_caso, fecha_de_notificaci_n, departamento_nom, ciudad_municipio_nom, edad, unidad_medida, sexo, fuente_tipo_contagio, ubicacion, estado, recuperado")

    # Convert to pandas DataFrame
    results_df = pd.DataFrame.from_records(results)
    return results_df

results_df = download_data()

def chart_edad(results_df:DataFrame= results_df):
    # Create a histogram
    fig = px.histogram(results_df, x='edad', color='sexo', barmode='group')

    # Customize the plot
    fig.update_layout(title='Distribución de edades de casos de COVID-19', xaxis_title='Edad', yaxis_title='Número de casos')

    # Display the plot
    plot_div = opy.plot(fig, auto_open=False, output_type='div')

    #fig.show()
    return plot_div

def chart_lugar(results_df:DataFrame= results_df):
    fig = px.histogram(results_df, x='edad', color='sexo', barmode='group')

    # Customize the plot
    fig.update_layout(title='Distribución de edades de casos de COVID-19', xaxis_title='Edad', yaxis_title='Número de casos')

    # Display the plot
    plot_div = opy.plot(fig, auto_open=False, output_type='div')

    #fig.show()
    return plot_div