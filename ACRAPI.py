from acrcloud.recognizer import ACRCloudRecognizer
from acrcloud.recognizer import ACRCloudRecognizeType
from SongIDCore import *




# Get the ACRCloud config
with open('data/acrcloud.json', 'r') as f:
    config = json.load(f)
    logger.info('Loaded: ACR Config')


# Get the ACRCloud access & private keys
acrkey = all_tokens["acr"]




config_clear = config["clear"]
config_clear["access_key"] = acrkey["clear"]["access_key"]
config_clear["access_secret"] = acrkey["clear"]["access_secret"]
config_clear["recognize_type"] = ACRCloudRecognizeType.ACR_OPT_REC_AUDIO
config_clear["debug"] = False


config_noisy = config["noisy"]
config_noisy["access_key"] = acrkey["noisy"]["access_key"]
config_noisy["access_secret"] = acrkey["noisy"]["access_secret"]
config_noisy["recognize_type"] = ACRCloudRecognizeType.ACR_OPT_REC_AUDIO
config_noisy["debug"] = False


config_hum = config["hum"]
config_hum["access_key"] = acrkey["hum"]["access_key"]
config_hum["access_secret"] = acrkey["hum"]["access_secret"]
config_hum["recognize_type"] = ACRCloudRecognizeType.ACR_OPT_REC_BOTH
config_hum["debug"] = False



# Functions for sending files to the ACRCloud API and getting a response
# These functions were pre-made on the ACRCloud GitHub: https://github.com/acrcloud/acrcloud_sdk_python/blob/master/windows/win64/python3/test.py
class ACRAPI():
    #def clear(filePath):
    # Not currently using clear-audio detection, so the function is not necessary




    def noisy(self):
        config = config_noisy

        '''This module can recognize ACRCloud by most of audio/video file.
            Audio: mp3, wav, m4a, flac, aac, amr, ape, ogg ...
            Video: mp4, mkv, wmv, flv, ts, avi ...'''
        re = ACRCloudRecognizer(config)

        #recognize by file path, and skip 0 seconds from from the beginning of sys.argv[1].
        #re.recognize_by_file(filePath, 0, 10)
        logger.info('ACR: Processing request...')
        buf = open(self, 'rb').read()
        #recognize by file_audio_buffer that read from file path, and skip 0 seconds from from the beginning of sys.argv[1].
        data = re.recognize_by_filebuffer(buf, 0, 60)
        data = json.loads(data)
        logger.info('ACR: Processing complete!')
        return data




    def hum(self):
        config = config_hum

        '''This module can recognize ACRCloud by most of audio/video file.
            Audio: mp3, wav, m4a, flac, aac, amr, ape, ogg ...
            Video: mp4, mkv, wmv, flv, ts, avi ...'''
        re = ACRCloudRecognizer(config)

        #recognize by file path, and skip 0 seconds from from the beginning of sys.argv[1].
        #re.recognize_by_file(filePath, 0, 10)
        logger.info('ACR: Processing request...')
        buf = open(self, 'rb').read()
        #recognize by file_audio_buffer that read from file path, and skip 0 seconds from from the beginning of sys.argv[1].
        data = re.recognize_by_filebuffer(buf, 0, 10)
        data = json.loads(data)
        logger.info('ACR: Processing complete!')
        return data