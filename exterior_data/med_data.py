import pandas as pd
from pandas import DataFrame
import requests
import plotly.express as px
import plotly.offline as opy
from pathlib import Path
from datetime import datetime, date
from pyarrow import csv
from pyarrow import feather
import functools

dengue_id = "Dengue"
meningitis_id = "Meningitis por haemophilus influenzae"
viruela_simica_id = "Casos positivos de Viruela símica"
vih_id = "VIH - SIDA"

@functools.lru_cache(maxsize=1)
def chart_dengue():
    df = get_dataset(dengue_id)
    
    v = "edad_"
    color = "sexo_"
    title = f"Distribución de edad en Dengue ({df.shape[0]} casos)"
    x_axis = "Edad"
    y_axis = "Número de casos"
    
    textos = title, x_axis, y_axis
    edad_plot_div = create_histogram(df, v, color, textos)

    v = "year_"
    color = "sexo_"
    title = f"Distribución de número de casos de Dengue por año  ({df.shape[0]} casos)"
    x_axis = "Año de diagnósis"
    y_axis = "Número de casos"
    textos = title, x_axis, y_axis
    ano_plot_div = create_histogram(df, v, color, textos)
        
    v = "comuna"
    color = "sexo_"
    title = f"Distribución de número de casos de Dengue por comuna ({df.shape[0]} casos)"
    x_axis = "Comuna"
    y_axis = "Número de casos"
    textos = title, x_axis, y_axis
    comuna_plot_div = create_histogram(df, v, color, textos)

    v = "pac_hos_"
    color = "sexo_"
    title = f"Distribución de pacientes hospitalizados por Dengue ({df.shape[0]} casos)"
    x_axis = "Pacientes hospitalizados"
    y_axis = "Número de casos"
    replace_value = lambda pac: "Hospitalizado" if pac == 1 else "No hospitalizado"
    df[v] = df[v].apply(replace_value)
    textos = title, x_axis, y_axis
    hospitalizado_plot_div = create_histogram(df, v, color, textos)

    return edad_plot_div, ano_plot_div, comuna_plot_div, hospitalizado_plot_div

@functools.lru_cache(maxsize=1)
def chart_vih():
    df = get_dataset(vih_id)

    v = "edad_"
    color = "sexo_"
    title = f"Distribución de edad en VIH ({df.shape[0]} casos)"
    x_axis = "Edad"
    y_axis = "Número de casos"
    textos = title, x_axis, y_axis
    edad_plot_div = create_histogram(df, v, color, textos)

    # Sort the DataFrame by 'año'
    v = "año"
    color = "sexo_"
    title = f"Distribución de número de casos por año VIH ({df.shape[0]} casos)"
    x_axis = "Año de diagnósis"
    y_axis = "Número de casos"
    textos = title, x_axis, y_axis
    ano_plot_div = create_histogram(df, v, color, textos)

    v = "estrato_"
    ef = df[df[v] != 999]
    color = "sexo_"
    title= (
        f"Número de casos por Estrato en VIH ({df.shape[0]} casos)"
    )
    x_axis = "Estrato"
    y_axis = "Número de casos"
    textos = title, x_axis, y_axis
    estrato_plot_div = create_histogram(ef, v, color, textos)

    v = "nombre_comuna"
    color = "sexo_"
    title = f"Distribución de número de casos por comuna {meningitis_id} ({df.shape[0]} casos)"
    x_axis = "Comuna"
    y_axis = "Número de casos"
    textos = title, x_axis, y_axis
    comuna_plot_div = create_histogram(df, v, color, textos)
    
    return edad_plot_div, ano_plot_div, estrato_plot_div, comuna_plot_div


@functools.lru_cache(maxsize=1)
def chart_viruela_sim():
    df = get_dataset(viruela_simica_id)
    
    v = "edad"
    color = "sexo"
    title = f"Distribución de edad en Viruela Símica ({df.shape[0]} casos)"
    x_axis = "Edad"
    y_axis = "Número de casos"
    textos = title, x_axis, y_axis
    edad_plot_div = create_histogram(df, v, color, textos)

    # Sort the DataFrame by 'año'
    v = "a_o"
    color = "sexo"
    title = (
        f"Distribución de número de casos por año Viruela Símica ({df.shape[0]} casos)"
    )
    x_axis = "Año de diagnósis"
    y_axis = "Número de casos"
    textos = title, x_axis, y_axis
    ano_plot_div = create_histogram(df, v, color, textos)

    ef = df[df['estrato'] != 999]
    v = "estrato"
    color = "sexo"
    title= (
        f"Número de casos por Estrato en Viruela Símica ({df.shape[0]} casos)"
    )
    x_axis = "Estrato"
    y_axis = "Número de casos"
    textos = title, x_axis, y_axis
    estrato_plot_div = create_histogram(ef, v, color, textos)

    v = "hospitalizacion"
    color = "sexo"
    title = f"Distribución de pacientes hospitalizados con Viruela Símica ({df.shape[0]} casos)"
    x_axis = "Pacientes hospitalizados"
    y_axis = "Número de casos"
    replace_value = lambda pac: "Hospitalizado" if pac == 1 else "No hospitalizado"
    df[v] = df[v].apply(replace_value)
    textos = title, x_axis, y_axis
    hospitalizado_plot_div = create_histogram(df, v, color, textos)

    return edad_plot_div, ano_plot_div, estrato_plot_div, hospitalizado_plot_div

@functools.lru_cache(maxsize=1)
def chart_meningitis():
    df = get_dataset(meningitis_id)
    v = "edad_"
    color = "sexo_"
    title = f"Distribución de edad en {meningitis_id} ({df.shape[0]} casos)"
    x_axis = "Edad"
    y_axis = "Número de casos"
    textos = title, x_axis, y_axis
    edad_plot_div = create_histogram(df, v, color, textos)

    # Sort the DataFrame by 'año'
    v = "year_"
    color = "sexo_"
    title = f"Distribución de número de casos por año en {meningitis_id} ({df.shape[0]} casos)"
    x_axis = "Año de diagnósis"
    y_axis = "Número de casos"
    textos = title, x_axis, y_axis
    ano_plot_div = create_histogram(df, v, color, textos)

    v = "comuna"
    color = "sexo_"
    title = f"Distribución de número de casos por comuna {meningitis_id} ({df.shape[0]} casos)"
    x_axis = "Comuna"
    y_axis = "Número de casos"
    textos = title, x_axis, y_axis
    comuna_plot_div = create_histogram(df, v, color, textos)
   
    v = "pac_hos_"
    color = "sexo_"
    title = f"Distribución de pacientes hospitalizados {meningitis_id} ({df.shape[0]} casos)"
    x_axis = "Pacientes hospitalizados"
    y_axis = "Número de casos"
    replace_value = lambda pac: "Hospitalizado" if pac == 1 else "No hospitalizado"
    df[v] = df[v].apply(replace_value)
    textos = title, x_axis, y_axis
    hospitalizado_plot_div = create_histogram(df, v, color, textos)
   
    return edad_plot_div, ano_plot_div, hospitalizado_plot_div, comuna_plot_div 

def create_histogram(df: DataFrame, ordered_var: str, color: str, texts):
    # Sort the DataFrame by 'edad'
    df = df.sort_values(by=ordered_var)

    # Create a custom ordering for the 'edad' column
    uniques_var = df[ordered_var].unique()
    var_order = sorted(uniques_var)

    # Create a histogram
    fig = px.histogram(
        df,
        x=ordered_var,
        color=color,
        category_orders={ordered_var: var_order},
        barmode="group",
    )
    title, x, y = texts
    # Customize the plot
    fig.update_layout(
        title=title,
        xaxis_title=x,
        yaxis_title=y,
    )
    # Display the plot
    plot_div = opy.plot(fig, auto_open=False, output_type="div")

    return plot_div


def create_interactive_histogram(df: DataFrame, ordered_var: str, color: str, texts):
    pass


def get_dataset(id):
    # Load .feather de
    BASE_DIR = Path(__file__).resolve().parent
    enfermedades = {
        dengue_id: "sivigila_dengue",
        meningitis_id: "meningitis_por_haemophilus_influenzae",
        vih_id: "sivigila_vih",
        viruela_simica_id: "casos_positivos_viruela_simica",
    }
    file = enfermedades[id] + ".feather"
    try:
        df: DataFrame = feather.read_feather(BASE_DIR / "datasets" / file)
    except:
        get_dataset_remote(id)
        df: DataFrame = feather.read_feather(BASE_DIR / "datasets" / file)
    return df


def save_feather(new_file_path, new_feather_path):
    parse_options = csv.ParseOptions(delimiter=";")
    df = csv.read_csv(input_file=new_file_path, parse_options=parse_options)
    feather.write_feather(df=df, dest=new_feather_path)


def download_file(url, file_name, new_file_path):
    print(f"Se va a descargar {file_name}")
    r = requests.get(url, allow_redirects=True)
    with open(new_file_path, "wb") as new_file:
        new_file.write(r.content)


def get_dataset_remote(id):
    resource_url = f"http://medata.gov.co/api/3/action/package_show?id={id}"
    resource_response = requests.get(resource_url).json()["result"][0]["resources"][0]

    url: str = resource_response["url"]
    file_name = url.split("/")[-1]
    last_modified_remote_str = resource_response["last_modified"].split(",")[1].lstrip()
    format_string = "%m/%d/%Y - %H:%M"
    last_modified_remote = datetime.strptime(last_modified_remote_str, format_string).date()

    BASE_DIR = Path(__file__).resolve().parent
    new_file_path: Path = BASE_DIR / "csv" / file_name

    if new_file_path.is_file():
        last_modified_local = datetime.fromtimestamp(new_file_path.stat().st_mtime).date()
        
        if last_modified_remote > last_modified_local:
            # Si tenemos el archivo descargado y han actualizado los recursos, descargamos
            print(
                f"Se va a actualizar el recurso {file_name} que venía desde {last_modified_local} a {last_modified_remote}"
            )
            download_file(url, file_name, new_file_path)
        else:
            print(f"No hay que hacer nada con {file_name}")
    else:
        print(f"Se va a descargar el recurso {file_name}")
        download_file(url, file_name, new_file_path)

    new_feather_file = file_name.split(".")[0] + ".feather"
    new_feather_path: Path = BASE_DIR / "datasets" / new_feather_file

    if new_feather_path.exists():
        last_modified_local = datetime.fromtimestamp(new_feather_path.stat().st_mtime)
        if last_modified_remote > last_modified_local:
            print(f"Se va a actualizar el csv en {new_feather_file}")
            save_feather(new_file_path, new_feather_path)
        else:
            print(f" No hay que hacer nada con {new_feather_file}")
    else:
        print(f"Se va a transformar el csv en {new_feather_file}")
        save_feather(new_file_path, new_feather_path)
    try:
        pass
    except:
        print(f"Hubo un error tratando de obtener el recurso para {id}")
