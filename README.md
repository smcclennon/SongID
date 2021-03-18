# SongID
[![License](https://img.shields.io/github/license/smcclennon/SongID)](LICENSE)
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fsmcclennon%2FSongID.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2Fsmcclennon%2FSongID?ref=badge_shield)
[![GitHub last commit](https://img.shields.io/github/last-commit/smcclennon/SongID)](https://github.com/smcclennon/SongID/commits)
[![HitCount](https://hits.dwyl.com/smcclennon/SongID.svg)](https://hits.dwyl.com/smcclennon/SongID)

SongID is a Telegram bot that can identify music in audio/video files you send it. These files can be screen recordings of an instagram post, or a telegram audio message taken by holding down the microphone icon in the bottom right.

The bot downloads audio and video files it get sent on telegram via the [Telegram Bot API](https://core.telegram.org/api), and sends the file to [ACRCloud](https://www.acrcloud.com) for audio recognition processing.

Working with the [Telegram Bot API](https://core.telegram.org/api) is made significantly easier by using the [python-telegram-bot](https://python-telegram-bot.org/) wrapper which simplifies every aspect of the API

## Features
- Identify music within files
- Supports video files
- Supports Telegram audio messages
- Find the name, artist, album, duration and release date of an identified song
- Provide direct links to the song on YouTube, Spotify and Deezer
- Deletes downloaded files as soon as they've been processed

## Blog Post
Read the blog post on how I created SongID on the [ACRCloud blog](https://blog.acrcloud.com/how-a-15-year-old-created-a-music-recognition-service-in-less-than-a-day-with-acrcloud)

Also featured on [Telegram Channels](https://telegramchannels.me/bots/songidbot) and [BotoStore](https://botostore.com/c/songidbot/)
## Screenshots
<img src="https://smcclennon.github.io/assets/images/screenshots/SongID/voice.png" alt="Send Voice Message" width="100%"></img><img src="https://smcclennon.github.io/assets/images/screenshots/SongID/video.png" alt="Send Video" width="100%"></img>

*Written in Python 3.8 on Windows 10*
