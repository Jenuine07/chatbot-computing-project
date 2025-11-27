import pandas as pd
import os
from csv import QUOTE_NONNUMERIC

# --- Configuration ---
# The path to your Excel file (input)
EXCEL_FILE_PATH = r".\..\gabungan_akhir_bersih.xlsx"

# The target directory for the new CSV file (output)
OUTPUT_DIRECTORY = r".\processed"
# ---------------------

try:
    # 1. Prepare the output file path
    base_filename = os.path.splitext(os.path.basename(EXCEL_FILE_PATH))[0]
    # Name the new file and place it in the specified processed directory
    CSV_FILE_PATH = os.path.join(OUTPUT_DIRECTORY, f"{base_filename}_converted.csv")

    print(f"Reading Excel file from: {EXCEL_FILE_PATH}")
    
    # Check if the output directory exists, and create it if it doesn't
    if not os.path.exists(OUTPUT_DIRECTORY):
        os.makedirs(OUTPUT_DIRECTORY)
        print(f"Created output directory: {OUTPUT_DIRECTORY}")

    # 2. Read the Excel file into a pandas DataFrame
    # Reads the first sheet (index 0)
    df = pd.read_excel(EXCEL_FILE_PATH, sheet_name=0)
    
    print("Excel file read successfully.")
    
    # 3. Write the DataFrame to a CSV file with necessary quoting
    # - index=False: Skips the pandas row numbers
    # - quoting=QUOTE_NONNUMERIC: **Crucial** for wrapping text fields (like long bodies with commas) in double quotes.
    df.to_csv(
        CSV_FILE_PATH, 
        index=False, 
        encoding='utf-8', 
        quoting=QUOTE_NONNUMERIC
    )
    
    print(f"\n✅ Conversion successful!")
    print(f"New CSV file created at: {CSV_FILE_PATH}")

except FileNotFoundError:
    print(f"\n❌ Error: The Excel file was not found at: {EXCEL_FILE_PATH}")
except Exception as e:
    print(f"\n❌ An unexpected error occurred: {e}")