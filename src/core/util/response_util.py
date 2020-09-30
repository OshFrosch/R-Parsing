import pandas as pd


def convert_response_to_dataframe(response_json):
    return pd.json_normalize(response_json)
