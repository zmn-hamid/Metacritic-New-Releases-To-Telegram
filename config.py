import configparser, logging

# default configs
HISTORY_FILENAME = "history.json"

# private configs
private_config = configparser.ConfigParser()
private_config.read("private_config.ini")

BOT_TOKEN = private_config.get("api", "bot_token")
CHAT_ID = private_config.get("database", "chat_id")
CLIENT_ID = private_config.get("spotify", "client_id")
CLIENT_SECRET = private_config.get("spotify", "client_secret")

# public configs
public_config = configparser.ConfigParser()
public_config.read("public_config.ini")

URL = public_config.get("website", "url")
SKIP_IF_DATE_DONT_MATCH = public_config.getboolean(
    "settings", "skip_if_date_dont_match"
)
LOG_LEVEL = logging._nameToLevel[public_config.get("settings", "log_level").upper()]
READ_WEBPAGE_FROM_FILE = public_config.getboolean("settings", "read_webpage_from_file")
SAVE_TO_WEBPAGE_FILE = public_config.getboolean("settings", "save_to_webpage_file")
WEBPAGE_FILE_NAME = public_config.get("settings", "webpage_file_name")
NUMBER_OF_FETCHED_ALBUMS = public_config.getint("settings", "number_of_fetched_albums")
