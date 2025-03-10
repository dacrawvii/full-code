import pandas as pd
import requests
import time
import os
import logging

# Configure logging
logging.basicConfig(filename='address_autocomplete_script.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Load the Excel file
file_path = r'C:\Users\Alex.Crawley\OneDrive - Bentley Systems, Inc\Documents\PY DATA\cleaned_sorted_py_input_with_columns.xlsx'
logging.info(f"Loading Excel file from: {file_path}")
try:
    df = pd.read_excel(file_path, engine='openpyxl')
    logging.info("Excel file loaded successfully.")
except Exception as e:
    logging.error(f"Error loading Excel file: {e}")
    exit()

# Define the Geoapify API key and endpoint
api_key = '6a0f63b96e30489b9a5c8e7d07ed7ed0'
autocomplete_endpoint = 'https://api.geoapify.com/v1/geocode/search'

# Function to get address autocomplete suggestions with error handling
def get_address_suggestions(address):
    try:
        params = {
            'text': address,
            'apiKey': api_key
        }
        response = requests.get(autocomplete_endpoint, params=params)
        response.raise_for_status()
        suggestions = response.json().get('features', [])
        if suggestions:
            return suggestions[0].get('properties', {}).get('formatted', 'No suggestion')
        else:
            return 'No suggestion'
    except requests.exceptions.RequestException as e:
        logging.error(f"Request error for address '{address}': {e}")
        return f"Request error: {e}"
    except Exception as e:
        logging.error(f"Error for address '{address}': {e}")
        return f"Error: {e}"

# Apply the function to one row for testing
suggestions = []
unprocessed_rows = []
logging.info("Starting address autocomplete suggestions...")
for index, row in df.iterrows():
    if index >= 1:
        unprocessed_rows.append(row)
        continue  # Skip processing for the remaining rows
    address = f"{row['Education Institute']}, {row['Country Name']}"
    suggestion = get_address_suggestions(address)
    suggestions.append(suggestion)
    logging.info(f"Processed {index + 1} addresses.")
    time.sleep(1)  # To handle rate limiting

# Create a new DataFrame for the processed row
processed_df = df.iloc[:1].copy()
processed_df['Address Suggestions'] = suggestions

# Save the new file with address suggestions
output_dir = r'C:\Users\Alex.Crawley\OneDrive - Bentley Systems, Inc\Documents\PY DATA'
autocomplete_file_path = os.path.join(output_dir, 'processed_with_address_suggestions.xlsx')
logging.info(f"Saving file with address suggestions to: {autocomplete_file_path}")
try:
    processed_df.to_excel(autocomplete_file_path, index=False, engine='openpyxl')
    logging.info(f"The new file with address suggestions has been saved to {autocomplete_file_path}.")
except Exception as e:
    logging.error(f"Error saving Excel file: {e}")

# Save the unprocessed rows to a separate file
unprocessed_file_path = os.path.join(output_dir, 'unprocessed_rows.xlsx')
logging.info(f"Saving unprocessed rows to: {unprocessed_file_path}")
try:
    unprocessed_df = pd.DataFrame(unprocessed_rows)
    unprocessed_df.to_excel(unprocessed_file_path, index=False, engine='openpyxl')
    logging.info(f"The unprocessed rows have been saved to {unprocessed_file_path}.")
except Exception as e:
    logging.error(f"Error saving unprocessed rows: {e}")