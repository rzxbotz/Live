import os

API_ID = int(os.getenv("API_ID", 17427408))  # Telegram API ID
API_HASH = os.getenv("API_HASH", "9699e632de895e7d566c241615a0e637")  # Telegram API Hash
BOT_TOKEN = os.getenv("BOT_TOKEN", "7391030602:AAHHBkz1f6c9Zc13hGHzE587TKdUcD6Uf_A")  # Telegram Bot Token
SESSION_NAME = "movie_forward_bot"  # Pyrogram Session Name

SOURCE_CHANNEL = int(os.getenv("SOURCE_CHANNEL", -1002492867485))  # Source Channel ID
DESTINATION_CHANNEL = int(os.getenv("DESTINATION_CHANNEL", -1001855298932))  # Destination Channel ID
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://dudemusic111:dudemusic111@cluster0.df3yis2.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")  # MongoDB Connection URI

CAPTION_TEMPLATE = os.getenv("CAPTION_TEMPLATE", "<b>{original_caption}</b>")  # Custom Caption Format
