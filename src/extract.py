import pandas as pd


def extract(config):
    df = pd.read_csv(config['source_path'], encoding='utf-8', dtype=str, keep_default_na=False)
    df_secondary = pd.read_csv(config['secondary_source_path'], encoding='utf-8', dtype=str, keep_default_na=False)
    return df, df_secondary


