import re
import time
import asyncio
import random
from pyrogram import Client, filters, enums
from config import CAPTION
from pyrogram.errors import FloodWait

# Define Source and Destination Channel IDs
SOURCE_CHANNEL_ID = -1002492867485  # Replace with your source channel ID
DEST_CHANNEL_ID = -1001855298932  # Replace with your destination channel ID

# Reversed Regex: Matches files that DO NOT contain episode-related patterns
NON_EPISODE_REGEX = re.compile(r"^(?!.*(s\d{1,2}[\.\s]?e[p]?\d{1,2}|season|\bepisode\b)).*$", re.IGNORECASE)

@Client.on_message(filters.channel & filters.chat(SOURCE_CHANNEL_ID))
async def auto_forward(client, message):
    """Automatically forwards non-episode files from source to destination"""
    try:
        if not message.media:
            return  # Skip if there's no media

        file_name = None
        file_size = None
        file_caption = message.caption if message.caption else ""

        # Extract media file details
        if message.document:
            file_name = message.document.file_name
            file_size = get_size(message.document.file_size)
        elif message.video:
            file_name = message.video.file_name
            file_size = get_size(message.video.file_size)
        elif message.audio:
            file_name = message.audio.file_name
            file_size = get_size(message.audio.file_size)

        # Check if file name DOES NOT match episode format
        if file_name and not NON_EPISODE_REGEX.match(file_name):
            print(f"Skipped: {file_name}")  # Log skipped message
            return
        
        # Forward the message with custom caption
        await client.copy_message(
            chat_id=DEST_CHANNEL_ID,
            from_chat_id=SOURCE_CHANNEL_ID,
            message_id=message.id,
            caption=CAPTION.format(file_name=file_name, file_size=file_size, file_caption=file_caption)
        )
        
        print(f"Forwarded: {file_name}")  # Log forwarded message

        # Add random sleep time to avoid API bans
        random_sleep_time = random.uniform(2, 5)
        await asyncio.sleep(random_sleep_time)

    except FloodWait as e:
        print(f"Flood Wait triggered! Waiting for {e.value + 1} seconds.")
        await asyncio.sleep(e.value + 1)
    except Exception as e:
        print(f"Error in forwarding: {e}")

def get_size(size):
    """Convert file size to human-readable format"""
    units = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB"]
    size = float(size)
    i = 0
    while size >= 1024.0 and i < len(units):
        i += 1
        size /= 1024.0
    return "%.2f %s" % (size, units[i])
    
