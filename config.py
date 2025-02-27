import os

API_ID = int(os.getenv("API_ID"))  # Telegram API ID
API_HASH = os.getenv("API_HASH")  # Telegram API Hash
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Telegram Bot Token
SESSION_NAME = "movie_forward_bot"  # Pyrogram Session Name

SOURCE_CHANNEL = int(os.getenv("SOURCE_CHANNEL"))  # Source Channel ID
DESTINATION_CHANNEL = int(os.getenv("DESTINATION_CHANNEL"))  # Destination Channel ID
MONGO_URI = os.getenv("MONGO_URI")  # MongoDB Connection URI
REGEX_PATTERN = os.getenv("REGEX_PATTERN", "")  # Optional Regex Pattern for filtering messages
CAPTION_TEMPLATE = os.getenv("CAPTION_TEMPLATE", "{original_caption}")  # Custom Caption Format
