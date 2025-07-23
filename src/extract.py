import pandas as pd
import yaml
import os


def extract(config):
    df = pd.read_csv(config['source_path'], encoding='utf-8', dtype=str, keep_default_na=False)
    return df

def load(df, config):
    # Ensures the output path exists
    output_path = os.path.dirname(config['processed_path'])
    if output_path and not os.path.exists(output_path):
        os.makedirs(output_path)
    df.to_csv(config['processed_path'], index=False, encoding='utf-8')
    # Print a message indicating the ETL process is complete
    print("ETL process completed. Output saved to:", config['processed_path'])

if __name__ == "__main__":
    #  Load config
    with open("../config/config.yaml", 'r') as file:
        config = yaml.safe_load(file)
    # Extract data
    df = extract(config)
    # Load data
    load(df, config)

