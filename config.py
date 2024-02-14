import os

API_TOKEN = os.getenv("TTB_API_TOKEN", "your_default_api_token")
DB_FILE = os.getenv("TTB_DB_FILE", "ttb.db")
ASKALL_CRONTAB = "0 10,13,16 * * *"
