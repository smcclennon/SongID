# SongID
# Music recognition

import logging


logger = logging.getLogger(__name__)


# TODO parse acrcloud response, update database, format message response, return message to handler for sending
#def parse_acrcloud_response(response):
#    if response['status'] == 0:  # Assuming 0 means success
#        song_info = response['metadata']['music'][0]
#        title = song_info['title']
#        artist = song_info['artists'][0]['name']
#        message = f'🎵 *{title}* by *{artist}*'
#        return message
#    else:
#        return 'Sorry, I couldn\'t identify the song.'