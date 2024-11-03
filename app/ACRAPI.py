from acrcloud.recognizer import ACRCloudRecognizer
from acrcloud.recognizer import ACRCloudRecognizeType
from SongIDCore import *




# Get the ACRCloud config
config = {
    "clear": {
        "host": env['acr']['clear']['host'],
        "access_key": env['acr']['clear']['access_key'],
        "access_secret": env['acr']['clear']['access_secret'],
        "recognize_type": ACRCloudRecognizeType.ACR_OPT_REC_AUDIO,
        "debug":  False,
        "timeout": int(env['acr']['clear']['timeout'])
    },
    "noisy": {
        "host": env['acr']['noisy']['host'],
        "access_key": env['acr']['noisy']['access_key'],
        "access_secret": env['acr']['noisy']['access_secret'],
        "recognize_type": ACRCloudRecognizeType.ACR_OPT_REC_AUDIO,
        "debug": False,
        "timeout": int(env['acr']['noisy']['timeout'])
    },
    "hum": {
        "host": env['acr']['hum']['host'],
        "access_key": env['acr']['hum']['access_key'],
        "access_secret": env['acr']['hum']['access_secret'],
        "recognize_type": ACRCloudRecognizeType.ACR_OPT_REC_BOTH,
        "debug": False,
        "timeout": int(env['acr']['hum']['timeout'])
    }
}
logger.info('Loaded: ACR Config')


# Functions for sending files to the ACRCloud API and getting a response
# These functions were pre-made on the ACRCloud GitHub: https://github.com/acrcloud/acrcloud_sdk_python/blob/master/windows/win64/python3/test.py
class ACRAPI():
    #def clear(filePath):
    # Not currently using clear-audio detection, so the function is not necessary




    def noisy(filePath):

        '''This module can recognize ACRCloud by most of audio/video file.
            Audio: mp3, wav, m4a, flac, aac, amr, ape, ogg ...
            Video: mp4, mkv, wmv, flv, ts, avi ...'''
        re_config = config['noisy']
        re = ACRCloudRecognizer(re_config)

        #recognize by file path, and skip 0 seconds from from the beginning of sys.argv[1].
        #re.recognize_by_file(filePath, 0, 10)
        logger.info('ACR: Processing Noisy request...')
        logger.debug(re_config)
        buf = open(filePath, 'rb').read()
        #recognize by file_audio_buffer that read from file path, and skip 0 seconds from from the beginning of sys.argv[1].
        data = re.recognize_by_filebuffer(buf, 0, 60)
        data = json.loads(data)
        logger.debug(data)
        logger.info('ACR: Processing complete!')
        return data




    def hum(filePath):

        '''This module can recognize ACRCloud by most of audio/video file.
            Audio: mp3, wav, m4a, flac, aac, amr, ape, ogg ...
            Video: mp4, mkv, wmv, flv, ts, avi ...'''
        re_config = config['hum']
        re = ACRCloudRecognizer(re_config)

        #recognize by file path, and skip 0 seconds from from the beginning of sys.argv[1].
        #re.recognize_by_file(filePath, 0, 10)
        logger.info('ACR: Processing Hum request...')
        logger.debug(re_config)
        buf = open(filePath, 'rb').read()
        #recognize by file_audio_buffer that read from file path, and skip 0 seconds from from the beginning of sys.argv[1].
        data = re.recognize_by_filebuffer(buf, 0, 10)
        data = json.loads(data)
        logger.debug(data)
        logger.info('ACR: Processing complete!')
        return data