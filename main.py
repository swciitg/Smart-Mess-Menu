from scripts import fetch_pdfs_from_email, process_to_csv, update_to_db
from logs.logs import log_info

def run_pipeline():
    log_info("Starting weekly mess menu pipeline...")
    fetch_pdfs_from_email.fetch_pdfs()
    process_to_csv.convert_all_to_csv()
    update_to_db.upload_xlsx_files()
    log_info("Pipeline completed successfully.")
