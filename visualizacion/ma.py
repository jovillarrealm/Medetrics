from pathlib import Path
from json import load as jload
import functools
from exterior_data.med_data import get_dataset
import exterior_data.ids as ids


@functools.lru_cache(maxsize=1)
def get_mapbox_token():
    BASE_DIR = Path(__file__).resolve().parent
    with open(BASE_DIR / "mapbox.json") as map_box_secret:
        credentials = jload(map_box_secret)
        return credentials["MAP_BOX_TOKEN"]


def build_comunas():
    df_meningitis = get_dataset(ids.meningitis_id)
    df_dengue = get_dataset(ids.dengue_id)

    # print(df_dengue.groupby(by=["comuna"]).size())

    # print(df_meningitis.groupby(by=["comuna"]).size())

    comunas = {
        "Comuna 1 - Popular": [6.255417, -75.578611],
        "Comuna 2 - Santa Cruz": [6.241111, -75.567222],
        "Comuna 3 - Manrique": [6.244167, -75.555278],
        "Comuna 4 - Aranjuez": [6.227778, -75.552222],
        "Comuna 5 - Castilla": [6.226944, -75.541389],
        "Comuna 6 - Doce de Octubre": [6.224722, -75.531667],
        "Comuna 7 - Robledo": [6.227778, -75.521944],
        "Comuna 8 - Villa Hermosa": [6.237222, -75.513333],
        "Comuna 9 - Buenos Aires": [6.246667, -75.506944],
        "Comuna 10 - La Candelaria": [6.258333, -75.506667],
        "Comuna 11 - Laureles-Estadio": [6.263333, -75.516667],
        "Comuna 12 - La América": [6.266667, -75.528056],
        "Comuna 13 - San Javier": [6.268056, -75.538056],
        "Comuna 14 - Belen": [6.270278, -75.548056],
        "Comuna 15 - Guayabal": [6.272222, -75.558056],
        "Comuna 16 - El Poblado": [6.274167, -75.568056],
    }

    for i in comunas:
        comunas[i].reverse()
        comunas[i] = [comunas[i]]

    for comuna_df, casos_df in df_dengue.groupby(by=["comuna"]).size().items():
        for i in comunas:
            if comuna_df in i:
                comunas[i].append(f"Casos dengue: {casos_df}")

    for comuna_df, casos_df in df_meningitis.groupby(by=["comuna"]).size().items():
        for i in comunas:
            if comuna_df in i:
                if isinstance(comunas[i][1], str):
                    comunas[i] = [
                        comunas[i][0],
                        comunas[i][1] + f"Casos meningitis: {casos_df}",
                    ]
                else:
                    comunas[i] = [comunas[i][0], f"Casos meningitis: {casos_df}"]


    resultado = [
        {
            "nombre": f"{k}",
            "coordenadas": v[0],
            "descripcion": v[1],
        }
        if len(v)>1
        else {
            "nombre": f"{k}",
            "coordenadas": v[0],
        }
        for k, v in comunas.items()
    ]

    return resultado
