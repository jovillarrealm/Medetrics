
from exterior_data.med_data import get_dataset
import functools
from pandas import DataFrame
import plotly.express as px
import plotly.offline as opy
from exterior_data.ids import *



@functools.lru_cache(maxsize=1)
def chart_dengue(ttl):
    del ttl
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
    title = f"Distribución de número de casos Dengue por año  ({df.shape[0]} casos)"
    x_axis = "Año de diagnósis"
    y_axis = "Número de casos"
    textos = title, x_axis, y_axis
    ano_plot_div = create_histogram(df, v, color, textos)
        
    v = "comuna"
    color = "sexo_"
    title = f"Distribución de número de casos Dengue por comuna ({df.shape[0]} casos)"
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
def chart_vih(ttl):
    del ttl
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
    title = f"Distribución de número de casos VIH por año  ({df.shape[0]} casos)"
    x_axis = "Año de diagnósis"
    y_axis = "Número de casos"
    textos = title, x_axis, y_axis
    ano_plot_div = create_histogram(df, v, color, textos)

    v = "estrato_"
    ef = df[df[v] != 999]
    color = "sexo_"
    title= (
        f"Número de casos VIH por Estrato ({df.shape[0]} casos)"
    )
    x_axis = "Estrato"
    y_axis = "Número de casos"
    textos = title, x_axis, y_axis
    estrato_plot_div = create_histogram(ef, v, color, textos)

    v = "nombre_comuna"
    color = "sexo_"
    title = f"Distribución de número de casos VIH por comuna ({df.shape[0]} casos)"
    x_axis = "Comuna"
    y_axis = "Número de casos"
    textos = title, x_axis, y_axis
    comuna_plot_div = create_histogram(df, v, color, textos)
    
    return edad_plot_div, ano_plot_div, estrato_plot_div, comuna_plot_div


@functools.lru_cache(maxsize=1)
def chart_viruela_sim(ttl):
    del ttl
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
        f"Distribución de número de casos Viruela Símica por año ({df.shape[0]} casos)"
    )
    x_axis = "Año de diagnósis"
    y_axis = "Número de casos"
    textos = title, x_axis, y_axis
    ano_plot_div = create_histogram(df, v, color, textos)

    ef = df[df['estrato'] != 999]
    v = "estrato"
    color = "sexo"
    title= (
        f"Número de casos Viruela Símica por Estrato({df.shape[0]} casos)"
    )
    x_axis = "Estrato"
    y_axis = "Número de casos"
    textos = title, x_axis, y_axis
    estrato_plot_div = create_histogram(ef, v, color, textos)

    v = "hospitalizacion"
    color = "sexo"
    title = f"Distribución de pacientes hospitalizados por Viruela Símica ({df.shape[0]} casos)"
    x_axis = "Pacientes hospitalizados"
    y_axis = "Número de casos"
    replace_value = lambda pac: "Hospitalizado" if pac == 1 else "No hospitalizado"
    df[v] = df[v].apply(replace_value)
    textos = title, x_axis, y_axis
    hospitalizado_plot_div = create_histogram(df, v, color, textos)

    return edad_plot_div, ano_plot_div, estrato_plot_div, hospitalizado_plot_div

@functools.lru_cache(maxsize=1)
def chart_meningitis(ttl):
    del ttl
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
    title = f"Distribución de número de casos {meningitis_id} por año ({df.shape[0]} casos)"
    x_axis = "Año de diagnósis"
    y_axis = "Número de casos"
    textos = title, x_axis, y_axis
    ano_plot_div = create_histogram(df, v, color, textos)

    v = "comuna"
    color = "sexo_"
    title = f"Distribución de número de casos {meningitis_id} por comuna ({df.shape[0]} casos)"
    x_axis = "Comuna"
    y_axis = "Número de casos"
    textos = title, x_axis, y_axis
    comuna_plot_div = create_histogram(df, v, color, textos)
   
    v = "pac_hos_"
    color = "sexo_"
    title = f"Distribución de pacientes hospitalizados por {meningitis_id} ({df.shape[0]} casos)"
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

