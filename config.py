import os

API_ID = int(os.getenv("API_ID", ""))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
SESSION_NAME = "movie_forward_bot"

SOURCE_CHANNEL = int(os.getenv("SOURCE_CHANNEL", ""))
DESTINATION_CHANNEL = list(map(int, os.getenv("DESTINATION_CHANNELS", "").split(',')))

MONGO_URI = os.getenv("MONGO_URI", "")
CAPTION_TEMPLATE = os.getenv("CAPTION_TEMPLATE", "<b>{original_caption}</b>")

MOVIE_REGEX = r"(?i)^(?!.*\b(?:S\d{2}E\d{2}|S\d{2}\s?EP\d{2}|S\d{2}\s?E\d{2}|Season\s?\d+\s?Episode\s?\d+|EP\d+|E\d{2}(-E\d{2,})?|combined|-\sS\d{2}E\d{2}\s-)\b).*(19\d{2}|20\d{2}).*"
