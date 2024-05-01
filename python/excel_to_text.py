#pip install pandas
#pip install openpyxl

import pandas as pd
import os

def excel_to_text_files(excel_path):
    # Load the Excel file
    xls = pd.ExcelFile(excel_path)
    
    # Get the directory to save text files
    output_directory = os.path.dirname(excel_path)
    
    # Iterate over all sheets in the Excel file
    for sheet_name in xls.sheet_names:
        # Read the sheet into a DataFrame
        df = pd.read_excel(xls, sheet_name=sheet_name)
        
        # Convert the DataFrame to a string with tab-separated values
        data_string = df.to_csv(sep='\t', index=False)
        
        # Define the path for the output text file
        output_path = os.path.join(output_directory, f"{sheet_name}.txt")
        
        # Create a text file named after the sheet and write the data
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(data_string)

# Define the path to the Excel file
excel_path = '/Users/username/path/input.xlsx'  # Update 'yourusername' with your actual username
excel_to_text_files(excel_path)
