from scripts import fetch_pdfs_from_email, process_to_csv, update_to_db


def run_pipeline():
    fetch_pdfs_from_email.fetch_pdfs()
    process_to_csv.convert_all_to_csv()
    update_to_db.upload_xlsx_files()

if __name__ == "__main__":
    run_pipeline()
    print("Pipeline completed successfully.")