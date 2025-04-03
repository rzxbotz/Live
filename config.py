import os

API_ID = int(os.getenv("API_ID"))  # Telegram API ID
API_HASH = os.getenv("API_HASH")  # Telegram API Hash
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Telegram Bot Token
SESSION_NAME = "movie_forward_bot"  # Pyrogram Session Name

SOURCE_CHANNEL = int(os.getenv("SOURCE_CHANNEL"))  # Source Channel ID
DESTINATION_CHANNELS = list(map(int, os.getenv("DESTINATION_CHANNELS", "").split()))  # Multiple Destination Channel IDs
MONGO_URI = os.getenv("MONGO_URI")  # MongoDB Connection URI

CAPTION_TEMPLATE = os.getenv("CAPTION_TEMPLATE", "<b>{original_caption}</b>")  # Custom Caption Format

MOVIE_REGEX = r"^(?!.*\b(?:S\d{1,2}\s?EP?\(?\d{1,2}\)?|Season\s?\d+\s?Episode\s?\d+|E\d{1,2}(-E\d{1,2})?|combined)\b).*(19\d{2}|20\d{2}).*"
