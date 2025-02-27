import asyncio
import re
import random
import logging
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from config import SOURCE_CHAT, DEST_CHAT

# Configure Logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Regex to filter only movies
MOVIE_REGEX = re.compile(
    r"(?i)^(?!.*\b(?:S\d{2}E\d{2}|S\d{2}\s?EP\d{2}|S\d{2}\s?E\d{2}|Season\s?\d+\s?Episode\s?\d+|EP\d+|E\d{2}(-E\d{2,})?|combined|-\sS\d{2}E\d{2}\s-)\b).*(19\d{2}|20\d{2}).*"
)

@app.on_message(filters.chat(SOURCE_CHAT) & (filters.document | filters.video | filters.photo))
async def forward_movies(client, message):
    try:
        text = message.caption or ""
        
        if MOVIE_REGEX.search(text):
            await message.forward(DEST_CHAT)
            logging.info(f"✅ Forwarded: {text[:50]}...")
        else:
            logging.info(f"❌ Skipped (Not a movie): {text[:50]}...")
    
    except FloodWait as e:
        delay = random.randint(5, 20)  # Random floodwait handling
        logging.warning(f"⚠️ FloodWait: Sleeping for {delay}s")
        await asyncio.sleep(delay)

    except Exception as e:
        logging.error(f"❌ Error: {str(e)}")

logging.info("🚀 Live Movie Forwarding Bot is Running 24/7...")
