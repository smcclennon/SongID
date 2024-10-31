print('        _ _  ---====  SongID  ====---  _ _\n')


from SongIDProcessor import SIDProcessor
from SongIDCore import *
from telegram import ParseMode
from telegram.utils.helpers import mention_html
import sys, traceback
from threading import Thread
import urllib.request  # Check for internet connectivity
import traceback


os.system(f'title _ _  ---====  SongID {ver}  ====---  _ _')  # Set the windows console window title

while True:
    try:
        ACR_PING_CODE = urllib.request.urlopen("https://identify-eu-west-1.acrcloud.com").getcode()
        if ACR_PING_CODE == 200:
            logger.info('ACR Cloud pinged successfully!')
            break
        else:
            logger.warning('ACR Cloud ping error code: '+str(ACR_PING_CODE)+', retrying in 20 seconds')
            time.sleep(20)
    except:
        logger.warning('Unable to ping ACR Cloud, retrying in 10 seconds')
        time.sleep(10)



# Function from the telegram-bot-api wiki:
# https://github.com/python-telegram-bot/python-telegram-bot/wiki/Code-snippets#an-good-error-handler
def error(update, context):
    # we want to notify the user of this problem. This will always work, but not notify users if the update is an
    # callback or inline query, or a poll update. In case you want this, keep in mind that sending the message
    # could fail
    try:
        raise context.error
    except telegram.error.Unauthorized as e:
        logging.error(f'Unauthorized: {e}')
        # remove update.message.chat_id from conversation list
    except telegram.error.BadRequest as e:
        logging.error(f'BadRequest: {e}')
        # handle malformed requests - read more below!
    except telegram.error.TimedOut as e:
        logging.error(f'TimedOut: {e}')
        # handle slow connection problems
    except telegram.error.NetworkError as e:
        logging.error(f'NetworkError: {e}')
        # handle other connection problems
    except telegram.error.ChatMigrated as e:
        logging.error(f'ChatMigrated: {e}')
        # the chat_id of a group has changed, use e.new_chat_id instead
    except telegram.error.TelegramError as e:
        logging.error(f'Telegram Error: {e}')
        # handle all other telegram related errors
    if 'An existing connection was forcibly closed by the remote host' in str(context.error):
        #update.effective_message.reply_text('⚠️ Telegram closed the connection. Please try again.')
        #logbot(update, '⚠️ Telegram closed the connection. Please try again.')
        logger.info('existing connection closed (error exception catch temp code), pass')
        pass
    elif '[WinError 32] The process cannot access the file because it is being used by another process' in str(context.error):
        logger.info('File cannot be accessed (likely deleted), being used by another process, pass')
        pass
    else:
        if update != None:
            text = "⚠️ An error occured, sorry for any inconvenience caused.\nThe developer has been notified and will look into this issue as soon as possible."
            update.effective_message.reply_text(text)
        # This traceback is created with accessing the traceback object from the sys.exc_info, which is returned as the
        # third value of the returned tuple. Then we use the traceback.format_tb to get the traceback as a string, which
        # for a weird reason separates the line breaks in a list, but keeps the linebreaks itself. So just joining an
        # empty string works fine.
        trace = "".join(traceback.format_tb(sys.exc_info()[2]))
        # lets try to get as much information from the telegram update as possible
        payload = ""
        # normally, we always have an user. If not, its either a channel or a poll update.
        if update.effective_user:
            payload += f' with the user {mention_html(update.effective_user.id, update.effective_user.first_name)}'
        # there are more situations when you don't get a chat
        if update.effective_chat:
            payload += f' within the chat <i>{update.effective_chat.title}</i>'
            if update.effective_chat.username:
                payload += f' (@{update.effective_chat.username})'
        # but only one where you have an empty payload by now: A poll (buuuh)
        if update.poll:
            payload += f' with the poll id {update.poll.id}.'
        # lets put this in a "well" formatted text
        text = f"⚠️ Uncaught error\n\nThe error <code>{context.error}</code> occured{payload}. The full traceback:\n\n<code>{trace}" \
            f"</code>"
        # and send it to the dev
        context.bot.send_message(devid, text, parse_mode=ParseMode.HTML)
    # we raise the error again, so the logger module catches it. If you don't use the logger module, use it.
    raise


def stop_and_restart():
    # Gracefully stop the Updater and replace the current process with a new one
    u.stop()
    os.execl(sys.executable, sys.executable, *sys.argv)


# Respond when the developer sends the '/r' command
def restart(update, context):
    update.message.reply_text(f'{botName} is restarting...')
    Thread(target=stop_and_restart).start()


# Send a message to a specific user
def sendMsg(update, context):
    logusr(update)
    processed = SIDProcessor.commandArgs(update, context)
    if processed == None:
        logbotsend(update, context, '⚠️ Invalid syntax! <i>Make sure your spacing is correct</i>')
        helpCMD(update, context)
    elif processed[0] == 'too_long':
        logbotsend(update, context, f'⚠️ Sorry, your message is {processed[1]} characters over our length limit')

    else:
        user = processed[0]
        message = processed[1]
        if user[0] == '@':
            user = SIDProcessor.find_key(userdata, user[1:])[0]

        context.bot.send_message(int(user), message, parse_mode=telegram.ParseMode.HTML)
        logbotsend(update, context, 'Message sent!')


# Respond when the user sends the '/start' command
# (When the user adds a telegram bot, they are forced to send '/start')
def startCMD(update, context):
    logusr(update)
    userID=str(update.effective_chat.id)
    username=str(update.effective_chat.username)
    if userID not in userdata:
        SIDProcessor.addUserData(update, '0', '0')
    botsend(update, context, f'''<b>{botName}</b> is a Telegram bot that can identify music, similar to Shazam

Key Features:
- Scan for music in <b>videos</b>
- Scan for music playing around you with <b>Telegram Audio Message</b>
- Direct links to services such as <b>Youtube</b>, <b>Spotify</b> and <b>Deezer</b>
<i>[20MB file size limit]</i>

To get started, upload a file or record a Telegram Audio Message''')
    devsend(update, context, '\'{update.message.text}\'')
    logbot(update, '*Sent \'/start\' response*')

def limitCMD(update, context):
    logusr(update)
    botsend(update, context, '''Running SongID isn't free, and to keep costs low, we limit our daily API requests (comparing your audio to a third party music fingerprint database). 

Unfortunately, we've hit that limit today, and we're sorry for any inconvenience in being unable to process your request.
Please try again tomorrow.

In the meantime, you could try using other music identification services such as "Shazam" and "Sound Hound". Unfortunately these services don't support sending videos or audio files and can only identify music with your microphone.

SongID was originally created as a proof of concept, and I had no idea that it would become this popular.

View SongID and my other projects here: github.com/smcclennon
''')
    devsend(update, context, '\'{update.message.text}\'')
    logbot(update, '*Sent \'/limit\' response*')


# Respond when the user sends an unknown command
def unknownCMD(update, context):
    devsend(update, context, '\'{update.message.text}\'')
    logusr(update)
    logbotsend(update, context, "Sorry, I didn't understand that command.")


# Send user information on how to use the bot when they send '/help'
def helpCMD(update, context):
    logusr(update)
    botsend(update, context, f'''--= How to use {botName} =--

1. Send us a file: We will scan the file for music

---> You can send us an audio/video file on your device by pressing the paperclip icon in the bottom left
---> Record a Telegram audio message with the microphone icon in the bottom right and capture music playing around you.

File size limit: 20MB
If you exceed this limit, we won't be able to scan your file for music!''')
    devsend(update, context, '\'{update.message.text}\'')
    logbot(update, '*Sent help information*')


# Notify the user that their uploaded file isn't supported
def invalidFiletype(update, context):
    logusr(update)
    botsend(update, context, 'Sorry, we don\'t scan those types of files.\nPlease upload an <b>audio</b> or <b>video</b> file containing the music you wish to scan, or <b>record/hum</b> a <b>Telegram Voice Message</b>.\n\n<i>20MB file size limit</i>')
    context.bot.send_message(devid, f'User @{update.effective_user.username} ({update.effective_chat.id}) sent an invalid filetype')
    logbot(update, '*Sent invalid-filetype response*')


# Send the user the data we have saved on them when they send '/mydata'
def mydataCMD(update, context):
    logusr(update)
    data=SIDProcessor.getUserData(update)
    user = update.effective_chat.id
    username = data["username"]
    name = data["name"].replace(' None', '')
    api_calls = data["api_calls"]
    last_call = round(int(time.time()) - int(data["last_call"]))
    lc=SIDProcessor.getUserData(update)['last_call']
    botsend(update, context, f'''Here is the data we have stored about you:

<b>User ID</b>: {user}
<b>Username</b>: @{username}
<b>Full Name</b>: {name}
<b>API Calls</b>: {api_calls}
<b>Last API Call</b>: {last_call} seconds ago

<i>We do not store more data than we need to, and we delete your uploaded audio files as soon as we've finished processing them</i>
''')
    devsend(update, context, '\'{update.message.text}\'')
    logbot(update, '*Sent user data*')


# Respond to the user entering a command when in debug mode
def maintenanceINFO(update, context):
    logusr(update)
    context.bot.send_message(devid, f'User @{update.effective_user.username} ({update.effective_chat.id}) [MAINTENANCE MODE]: \'{update.message.text}\'')
    logbotsend(update, context, 'We\'re currently under maintenance, please try again later')


def noisyProcess(update, context):
    SIDProcessor.fileProcess(update, context, 'noisy')


# Currently not in use
def clearProcess(update, context):
    SIDProcessor.fileProcess(update, context, 'clear')


def humProcess(update, context):
    SIDProcessor.fileProcess(update, context, 'hum')

maintenance = 0

dp.add_error_handler(error)  # Handle uncaught exceptions
if maintenance == 1:
    logger.info('- - - - MAINTENANCE MODE ENABLED - - - -')
    dp.add_handler(CommandHandler('start', startCMD))  # Respond to '/start'

    dp.add_handler(CommandHandler('mydata', mydataCMD, filters=Filters.user(username=devusername)))  # Respond to '/mydata'
    dp.add_handler(CommandHandler('help', helpCMD, filters=Filters.user(username=devusername)))  # Respond to '/help'
    dp.add_handler(CommandHandler('limit', limitCMD, filters=Filters.user(username=devusername)))  # Respond to '/limit'

    # Handle different types of file uploads
    dp.add_handler(MessageHandler(Filters.audio & Filters.user(username=devusername), noisyProcess))
    dp.add_handler(MessageHandler(Filters.video & Filters.user(username=devusername), noisyProcess))
    dp.add_handler(MessageHandler(Filters.voice & Filters.user(username=devusername), humProcess))

    dp.add_handler(MessageHandler(Filters.photo & Filters.user(username=devusername), invalidFiletype))  # Notify user of invalid file upload
    dp.add_handler(MessageHandler(Filters.document & Filters.user(username=devusername), invalidFiletype))  # Notify user of invalid file upload
    dp.add_handler(CommandHandler('r', restart, filters=Filters.user(username=devusername)))  # Allow the developer to restart the bot
    dp.add_handler(CommandHandler('send', sendMsg, filters=Filters.user(username=devusername)))  # Allow the developer to send messages to users
    dp.add_handler(MessageHandler(Filters.command, unknownCMD))  # Notify user of invalid command
    #dp.add_handler(MessageHandler(Filters.text & Filters.user(username=devusername), helpCMD))  # Respond to '/help'

    dp.add_handler(MessageHandler(Filters.text, maintenanceINFO))  # Respond to text

elif maintenance == 0:
    dp.add_handler(CommandHandler('start', startCMD))  # Respond to '/start'
    dp.add_handler(CommandHandler('mydata', mydataCMD))  # Respond to '/mydata'
    dp.add_handler(CommandHandler('help', helpCMD))  # Respond to '/help'
    dp.add_handler(CommandHandler('limit', limitCMD))  # Respond to '/limit'

    # Handle different types of file uploads
    dp.add_handler(MessageHandler(Filters.audio, noisyProcess))
    dp.add_handler(MessageHandler(Filters.video, noisyProcess))
    dp.add_handler(MessageHandler(Filters.voice, humProcess))


    dp.add_handler(MessageHandler(Filters.photo, invalidFiletype))  # Notify user of invalid file upload
    dp.add_handler(MessageHandler(Filters.document, invalidFiletype))  # Notify user of invalid file upload
    dp.add_handler(CommandHandler('r', restart, filters=Filters.user(username=devusername)))  # Allow the developer to restart the bot
    dp.add_handler(CommandHandler('send', sendMsg, filters=Filters.user(username=devusername)))  # Allow the developer to send messages to users
    dp.add_handler(MessageHandler(Filters.command, unknownCMD))  # Notify user of invalid command
    dp.add_handler(MessageHandler(Filters.text, helpCMD))  # Respond to text
logger.info('Loaded: Handlers')


logger.info('Loading Complete!')
u.start_polling()
logger.info('Standard polling initialised')
u.idle()