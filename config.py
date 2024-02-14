import os

API_TOKEN = os.getenv("ANCHOVY_API_TOKEN", "your_default_api_token")
DB_FILE = os.getenv("ANCHOVY_DB_FILE", "anchovy.db")
ASKALL_CRONTAB = "0 10,13,16 * * *"
