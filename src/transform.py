import pandas as pd
import re
import requests
import random


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

# Function to drop unnecessary fields from the DataFrame
def drop_fields(df, fields_to_drop=None):
    if fields_to_drop is None:
        fields_to_drop = ['Extent', 'Description']  # Default field(s) to drop
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
    #  print the unique ids of the columns that were dropped
    dropped_columns = df.columns[df.isnull().mean() > threshold].tolist()
    if dropped_columns:
        print("Dropped columns due to high missing data:", dropped_columns)
    else:
        print("No columns dropped due to missing data.")
    return df

# Function to handle missing values in specific columns
def handle_missing(df):
   
    # df['Description'] = df['Description'].replace('', 'No Description')
    # df['Issn'] = df['Issn'].replace('', None)
    
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
def standardize_places(df):
    # Print unique entries in the 'Place' column
    if 'Place' in df.columns:
        unique_places = df['Place'].unique()
        print("Unique entries in 'Place' column:", unique_places)
    # df['place'] = df['place'].replace(place_mapping)
    return df



# Single function to run all cleaning steps in order
def clean_data(df, config):
    df = standardize_column_names(df)
    df = create_unique_id(df, config['id_prefix_length'])
    df = create_issn(df)
    df = drop_fields(df, ['Extent', 'Description'])
    df = drop_empty_columns(df, config.get('empty_column_threshold', 0.5))
    df = convert_dates(df)
    df = handle_missing(df)
    df = remove_duplicates(df)
    df = clean_fields(df)
    df = trim_whitespace(df)
    df = standardize_places(df)
    return df
