import re
import asyncio
import random
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from config import CAPTION

# Define Source and Destination Channel IDs
SOURCE_CHANNEL_ID = -1002492867485  # Replace with your source channel ID
DEST_CHANNEL_ID = -1001855298932  # Replace with your destination channel ID

# Regex to match non-episode content
NON_EPISODE_REGEX = re.compile(
    r"(?i)^(?!.*\b(?:S\d{2}E\d{2}|S\d{2}\s?EP\d{2}|S\d{2}\s?E\d{2}|Season\s?\d+\s?Episode\s?\d+|EP\d+|E\d{2}(-E\d{2,})?|combined|-\sS\d{2}E\d{2}\s-)\b).*(19\d{2}|20\d{2}).*",
    re.IGNORECASE,
)

# Initialize queue for message processing
message_queue = asyncio.Queue()


async def process_queue(client):
    """Continuously processes messages from the queue."""
    while True:
        message = await message_queue.get()
        if message is None:
            continue  # Ignore if queue is empty (shouldn't happen)

        while True:  # Retry loop for FloodWait handling
            try:
                if not message.media:
                    continue  # Skip if there's no media

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

                # Skip if file is an episode
                if (file_name and NON_EPISODE_REGEX.match(file_name)) or (
                    file_caption and NON_EPISODE_REGEX.match(file_caption)
                ):
                    print(f"Skipped: {file_name or 'No filename'} | Caption: {file_caption}")
                    break  # Exit retry loop, move to next message

                # Forward the message with custom caption
                await client.copy_message(
                    chat_id=DEST_CHANNEL_ID,
                    from_chat_id=SOURCE_CHANNEL_ID,
                    message_id=message.id,
                    caption=CAPTION.format(file_name=file_name, file_size=file_size, file_caption=file_caption),
                )

                print(f"Forwarded: {file_name}")

                # Add random sleep time to avoid API bans
                await asyncio.sleep(random.uniform(2, 5))
                break  # Exit retry loop after success

            except FloodWait as e:
                wait_time = e.value + random.randint(1, 5)  # Random buffer to avoid bans
                print(f"FloodWait triggered! Sleeping for {wait_time} seconds.")
                await asyncio.sleep(wait_time)

            except Exception as e:
                print(f"Error processing message: {e}")
                break  # Exit retry loop, move to next message


@Client.on_message(filters.channel & filters.chat(SOURCE_CHANNEL_ID))
async def auto_forward(client, message):
    """Adds messages to the queue for processing."""
    await message_queue.put(message)


async def fetch_unread_messages(client):
    """Fetches the last 50 messages from the source channel to process missed messages."""
    try:
        async for message in client.get_chat_history(SOURCE_CHANNEL_ID, limit=50):
            await message_queue.put(message)
        print("Fetched unread messages and added to queue.")
    except Exception as e:
        print(f"Error fetching unread messages: {e}")


async def main():
    """Starts the bot and processing queue."""
    async with Client("my_bot") as client:
        # Fetch missed messages on startup
        await fetch_unread_messages(client)

        # Start processing queue
        asyncio.create_task(process_queue(client))

        print("Bot is running...")
        await client.run()  # Keep bot running


def get_size(size):
    """Convert file size to human-readable format."""
    units = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB"]
    size = float(size)
    i = 0
    while size >= 1024.0 and i < len(units) - 1:
        i += 1
        size /= 1024.0
    return "%.2f %s" % (size, units[i])


if __name__ == "__main__":
    asyncio.run(main())
