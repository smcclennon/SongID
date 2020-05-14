import telegram, json, time, os
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, MessageQueue


ver='0.2.2.6.2'
botName=f'SongID'
botVer=f'{botName} {ver}'
botAt=f'@SongIDBot'
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


# Load data/userdata.json into the variable 'userdata'
with open('data/userdata.json') as f:
    userdata = json.load(f)




#  Initialise the required telegram bot data
u=Updater(token=token, use_context=True, request_kwargs={'read_timeout': 6, 'connect_timeout': 7})
dp = u.dispatcher



# Log the users previous message (debugging)
def logusr(update):
    logger.info(f'[@{update.effective_chat.username}][{update.effective_chat.first_name} {update.effective_chat.last_name}][U:{update.effective_chat.id}][M:{update.effective_message.message_id}]: {update.message.text}')


# Send a message to the user
def botsend(update, context, msg):
    update.message.reply_text(str(msg)+f'\n\n<i>{botAt} <code>{ver}</code></i>', parse_mode=telegram.ParseMode.HTML)


# Send a message to the user and log the message sent
def logbotsend(update, context, msg):
    update.message.reply_text(str(msg)+f'\n\n<i>{botAt} <code>{ver}</code></i>', parse_mode=telegram.ParseMode.HTML)
    logger.info(f'[@{botUsername}][{botName}][M:{update.effective_message.message_id}]: {msg}')


# Log a message the bot has sent anonymously
def logbot(update, msg):
    logger.info(f'[@{botUsername}][{botName}][M:{update.effective_message.message_id}]: {msg}')




logger.info('Loaded: SongIDFramework')