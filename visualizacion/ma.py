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
        "Comuna 1 - Popular": [6.2933437, -75.5448249],
        "Comuna 2 - Santa Cruz": [6.2969558, -75.5548517],
        "Comuna 3 - Manrique": [6.2750611, -75.545892],
        "Comuna 4 - Aranjuez": [6.2777235, -75.5625988],
        "Comuna 5 - Castilla": [6.2936989, -75.5682636],
        "Comuna 6 - Doce de Octubre": [6.297565, -75.5775562],
        "Comuna 7 - Robledo": [6.2790741, -75.5887669],
        "Comuna 8 - Villa Hermosa": [6.24579365, -75.5465954114156],
        "Comuna 9 - Buenos Aires": [6.2307786, -75.5565935],
        "Comuna 10 - La Candelaria": [6.2501021, -75.5679154],
        "Comuna 11 - Laureles-Estadio": [6.2492382, -75.5886543],
        "Comuna 12 - La América": [6.2507013, -75.6079043],
        "Comuna 13 - San Javier": [6.2562742, -75.6215434],
        "Comuna 14 - El Poblado": [6.2010917, -75.5656654],
        "Comuna 15 - Guayabal": [6.2175494, -75.5848914],
        "Comuna 16 - Belen": [6.2258758, -75.6004937],
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
