from pyarrow import csv
from pyarrow import feather
def save_feather(new_file_path, new_feather_path):
    parse_options = csv.ParseOptions(delimiter=",")
    df = csv.read_csv(input_file=new_file_path, parse_options=parse_options)
    feather.write_feather(df=df, dest=new_feather_path)

save_feather("Casos_positivos_de_COVID-19_en_Colombia._20231013.csv", "covid_big_data.feather" )