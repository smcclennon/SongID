import telegram, json, time, os
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, MessageQueue
import sentry_sdk


ver='0.2.4'
botName = 'SongID'
botVer=f'{botName} {ver}'
botAt = '@SongIDBot'
botUsername='SongIDbot'
downloadDIR='data/downloads'


# Initialise the logger and format it's output
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S',
)
logger = logging.getLogger(__name__)


#  Load private information regarding the telegram bot
with open('data/token.json', 'r') as f:
    all_tokens = json.load(f)
    telegramConfig = all_tokens["telegram"]
    token = telegramConfig["token"]
    devid = telegramConfig["devid"]
    devusername = telegramConfig["devusername"]
    heroku_enabled = all_tokens["heroku"]["enabled"]
    heroku_webhook = all_tokens["heroku"]["webhook"]
    heroku_listen = all_tokens["heroku"]["listen"]
    heroku_port = all_tokens["heroku"]["port"]
    sentry_dsn = all_tokens["sentry"]["dsn"]

sentry_sdk.init(
dsn=sentry_dsn,
release=ver,
sample_rate=1.0,
traces_sample_rate=1.0,
attach_stacktrace=True,
with_locals=True
)


# Load data/userdata.json into the variable 'userdata'
with open('data/userdata.json') as f:
    userdata = json.load(f)




#  Initialise the required telegram bot data
u=Updater(token=token, use_context=True, request_kwargs={'read_timeout': 6, 'connect_timeout': 7})
dp = u.dispatcher



# Log the users previous message (debugging)
def logusr(update):
    if hasattr(update.message, 'text'):
        message = update.message.text
    else:
        message = '[No message]'
    logger.info(f'[@{update.effective_chat.username}][{update.effective_chat.first_name} {update.effective_chat.last_name}][U:{update.effective_chat.id}][M:{update.effective_message.message_id}]: {message}')


# Send a message to the user
def botsend(update, context, msg):
    if hasattr(update.message, 'reply_text'):
        update.message.reply_text(
            f'{str(msg)}\n\n<i>{botAt} <code>{ver}</code></i>',
            parse_mode=telegram.ParseMode.HTML,
        )

def devsend(update, context, msg):
    if '{update.message.text}' in msg:
        if hasattr(update.message, 'text'):
            msg = update.message.text
        else:
            msg = '[No message]'
    context.bot.send_message(devid, f'User @{update.effective_user.username} ({update.effective_chat.id}): \'{msg}\'')


# Send a message to the user and log the message sent
def logbotsend(update, context, msg):
    update.message.reply_text(
        f'{str(msg)}\n\n<i>{botAt} <code>{ver}</code></i>',
        parse_mode=telegram.ParseMode.HTML,
    )

    logger.info(f'[@{botUsername}][{botName}][M:{update.effective_message.message_id}]: {msg}')


# Log a message the bot has sent anonymously
def logbot(update, msg):
    logger.info(f'[@{botUsername}][{botName}][M:{update.effective_message.message_id}]: {msg}')




logger.info('Loaded: SongIDFramework')