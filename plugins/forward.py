import re
import asyncio
import random
import logging
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait
from config import CAPTION

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define Source and Destination Channel IDs
SOURCE_CHANNEL_ID = -1002492867485  # Replace with your source channel ID
DEST_CHANNEL_ID = -1001855298932  # Replace with your destination channel ID

# Regex: Matches files that DO NOT contain episode-related patterns
NON_EPISODE_REGEX = re.compile(r"(?i)^(?!.*\b(?:S\d{2}E\d{2}|S\d{2}\s?EP\d{2}|S\d{2}\s?E\d{2}|Season\s?\d+\s?Episode\s?\d+|EP\d+|E\d{2}(-E\d{2,})?|combined|-\sS\d{2}E\d{2}\s-)\b).*(19\d{2}|20\d{2}).*", re.IGNORECASE)

# Queue for message forwarding
message_queue = asyncio.Queue()

async def process_queue(client):
    """Continuously process messages from the queue."""
    while True:
        message = await message_queue.get()
        if message:
            await forward_message(client, message)
        message_queue.task_done()

async def forward_message(client, message):
    """Handles message forwarding with optimized FloodWait handling."""
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

        # Check if file name or caption matches episode format
        if (file_name and not NON_EPISODE_REGEX.match(file_name)) and (file_caption and not NON_EPISODE_REGEX.match(file_caption)):
            logger.info(f"Skipped: {file_name or 'No filename'} | Caption: {file_caption}")
            return

        # Forward the message with a custom caption
        await client.copy_message(
            chat_id=DEST_CHANNEL_ID,
            from_chat_id=SOURCE_CHANNEL_ID,
            message_id=message.id,
            caption=CAPTION.format(file_name=file_name, file_size=file_size, file_caption=file_caption)
        )

        logger.info(f"Forwarded: {file_name}")

        # Add random sleep time to avoid API bans
        await asyncio.sleep(random.uniform(1, 3))

    except FloodWait as e:
        logger.warning(f"Flood Wait triggered! Waiting for {e.value + 1} seconds.")
        await asyncio.sleep(e.value + 1)
        await forward_message(client, message)  # Retry after waiting
    except Exception as e:
        logger.error(f"Error in forwarding: {e}")

@Client.on_message(filters.channel & filters.chat(SOURCE_CHANNEL_ID))
async def queue_message(client, message):
    """Adds messages to the processing queue."""
    await message_queue.put(message)

def get_size(size):
    """Convert file size to human-readable format."""
    units = ["Bytes", "KB", "MB", "GB", "TB"]
    size = float(size)
    i = 0
    while size >= 1024.0 and i < len(units) - 1:
        i += 1
        size /= 1024.0
    return "%.2f %s" % (size, units[i])

# Start processing queue
async def start_processing(client):
    asyncio.create_task(process_queue(client))
        
