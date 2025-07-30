# Smart-Mess-Menu
Automated pipeline to fetch mess menus from email, extract structured data using gemini-1.5-flash model, and update the database — all on a weekly Dockerized cron job.


- Fetches mess menu PDFs from a configured email inbox
- Uses Gemini 1.5 Flash (via API) to extract structured data
- Updates the database with parsed menu information
