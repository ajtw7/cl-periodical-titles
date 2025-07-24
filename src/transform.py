import pandas as pd
import re




# Function to convert date columns to datetime format
def convert_dates(df):
    df['start_date'] = pd.to_datetime(df['start_date'], errors='coerce')
    df['end_date'] = pd.to_datetime(df['end_date'], errors='coerce')
    return df


# Function to handle missing values in specific columns
def handle_missing(df):
    df['description'] = df['description'].replace('', 'No description')
    df['ISSN'] = df['ISSN'].replace('', None)
    return df

# Function to validate ISSN format
def validate_issn(df):
    issn_pattern = re.compile(r'^\d{4}-\d{3}[\dX]$')
    df['ISSN_valid'] = df['ISSN'].apply(lambda x: bool(issn_pattern.match(str(x))) if x else False)
    return df

# Function to remove duplicate entries based on 'id' column
def remove_duplicates(df):
    df = df.drop_duplicates(subset=['id'])
    return df

# Function to truncate 'id' field by removing a specified prefix length
def truncate_ids(df, prefix_length):
    df['id'] = df['id'].apply(lambda x: x[prefix_length:] if isinstance(x, str) else x)
    return df

# Function to clean 'place' field by removing digits and extra spaces
def clean_fields(df):
    df['place'] = df['place'].apply(lambda x: re.sub(r'\d+', '', x).strip() if isinstance(x, str) else x)
    return df

# Function to trim whitespace from all string fields in the DataFrame
def trim_whitespace(df):
    for col in df.select_dtypes(include='object').columns:
        df[col] = df[col].str.strip()
    return df

# Function to standardize place names using a mapping dictionary
def standardize_places(df, place_mapping):
    df['place'] = df['place'].replace(place_mapping)
    return df



# Single function to run all cleaning steps in order
def clean_data(df, config):
    df = convert_dates(df)
    df = handle_missing(df)
    df = validate_issn(df)
    df = remove_duplicates(df)
    df = truncate_ids(df, config['id_prefix_length'])
    df = clean_fields(df)
    df = trim_whitespace(df)
    df = standardize_places(df, config['place_mapping'])
    return df
