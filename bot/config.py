# SongID
# Configuration settings: API keys, tokens, constants


from decouple import config as env
import logging


logger = logging.getLogger(__name__)

VERSION = '2.0.0-dev'

BOT_TOKEN         = env('BOT_TOKEN')
DEVELOPER_CHAT_ID = env('DEVELOPER_CHAT_ID')
DOWNLOAD_DIR      = env('DOWNLOAD_DIR', default='downloads')

SENTRY_DSN        = env('SENTRY_DSN')
ENVIRONMENT       = env('ENVIRONMENT', default='undefined').lower()
DEBUG             = env('DEBUG', default=False, cast=bool)

DB_NAME           = env('DB_NAME', default='songid_db')
DB_USER           = env('DB_USER', default='songid_user')
DB_PASSWORD       = env('DB_PASSWORD')
DB_HOST           = env('DB_HOST', default='localhost')
DB_PORT           = env('DB_PORT', default='5432')
DB_URL            = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
