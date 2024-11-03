# SongID
# Utility functions and helpers

import os
import logging
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration
from config import SENTRY_DSN, VERSION, ENVIRONMENT

def setup_logging(debug=False):
    '''Set up logging configuration.'''
    # Set logging level based on debug flag
    log_level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=log_level
    )

    # set higher logging level for httpx to avoid all GET and POST requests being logged
    logging.getLogger('httpx').setLevel(logging.WARNING)
    
    logger = logging.getLogger(__name__)
    logger.info('Logging is set up.')
    if debug:
        logger.debug('Debug logging is enabled.')

    if ENVIRONMENT != 'development':
        # Initialise Sentry
        sentry_logging = LoggingIntegration(
            level=logging.INFO,  # Capture info and above as breadcrumbs
            event_level=logging.ERROR  # Send errors as events
        )
        sentry_sdk.init(
            dsn=SENTRY_DSN,
            integrations=[sentry_logging],
            release=VERSION,
            environment=ENVIRONMENT
    )


# TODO: Attempt to download file above 20MB. Add error handling
#def download_file(update, context):
#    file_id = update.message.document.file_id
#    new_file = context.bot.get_file(file_id)
#    file_path = os.path.join('downloads', update.message.document.file_name)
#    new_file.download(file_path)
#    return file_path