import yaml
from extract import extract
from load import load
from transform import clean_data

if __name__ == "__main__":
    with open("../config/config.yaml", 'r') as file:
        config = yaml.safe_load(file)
    df, df_secondary = extract(config)  # Unpack the tuple
    df = clean_data(df, df_secondary, config, config['place_mapping'])
    load(df, config)

    # print(df.head())  # Print DataFrame head for debugging
    # print(df.info())  # Print DataFrame info for debugging

    