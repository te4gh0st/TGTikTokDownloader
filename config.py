import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN", "")

WEBHOOK_ACTIVE = os.getenv("WEBHOOK_ACTIVE", "0")
WEBHOOK_HOST = os.getenv('WEBHOOK_HOST', '')
WEBHOOK_PATH = os.getenv('WEBHOOK_PATH', '')
WEBAPP_HOST = os.getenv('WEBAPP_HOST', '')
WEBAPP_PORT = os.getenv('WEBAPP_PORT', '')

WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'
