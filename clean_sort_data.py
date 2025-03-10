import os
import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load the Excel file
excel_file = 'py input.xlsx'

try:
    df = pd.read_excel(excel_file)
    logging.info("Excel file loaded successfully.")
except Exception as e:
    logging.error(f"Error loading Excel file: {e}")
    exit()

# Function to clean, sort, and create new columns in the data
def clean_sort_create_columns(df):
    try:
        # Remove duplicates
        df.drop_duplicates(inplace=True)
        logging.info("Duplicates removed.")
        
        # Remove rows with totals
        df = df[~df.apply(lambda row: row.astype(str).str.contains('Total').any(), axis=1)]
        logging.info("Rows with totals removed.")
        
        # Fill missing values with 'Unknown'
        df.fillna('Unknown', inplace=True)
        logging.info("Missing values filled with 'Unknown'.")
        
        # Create new columns
        df['continent'] = 'Unknown'  # Replace with logic to determine continent if available
        df['country'] = df['Country Name']
        df['region'] = df['Region']
        df['state'] = 'Unknown'  # Replace with logic to determine state if available
        df['education institution'] = df['Education Institute']
        df['field of study'] = df['Field of Study']
        logging.info("New columns created.")
        
        # Sort data by continent, country, region, state, education institution, and field of study
        df.sort_values(by=['continent', 'country', 'region', 'state', 'education institution', 'field of study'], inplace=True)
        logging.info("Data sorted.")
        
        return df
    except Exception as e:
        logging.error(f"Error during data cleaning and sorting: {e}")
        exit()

# Clean, sort, and create new columns in the data
cleaned_df = clean_sort_create_columns(df)

# Get the directory of the initial Excel file
directory = os.path.dirname(os.path.abspath(excel_file))

# Save the cleaned and sorted data to a new Excel file in the same directory
output_file = os.path.join(directory, 'cleaned_sorted_py_input_with_columns.xlsx')

try:
    cleaned_df.to_excel(output_file, index=False)
    logging.info(f"Data cleaned, sorted, and new columns created successfully. Saved to '{output_file}'.")
except Exception as e:
    logging.error(f"Error saving Excel file: {e}")
    exit()