import os

API_ID = int(os.getenv("API_ID"))  # Telegram API ID
API_HASH = os.getenv("API_HASH")  # Telegram API Hash
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Telegram Bot Token
SESSION_NAME = "movie_forward_bot"  # Pyrogram Session Name

SOURCE_CHANNEL = int(os.getenv("SOURCE_CHANNEL"))  # Source Channel ID
DESTINATION_CHANNEL = int(os.getenv("DESTINATION_CHANNEL"))  # Destination Channel ID
MONGO_URI = os.getenv("MONGO_URI")  # MongoDB Connection URI

CAPTION_TEMPLATE = os.getenv("CAPTION_TEMPLATE", "<b>{original_caption}</b>")  # Custom Caption Format

MOVIE_REGEX = r"(?i)^(?!.*\b(?:S\d{2}E\d{2}|S\d{2}\s?EP\d{2}|S\d{2}\s?E\d{2}|Season\s?\d+\s?Episode\s?\d+|EP\d+|E\d{2}(-E\d{2,})?|combined|-\sS\d{2}E\d{2}\s-)\b).*(19\d{2}|20\d{2}).*"
