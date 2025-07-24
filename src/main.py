import yaml
from extract import extract, load
from transform import clean_data

if __name__ == "__main__":
    with open("../config/config.yaml", 'r') as file:
        config = yaml.safe_load(file)
    df = extract(config)
    df = clean_data(df)
    load(df, config)