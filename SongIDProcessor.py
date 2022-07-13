from ACRAPI import ACRAPI
from SongIDCore import *




# Save user data from the "userdata" variable contents to data/userdata.json
def saveUserData():
    with open('data/userdata.json', 'w') as f:
        json.dump(userdata, f)
    logger.info('User data has been saved')


# Format milliseconds to minutes:seconds (used for track-length)
def msConvert(ms):
    ms = int(ms)
    seconds = ms // 1000
    return time.strftime('%M:%S', time.gmtime(seconds))


# Return how long the user has until they can make another API request
def timeLeft(update):
    logger.debug('timeLeft(0/3)')
    last_call = SIDProcessor.getUserData(update)['last_call']
    logger.debug('timeLeft(1/2)')
    dur_since_last_call = round(time.time()) - int(last_call)
    logger.debug('timeLeft(2/2)')
    return int(20 - round(dur_since_last_call))


# Return whether the user has surpassed their API cooldown or not
def authorised(update):
    logger.debug('authorised(0/3)')
    alldata=SIDProcessor.getUserData(update)
    api_calls = alldata['api_calls']
    last_call = alldata['last_call']
    logger.debug('authorised(1/3)')
    if timeLeft(update) <= 0:
        #api_calls = getUserData(f'{update.effective_chat.id}')['api_calls']
        logger.debug('authorised(2/3)')
        api_calls = int(api_calls) + 1
        last_call = round(time.time())
        SIDProcessor.addUserData(update, f'{api_calls}', f'{last_call}')
        logger.debug('authorised(3/3)')
        return True
    else:
        logger.debug('authorised(3/3)')
        return False


# Download the users uploaded file
def fileDownload(update, context):
    file_id = None
    while file_id is None:
        # Get the file-id
        try:
            file_id = update.effective_message.audio.file_id
            break
        except:
            pass
        try:
            file_id = update.effective_message.video.file_id
            break
        except:
            pass
        try:
            file_id = update.effective_message.document.file_id
            break
        except:
            pass
        try:
            file_id = update.effective_message.voice.file_id
            break
        except:
            logbotsend(update, context, f'⚠️ Sorry, we don\'t support that filetype.')
        break
    try:
        file_info = context.bot.get_file(file_id)
        file_size = file_info["file_size"]
        if int(file_size) <= 20000000:
            web_path = file_info["file_path"]  # Get the original filename
            extension = os.path.splitext(f'{web_path}')[1]  # Get the file extension (.mp3, .mp4 etc)
            fileName = f'{update.effective_chat.id}_{update.effective_message.message_id}_{file_id}{extension}'
            newFile = context.bot.get_file(file_id)
            newFile.download(f'{downloadDIR}/{fileName}')
            return fileName
    except:
        botsend(update, context, f'⚠️ Sorry, your file is too big for us to process.\nFile size limit: 20MB')
        logbot(update, '*Sent file-size limit error*')
        return 'FILE_TOO_BIG'



# Process the JSON response from the ACRCloud API
def dataProcess(update, context, data):
    context.bot.sendChatAction(chat_id=update.effective_chat.id, action=telegram.ChatAction.TYPING, timeout=20)  # Display a typing 'chat action' from the bot for the respective user
    if data["status"]["msg"] == 'Success':  #  If a match was found by ACRCloud
        logger.info('ACR: Found a match!')
        data = data["metadata"]["music"][0]
        score=data["score"]
        title=data["title"]
        artist=data["artists"][0]["name"]
        try:
            album=None
            album=data["album"]["name"]
        except:
            pass
        #artists_dict=data["artists"]
        #artists=''
        #for value in artists_dict:
        #    print(value)
        #    artists=artists+str(data["artists"][int(value)]["name"])+', '
        #print(artists_dict)
        #artists=data["artists"][0:]["name"]
        duration=msConvert(data["duration_ms"])
        try:
            # Get the YouTube link for the song if it exists
            youtube=None
            youtube='youtu.be/'+data["external_metadata"]["youtube"]["vid"]  # Get the YouTube track URL
        except:
            pass
        try:
            # Get Deezer information on the song if it exists
            deezer=None
            deezer='deezer.com/track/'+data["external_metadata"]["deezer"]["track"]["id"]  # Get the Deezer track URL
            # Set the title, artist & album information to Deezer's record if possible
            title=data["external_metadata"]["deezer"]["track"]["name"]
            artist=data["external_metadata"]["deezer"]["artists"][0]["name"]
            album=data["external_metadata"]["deezer"]["album"]["name"]
        except:
            pass
        try:
            # Get Spotify information on the song if it exists
            spotify=None
            spotify='open.spotify.com/track/'+data["external_metadata"]["spotify"]["track"]["id"]  # Get the Spotify track URL
            # Set the title, artist & album information to Spotify's record if possible
            title=data["external_metadata"]["spotify"]["track"]["name"]
            artist=data["external_metadata"]["spotify"]["artists"][0]["name"]
            album=data["external_metadata"]["spotify"]["album"]["name"]
        except:
            pass
        try:
            # Try to get the track release date
            release_date=None
            release_date=data["release_date"]
        except:
            pass
        # Rank the track match based off of it's match %
        if score == 100:
            response = f'Perfect Match: <b>{score}%</b>'
        elif score >= 90:
            response = f'Good Match: <b>{score}%</b>'
        elif score >= 80:
            response = f'Likely Match: <b>{score}%</b>'
        elif score >= 70:
            response = f'Possible Match: <b>{score}%</b>'
        else:
            response = f'Unlikely Match\n<i>We\'re unsure what your song is, but it may be this</i>'
        response += f'\n\n<b>{artist}</b> - <b>{title}</b>\n'
        if album != None:
            response += f'\nAlbum: {album}'
        response += f'\nLength: {duration}'
        if release_date != None:
            response += f'\nRelease date: {release_date}'
        response += f'\n'
        if youtube != None:
            response += f'\nYouTube: {youtube}'
        if spotify != None:
            response += f'\nSpotify: {spotify}'
        if deezer != None:
            response += f'\nDeezer: {deezer}'
        response = response + \
            '\n\nPlease consider <a href="https://t.me/dailychannelsbot?start=songidbot">leaving us a review!</a>'
        # Send the respective user this information
        botsend(update, context, response)
        logbot(update, '*Sent song information*')
        context.bot.send_message(
            devid, f'User @{update.effective_user.username} ({update.effective_chat.id}) identified a song!')
    elif data["status"]["code"] == 3003:
        logger.info('ACR: Limit exceeded')
        botsend(update, context,
                'We\'ve hit our daily API limit. Type /limit for more info')
        context.bot.send_message(
            devid, f'User @{update.effective_user.username} ({update.effective_chat.id}) hit the limit')
    else:  # If no match was found by ACRCloud
        logger.info('ACR: Failed to find a match')
        botsend(update, context, '''No Match :(

<i>Sorry, couldn\'t find any music in the file you uploaded.</i>


Tips for a higher chance of matching:
- When recording with the Telegram Voice Recorder, try to record for at least 10 seconds, preferably during the chorus of a song where it's most iconic.
- When uploading a file, try to make sure the audio quality is the best you have accessible.''')
        logbot(update, 'No Match :(')
        context.bot.send_message(devid, f'User @{update.effective_user.username} ({update.effective_chat.id}) couldn\'t find a match')













class SIDProcessor():

    # Add user data to the 'userdata' variable and save it to disk
    def addUserData(self, apiCalls, lastCall):
        userdata[f'{self.effective_user.id}'] = {
            'username': f'{self.effective_chat.username}',
            'name': f'{self.effective_user.first_name} {self.effective_user.last_name}',
            'api_calls': f'{apiCalls}',
            'last_call': f'{lastCall}',
        }

        logger.info(
            f'User data added/updated: [{self.effective_user.id}: {self.effective_user.username}, {self.effective_user.first_name} {self.effective_user.last_name}, {apiCalls}, {lastCall}]'
        )

        saveUserData()

    # Get user data for the respective user
    def getUserData(self):
        #update = json.loads(update)
        logger.debug('getUserData(0/2)')

        # May be completely unnecessary, just in case
        if hasattr(self, 'effective_chat'):
            # Get users Telegram ID
            userID = str(self.effective_chat.id)
            # Add user to userdata in case they did not initially send /start
            # to prevent AttributeErrors occurring from their key not being
            # present in the database
            # (https://github.com/smcclennon/SongID/issues/6#issuecomment-1021517621)
            if userID not in userdata:
                SIDProcessor.addUserData(self, '0', '0')
        logger.debug('getUserData(1/2)')

        data = userdata[f'{self.effective_user.id}']
        logger.debug('getUserData(2/2)')
        return data




    # If authorised, download the users uploaded file and send it to the API response processor, and then delete the downloaded file from disk
    def fileProcess(self, context, processor):
        logusr(self)
        for _ in range(10):
            try:
                logger.info('fileProcess: Attempting to send ChatAction.TYPING')
                context.bot.sendChatAction(
                    chat_id=self.effective_chat.id,
                    action=telegram.ChatAction.TYPING,
                    timeout=10,
                )

                logger.info('fileProcess: Successfully sent ChatAction.TYPING')
            except:
                logger.info('fileProcess: Failed to send ChatAction.TYPING')
                continue
            logger.info('fileProcess: Breaking from ChatAction loop')
            break
        if authorised(self):
            context.bot.sendChatAction(
                chat_id=self.effective_chat.id,
                action=telegram.ChatAction.RECORD_AUDIO,
                timeout=20,
            )

            fileName = fileDownload(self, context)
            if fileName != 'FILE_TOO_BIG':
                deleteSuccess = 0
                while deleteSuccess != 5:
                    try:
                        if processor == 'noisy':
                            dataProcess(self, context, ACRAPI.noisy(f'{downloadDIR}/{fileName}'))
                            os.remove(f'{downloadDIR}/{fileName}')
                        elif processor == 'clear':
                            dataProcess(self, context, ACRAPI.clear(f'{downloadDIR}/{fileName}'))
                            os.remove(f'{downloadDIR}/{fileName}')
                        elif processor == 'hum':
                            dataProcess(self, context, ACRAPI.hum(f'{downloadDIR}/{fileName}'))
                            os.remove(f'{downloadDIR}/{fileName}')
                        deleteSuccess = 5
                    except:
                        deleteSuccess+=1
        else:
            timeLeft_int = timeLeft(self)
            if timeLeft_int == 1:
                time_msg = f'{timeLeft_int} second'
            else:
                time_msg = f'{timeLeft_int} seconds'
            logbotsend(
                self,
                context,
                f'Due to an increased volume of requests, a 20 second cooldown has been put in place to benefit the user.\n\nPlease wait {time_msg} before making another request',
            )

            context.bot.send_message(
                devid,
                f'User @{self.effective_user.username} ({self.effective_chat.id}) hit the cooldown ({time_msg} left)',
            )
    # Split the command arguments into an array
    def commandArgs(self, context):
        whitespace=[]
        keysplit=1
        msgsplit=2
        command = self.message.text
        split = command.split(' ')  # Split the message with each space
        if len(split) < 3:
            return None
        key = split[1]
        while key == "":  # If the user used irregular spacing
            keysplit+=1
            whitespace.append(keysplit-1)
            key = split[keysplit]

        message = command
        for space in whitespace:
            message = message.replace(split[space], '', 1)
        message = message.replace(f'{split[0]} ', '', 1)
        message = message.replace(f'{split[keysplit]} ', '', 1)

        if len(message) > 5000:
            return ['too_long', len(message)-5000]
        return [key, message]


    # Find the parent key(s) within a dictionary
    def find_key(self, value):  # https://stackoverflow.com/a/15210253
        for k,v in self.items():
            if isinstance(v, dict):
                if p := SIDProcessor.find_key(v, value):
                    return [k] + p
            elif v == value:
                return [k]
