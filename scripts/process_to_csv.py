import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("models/gemini-2.5-pro")


system_prompt = os.getenv("SYSTEM_PROMPT").replace("\\n", "\n")

input_folder = "./mess_menus"
output_folder = "./mess_menu_csv"

os.makedirs(output_folder, exist_ok=True)

def read_pdf_bytes(file_path):
    with open(file_path, "rb") as f:
        return f.read()


def convert_pdf_to_csv(pdf_path):
    pdf_bytes = read_pdf_bytes(pdf_path)

    try:
        response = model.generate_content([
            {"mime_type": "application/pdf", "data": pdf_bytes},
            system_prompt.strip()
        ])
        return response.text
    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")
        return None


def save_csv(csv_text, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(csv_text)


def convert_all_to_csv():
    for filename in os.listdir(input_folder):
        if not filename.lower().endswith(".pdf"):
            continue

        pdf_path = os.path.join(input_folder, filename)
        print(f"Processing {filename}...")

        csv_output = convert_pdf_to_csv(pdf_path)


        if csv_output and csv_output.strip().startswith("Day,Breakfast,Lunch,Dinner"):
            output_csv_path = os.path.join(output_folder, filename.replace(".pdf", ".csv"))
            save_csv(csv_output, output_csv_path)
            print(f" Saved: {output_csv_path}")
        else:
            print(f" Skipped (not a valid mess menu): {filename}")

        print("Waiting for 62 seconds to respect rate limits...")
        time.sleep(62)
convert_all_to_csv()
