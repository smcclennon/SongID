# SongID
SongID is a Telegram bot that can identify music you send it

The bot downloads audio and video files it get sent on telegram via the [Telegram Bot API](https://core.telegram.org/api), and sends the file to [ACRCloud](https://www.acrcloud.com) for audio recognition processing.

Working with the [Telegram Bot API](https://core.telegram.org/api) is made significantly easier by using the [python-telegram-bot](https://python-telegram-bot.org/) wrapper which simplifies every aspect of the API

## Features
- Identify music within files
- Supports video files
- Supports Telegram audio messages
- Deletes downloaded files as soon as they've been processed
- Contents of generated files are completely customisable!

## Screenshots
<img src="https://smcclennon.github.io/assets/images/screenshots/SongID/voice.png" alt="Send Voice Message" width="100%"></img><img src="https://smcclennon.github.io/assets/images/screenshots/SongID/video.png" alt="Send Video" width="100%"></img>

*Written in Python 3.8 on Windows 10*