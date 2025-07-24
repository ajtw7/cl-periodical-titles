import pandas as pd
import re



def standardize_column_names(df):
    df.columns = [col.replace('_', ' ').title() for col in df.columns]
    return df

# Function to convert date columns to datetime format
def convert_dates(df):
    # Convert to datetime
    df['Start Date'] = pd.to_datetime(df['Start Date'], errors='coerce')
    df['End Date'] = pd.to_datetime(df['End Date'], errors='coerce')
    # Format as 'Jan 01 2011'
    df['Start Date'] = df['Start Date'].dt.strftime('%b %d %Y')
    df['End Date'] = df['End Date'].dt.strftime('%b %d %Y')
    # Rename column
    return df


# Function to handle missing values in specific columns
def handle_missing(df):
    df['Description'] = df['Description'].replace('', 'No Description')
    df['Issn'] = df['Issn'].replace('', None)
    return df

# Function to validate ISSN format
def validate_issn(df):
    issn_pattern = re.compile(r'^\d{4}-\d{3}[\dX]$')
    df['issn_valid'] = df['Issn'].apply(lambda x: bool(issn_pattern.match(str(x))) if x else False)
    return df

# Function to remove duplicate entries based on 'id' column
def remove_duplicates(df):
    df = df.drop_duplicates(subset=['Id'])
    return df

# Function to truncate 'id' field by removing a specified prefix length
def truncate_ids(df, prefix_length):
    df['Id'] = df['Id'].apply(lambda x: x[prefix_length:] if isinstance(x, str) else x)
    return df

# Function to clean 'place' field by removing digits and extra spaces
def clean_fields(df):
    df['Place'] = df['Place'].apply(lambda x: re.sub(r'\d+', '', x).strip() if isinstance(x, str) else x)
    return df

# Function to trim whitespace from all string fields in the DataFrame
def trim_whitespace(df):
    for col in df.select_dtypes(include='object').columns:
        df[col] = df[col].str.strip()
    return df

# Function to standardize place names using a mapping dictionary
# def standardize_places(df, place_mapping):
#     df['place'] = df['place'].replace(place_mapping)
#     return df



# Single function to run all cleaning steps in order
def clean_data(df, config):
    df = standardize_column_names(df)
    df = convert_dates(df)
    df = handle_missing(df)
    df = validate_issn(df)
    df = remove_duplicates(df)
    df = truncate_ids(df, config['id_prefix_length'])
    df = clean_fields(df)
    df = trim_whitespace(df)
    # df = standardize_places(df, config['place_mapping'])
    return df
