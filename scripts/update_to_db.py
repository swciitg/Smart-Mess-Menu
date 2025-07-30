import os
import requests
import pandas as pd
from dotenv import load_dotenv
from io import BytesIO

load_dotenv()

API_URL = os.getenv('API_URL')
FOLDER_PATH = './mess_menu_csv'
SECURITY_KEY = os.getenv('MESSMENU_SECURITY')

def convert_csv_to_xlsx_bytes(csv_file_path):
    df = pd.read_csv(csv_file_path, on_bad_lines='skip')  # Skip bad rows gracefully
    excel_bytes = BytesIO()
    df.to_excel(excel_bytes, index=False, engine='openpyxl')
    excel_bytes.seek(0)
    return excel_bytes

def upload_xlsx_files():
    files = []
    for filename in os.listdir(FOLDER_PATH):
        if filename.endswith('.csv'):
            csv_path = os.path.join(FOLDER_PATH, filename)
            xlsx_filename = filename.replace('.csv', '.xlsx')
            xlsx_bytes = convert_csv_to_xlsx_bytes(csv_path)

            files.append(('csv2', (xlsx_filename, xlsx_bytes, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')))
    
    if not files:
        print("No CSV files found in the folder.")
        return

    data = {
        'security': SECURITY_KEY
    }

    print(f"Uploading {len(files)} XLSX files to server...")
    response = requests.post(API_URL, files=files, data=data)

    print(f"Status Code: {response.status_code}")
    if 'text/html' in response.headers.get('Content-Type', ''):
        print("HTML Response:")
        print(response.text)
    else:
        print("Response:", response.text)

