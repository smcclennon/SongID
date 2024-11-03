# SongID
# Handle different types of updates (messages, commands, etc.) + catch errors


import logging, html, json, traceback
from telegram import ForceReply, Update
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from database import add_user
from config import DEVELOPER_CHAT_ID

logger = logging.getLogger(__name__)


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    '''Log the error and send a telegram message to notify the developer.'''
    # Log the error before we do anything else, so we can see it even if something breaks.
    logger.error('Exception while handling an update:', exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = ''.join(tb_list)

    # Build the message with some markup and additional information about what happened.
    # You might need to add some logic to deal with messages longer than the 4096 character limit.
    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    message = (
        'An exception was raised while handling an update\n'
        f'<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}'
        '</pre>\n\n'
        f'<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n'
        f'<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n'
        f'<pre>{html.escape(tb_string)}</pre>'
    )

    # Finally, send the message
    await context.bot.send_message(
        chat_id=DEVELOPER_CHAT_ID, text=message, parse_mode=ParseMode.HTML
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    '''Send a message when the command /start is issued.'''
    user = update.effective_user
    logger.info(f'User {user.id} initiated /start command.')
    add_user(user.id, user.username, user.first_name, user.last_name)
    await update.message.reply_html(
        rf'Hi {user.mention_html()}!',
        reply_markup=ForceReply(selective=True),
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    '''Send a message when the command /help is issued.'''
    logger.info(f'User {update.effective_user.id} requested help.')
    await update.message.reply_text('Help!')

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    '''Echo the user message.'''
    logger.debug(f'Echoing message from user {update.effective_user.id}: {update.message.text}')
    await update.message.reply_text(update.message.text)

async def chat_id_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    '''Displays chat ID'''
    await update.effective_message.reply_html(
        f'Your chat id is <code>{update.effective_chat.id}</code>.'
    )

async def crash_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    x = 1 / 0


def setup_handlers(application: Application) -> None:
    '''Set up command and message handlers.'''
    application.add_error_handler(error_handler)  # Handle uncaught exceptions
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('chatid', chat_id_command))
    application.add_handler(CommandHandler('crash', crash_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    logger.info('Handlers have been set up.')