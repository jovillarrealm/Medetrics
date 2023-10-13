import pandas as pd
from pandas import DataFrame
import requests
import plotly.express as px
import plotly.offline as opy
from pathlib import Path
from datetime import datetime
from pyarrow import csv
from pyarrow import feather


dengue_id = "Dengue"
meningitis_id = "Meningitis por haemophilus influenzae"
viruela_simica = "Casos positivos de Viruela símica"
vih_id = "VIH - SIDA"

def chart_dengue():
    df = get_dataset(dengue_id)
    # Sort the DataFrame by 'edad'
    df = df.sort_values(by="edad_")

    # Create a custom ordering for the 'edad' column
    unique_edades = df["edad_"].unique()
    edad_order = sorted(unique_edades)

    # Create a histogram
    fig = px.histogram(
        df,
        x="edad_",
        color="sexo_",
        category_orders={"edad_": edad_order},
        barmode="group",
    )

    # Customize the plot
    fig.update_layout(
        title=f"Distribución de edades de casos de Dengue ({df.shape[0]} casos)",
        xaxis_title="Edad",
        yaxis_title="Número de casos",
    )

    # Display the plot
    plot_div = opy.plot(fig, auto_open=False, output_type="div")
    return plot_div


def chart_vih():
    df = get_dataset(vih_id)
    v = "edad_"
    color="sexo_"
    title = f"Distribución de edad en VIH ({df.shape[0]} casos)"
    x_axis = "Edad"
    y_axis = "Número de casos"
    textos = title, x_axis, y_axis
    edad_plot_div = create_histogram(df,v,color,textos)

    # Sort the DataFrame by 'año'
    v = "año"
    color="sexo_"
    title=f"Distribución de número de casos por año VIH ({df.shape[0]} casos)"
    xaxis_title="Año de diagnósis"
    yaxis_title="Número de casos"
    textos = title, x_axis, y_axis
    ano_plot_div= create_histogram(df,v,color, textos)
    return edad_plot_div, ano_plot_div


def create_histogram(df:DataFrame, ordered_var: str, color:str, texts):
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
    print(texts)
    # Customize the plot
    fig.update_layout(
        title=title,
        xaxis_title=x,
        yaxis_title=y,
    )
    # Display the plot
    plot_div = opy.plot(fig, auto_open=False, output_type="div")

    return plot_div


def create_interactive_histogram(df:DataFrame, ordered_var: str, color:str, texts):
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
    print(texts)
    # Customize the plot
    fig.update_layout(
        title=title,
        xaxis_title=x,
        yaxis_title=y,
    )
    # Display the plot
    plot_div = opy.plot(fig, auto_open=False, output_type="div")

    return plot_div


def get_dataset(id):
    # Load .feather de
    BASE_DIR = Path(__file__).resolve().parent
    enfermedades = {
        dengue_id: "sivigila_dengue",
        meningitis_id: "meningitis_por_haemophilus_influenzae",
        vih_id: "sivigila_vih",
        viruela_simica: "casos_positivos_viruela_simica",
    }
    file = enfermedades[id] + ".feather"
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
    last_modified_remote = datetime.strptime(last_modified_remote_str, format_string)

    BASE_DIR = Path(__file__).resolve().parent
    new_file_path: Path = BASE_DIR / "csv" / file_name

    if new_file_path.is_file():
        last_modified_local = datetime.fromtimestamp(new_file_path.stat().st_mtime)
        if last_modified_remote > last_modified_local:
            # Si tenemos el archivo descargado y han actualizado los recursos, descargamos
            download_file(url, file_name, new_file_path)
        else:
            print(f"No hay que hacer nada con {file_name}")
    else:
        download_file(url, file_name, new_file_path)

    new_feather_file = file_name.split(".")[0] + ".feather"
    new_feather_path: Path = BASE_DIR / "datasets" / new_feather_file

    if new_feather_path.exists():
        last_modified_local = datetime.fromtimestamp(new_feather_path.stat().st_mtime)
        if last_modified_remote > last_modified_local:
            save_feather(new_file_path, new_feather_path)
        else:
            print(f" No hay que hacer nada con {new_feather_file}")
    else:
        save_feather(new_file_path, new_feather_path)
    try:
        pass
    except:
        print(f"Hubo un error tratando de obtener el recurso para {id}")
