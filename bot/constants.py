import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


dotenv_file = BASE_DIR / '.env'
if os.path.isfile(dotenv_file):
    load_dotenv(dotenv_file, override=True)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MAX_FILE_DESCR_LEN = 20
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
LOGS_FILENAME = os.getenv("LOGS_FILENAME")

POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')

DEFAULT_DELAY_MIN = 5


API_KEY = os.getenv('API_KEY')
SHOP_ID = os.getenv('SHOP_ID')
BOT_URL= os.getenv('BOT_URL')

MEDIA_ROOT = Path('/media')

LOGS_FILENAME = os.getenv("LOGS_FILENAME")
