import telegram, json, time, os
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, MessageQueue


ver='0.2.2'
botName=f'SongID'
botVer=f'{botName} {ver}'
botAt=f'@SongIDBot'
botUsername='SongIDbot'
userdataDIR='data/userdata.json'
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


# Load saved user-data (user ID, username, full name, api calls, last api call)
with open(userdataDIR) as f:
    userdata = json.load(f)




 #  Initialise the required telegram bot data
u=Updater(token=token, use_context=True)
dp = u.dispatcher



# Log the users previous message (debugging)
def logusr(update):
    logger.info(f'[@{update.effective_chat.username}][{update.effective_chat.first_name} {update.effective_chat.last_name}][U:{update.effective_chat.id}][M:{update.effective_message.message_id}]: {update.message.text}')


# Send a message to the user and log the message (debugging)
def botsend(update, context, msg):
    context.bot.send_message(chat_id=update.effective_chat.id, text=str(msg)+f'\n\n<i>{botAt} <code>{ver}</code></i>', parse_mode=telegram.ParseMode.HTML)
    logger.info(f'[@{botUsername}][{botName}][M:{update.effective_message.message_id}]: {msg}')




logger.info('Loaded: SongIDFramework')