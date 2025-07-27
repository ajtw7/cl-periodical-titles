# from logging import config
import pandas as pd
import re
import random


# function to merge issues and titles CSV files
def merge_dataframes(df, df_secondary):
    if 'Id' not in df.columns or 'Title Id' not in df_secondary.columns:
        raise ValueError("Merge keys 'Id' or 'Title Id' are missing in the datasets.")
    return pd.merge(df, df_secondary, left_on='Id', right_on='Title Id', how='left')


# Function to standardize column names by replacing underscores with spaces and capitalizing
# the first letter of each word
def standardize_column_names(df):
    df.columns = [col.replace('_', ' ').title() for col in df.columns]
    return df

# Function to create a new column 'Id (no prefix)' by removing the first 5 characters from 'Id'
def create_unique_id(df, id_prefix_length):
    df['Unique Id'] = df['Id'].apply(lambda x: x[id_prefix_length:] if isinstance(x, str) else x)
    return df

def create_issn(df):
    # Check if 'Issn' column exists, if not create it
    if 'Issn' not in df.columns:
        df['Issn'] = None
    # Generate ISSN numbers directly in the 'Issn' column for missing, null, or empty values
    df['Issn'] = df['Issn'].apply(lambda x: f"{random.randint(1000, 9999)}-{random.randint(1000, 9999)}" if pd.isnull(x) or x == '' else x)
    return df

def differentiate_types(df):
    # Add a column to differentiate between Titles and Issues based on the presence of 'Title Id'
    if 'Title Id' in df.columns:
        df['Type'] = df['Title Id'].apply(lambda x: 'Issue' if pd.notnull(x) else 'Title')
    else:
        raise ValueError("Column 'Title Id' is missing in the dataset.")
    return df

# Function to drop unnecessary fields from the DataFrame
def drop_fields(df, fields_to_drop=None):
    if fields_to_drop is None:
        fields_to_drop = ['Extent', 'Description', 'Text Download Url']  # Default field(s) to drop
    df = df.drop(columns=[field for field in fields_to_drop if field in df.columns])
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

def drop_empty_columns(df, threshold=0.5):
    threshold = len(df) * threshold  # Calculate the threshold based on the number of rows
    df = df.dropna(thresh=threshold, axis=1)
    return df

# Function to handle missing values in specific columns
def handle_missing(df):
    # Fill empty 'Start Year' with year from 'Start Date' if available
    if 'Start Year' in df.columns and 'Start Date' in df.columns:
        for idx, row in df.iterrows():
            if (not row['Start Year'] or str(row['Start Year']).strip() == '') and row['Start Date'] and str(row['Start Date']).strip() != '':
                try:
                    year = pd.to_datetime(row['Start Date'], errors='coerce').year
                    if pd.notnull(year):
                        df.at[idx, 'Start Year'] = str(year)
                except Exception:
                    pass
    return df


# Function to remove duplicate entries based on 'id' column
def remove_duplicates(df):
    df = df.drop_duplicates(subset=['Id'])
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
def standardize_places(df, place_mapping):
    # Replace Null or empty cells with "Australia"
    df['Place'] = df['Place'].fillna('Australia')  # Replace Null values
    df['Place'] = df['Place'].replace('', 'Australia')  # Replace empty strings
    df['Place'] = df['Place'].replace(place_mapping)

    return df

def remove_duplicate_columns(df):
    # Remove duplicate columns by keeping the first occurrence
    df = df.loc[:, ~df.columns.duplicated()]
    # Print the columns name of the removed duplicates
    removed_columns = df.columns[df.columns.duplicated()].tolist()
    if removed_columns:
        print("Removed duplicate columns:", removed_columns)
    else:
        print("No duplicate columns found.")
    return df



# Single function to run all cleaning steps in order
def clean_data(df, df_secondary, config, place_mapping):
    df = standardize_column_names(df)
    df_secondary = standardize_column_names(df_secondary)
    df = create_unique_id(df, config['id_prefix_length'])
    df = create_issn(df)
    df = drop_fields(df, ['Extent', 'Description'])
    df_secondary = drop_fields(df_secondary, ['Text Download Url'])
    df = drop_empty_columns(df, config.get('empty_column_threshold', 0.5))
    df = convert_dates(df)
    df = handle_missing(df)
    df = standardize_places(df, place_mapping)
    df = remove_duplicates(df)
    df = clean_fields(df)
    df = trim_whitespace(df)
    df_secondary = trim_whitespace(df_secondary)
    df = merge_dataframes(df, df_secondary)
    df = remove_duplicate_columns(df)
    df = differentiate_types(df)
    return df
