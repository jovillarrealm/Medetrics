import pandas as pd
def chart_custom(records):
    df = pd.DataFrame.from_records(records)
    print(df)
    print(df.dtypes)