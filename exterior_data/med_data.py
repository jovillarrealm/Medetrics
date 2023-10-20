from pandas import DataFrame
import requests

from pathlib import Path
from datetime import datetime, date
from pyarrow import csv
from pyarrow import feather
import statsmodels.api as sm
from exterior_data.ids import *





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
