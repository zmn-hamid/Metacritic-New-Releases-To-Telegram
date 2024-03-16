# Metacritic New Releases

## What is this

I used to check [Metacritics new releases](https://www.metacritic.com/browse/albums/release-date/available/date) every time and save the Spotify link of the new albums of that webpage.
So I automated it

### Files explanation

- [AlbumOBJ.py](/AlbumOBJ.py): contains class for album objects
- [app.py](/app.py): the main app to be run
- [config.py](/config.py): parses the configs (not to be changed)
- [JSON_handler.py](/JSON_handler.py): handles json files
- [Log.py](/Log.py): handles logger
- [meta.html](/meta.html): offline example of that metacritic page, march 24
- [new_releases.py](/new_releases.py): fetches the new releases and saves them as well
- [public_config.ini](/public_config.ini): the configurations of the app
- [README.md](/README.md): this file
- [requirements.txt](/requirements.txt): the libraries that app use
- [roadmap.md](/roadmap.md): the simple roadmap of the program
- [Spotify_handler.py](/Spotify_handler.py): handles spotify interactions
- [Telegram_handler.py](/Telegram_handler.py): handles telegram

## Installation

1. python 3.8 or above, preferrably 3.11 (installed and added to path)
2. > pip install -r requirements.txt
3. make a `private_config.ini` file with this structure:

   ```
   [api]
   bot_token = token_of_your_bot


   [database]
   chat_id = the_chat_id_to_send_the_albums_to

   [spotify]
   client_id = client_id_of_spotify_app
   client_secret = client_secret_of_spotify_app
   ```

   `bot_token` -> from [BotFather](https://t.me/BotFather)
   `chat_id` -> from [Get My ID](https://t.me/getmyid_bot) or Using the link of the message (if is channel or group)
   `client_id` and `client_secret` -> from [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)

4. change `public_config.ini` if needed (not necessary):
   `skip_if_date_dont_match` -> skips the sending of the album if the date doesn't match with the url
   `log_level` -> debug, info, warning, ...
   `read_webpage_from_file` -> for developement. read the albums from website or the [meta file](/meta.html)
   `save_to_webpage_file` -> for development. save the content of webpage to the [meta file](/meta.html)
   `webpage_file_name` -> webpages's offline file name (eg meta.html)
   `number_of_fetched_albums` -> between 1 and 50. used in spotify's library to increase the chance of finding the album

## Usage

> python app.py

- Note: You have to manually stop the bot after the links are sent, using CTRL+C
