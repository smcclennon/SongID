# SongID
# Configuration settings: API keys, tokens, constants


from decouple import config as env
import logging


logger = logging.getLogger(__name__)

VERSION = '2.0.0-dev'

BOT_TOKEN = env('BOT_TOKEN')
DEVELOPER_CHAT_ID = env('DEVELOPER_CHAT_ID')

SENTRY_DSN = env('SENTRY_DSN')
ENVIRONMENT = env('ENVIRONMENT', default='undefined').lower()
DEBUG = env('DEBUG', default=False, cast=bool)

DB_NAME = env('DB_NAME')
DB_USER = env('DB_USER')
DB_PASSWORD = env('DB_PASSWORD')
DB_HOST = env('DB_HOST')
DB_PORT = env('DB_PORT')
DB_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
