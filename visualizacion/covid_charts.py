from exterior_data.covid_data import get_dataset
import plotly.express as px
import plotly.offline as opy
from pandas import DataFrame
import functools

@functools.lru_cache(maxsize=1)
def covid_charts(ttl:int)->tuple:
    del ttl
    # Sort the DataFrame by 'edad'
    df = get_dataset()

    v = "edad"
    color = "sexo"
    title = f"Distribución de edad en COVID-19 ({df.shape[0]} casos)"
    x_axis = "Edad"
    y_axis = "Número de casos"

    textos = title, x_axis, y_axis
    edad_plot_div = create_histogram(df, v, color, textos)

    v = "ciudad_municipio_nom"
    color = "sexo"
    title = f"Distribución por ciudad: COVID-19 ({df.shape[0]} casos)"
    x_axis = "Ciudad"
    y_axis = "Número de casos"

    textos = title, x_axis, y_axis
    ciudad_plot_div = create_histogram(df, v, color, textos)

    
    v = "departamento_nom"
    color = "sexo"
    title = f"Distribución por departamento: COVID-19 ({df.shape[0]} casos)"
    x_axis = "Departamento"
    y_axis = "Número de casos"

    textos = title, x_axis, y_axis
    depto_plot_div = create_histogram(df, v, color, textos)
    
    return edad_plot_div, ciudad_plot_div,depto_plot_div

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
