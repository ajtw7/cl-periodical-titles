import os


def load(df, config):
    # Ensures the output path exists
    output_path = os.path.dirname(config['processed_path'])
    if output_path and not os.path.exists(output_path):
        os.makedirs(output_path)
    df.to_csv(config['processed_path'], index=False, encoding='utf-8')
    # Print a message indicating the ETL process is complete
    print("ETL process completed. Output saved to:", config['processed_path'])