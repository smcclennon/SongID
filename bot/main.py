# SongID
# Main entry point for the bot. App flow + global error handling


import logging
from utils import setup_logging
from telegram import Update
from telegram.ext import Application
from config import BOT_TOKEN, DEBUG
from handlers import setup_handlers
from database import initialise_database





def main():
    '''Start the bot.'''
    setup_logging(debug=DEBUG)
    logger = logging.getLogger(__name__)
    initialise_database()
    logger.info('Starting the bot...')

    # Create the Application and pass it your bot's token.
    application = Application.builder().token(BOT_TOKEN).build()

    # Set up command and message handlers
    setup_handlers(application)

    # Run the bot until the user presses Ctrl-C
    logger.info('Bot is running. Press Ctrl-C to stop.')
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()