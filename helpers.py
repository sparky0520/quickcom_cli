import csv
import pandas as pd
from pyfiglet import Figlet

def pretty_print(text, font):
    f = Figlet(font=font)
    print(f.renderText(text))


def save_to_file(data_list, filename, filetype='excel'):
    """
    Save list of dictionaries to an Excel or CSV file.
    
    Args:
        data_list (list): List of dictionaries to save.
        filename (str): The name of the output file (without extension).
        filetype (str): 'excel' or 'csv' (default: 'excel').
    """
    if not data_list:
        print("💥 Your data list is empty! Nothing to save.")
        return
    
    # Create a DataFrame from the list of dicts
    df = pd.DataFrame(data_list)
    
    if filetype.lower() == 'csv':
        csv_file = f"{filename}.csv"
        df.to_csv(csv_file, index=False, encoding='utf-8-sig')
        print(f"✨ Your data has been saved to CSV at '{csv_file}'!")
    else:
        excel_file = f"{filename}.xlsx"
        with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Data')
        print(f"👑 Your data is now perfectly placed in Excel file '{excel_file}'!")
