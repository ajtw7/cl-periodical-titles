import os
import platform
import subprocess


def load(df, config):
    # Ensures the output path exists
    output_path = os.path.dirname(config['processed_path'])
    if output_path and not os.path.exists(output_path):
        os.makedirs(output_path)
    df.to_csv(config['processed_path'], index=False, encoding='utf-8')
    # Print a message indicating the ETL process is complete
    print("ETL process completed. Output saved to:", config['processed_path'])


     # Automatically open the CSV file
    try:
        if platform.system() == "Darwin":  # macOS
            subprocess.call(["open", config['processed_path']])
        elif platform.system() == "Windows":  # Windows
            os.startfile(config['processed_path'])
        elif platform.system() == "Linux":  # Linux
            subprocess.call(["xdg-open", config['processed_path']])
        else:
            print("Automatic file opening is not supported on this platform.")
    except Exception as e:
        print(f"Failed to open the file automatically: {e}")