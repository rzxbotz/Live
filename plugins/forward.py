import re
import asyncio
import random
from pyrogram import Client, filters
from config import CAPTION, SOURCE_CHANNEL_ID, DESTINATION_CHANNEL_ID

app = Client("live_movie_forward_bot")

# Updated movie regex pattern
MOVIE_REGEX = r"(?i)^(?!.*\b(S\d{1,2}E\d{1,2}|Season\s?\d+|Episode\s?\d+|E\d{2}(-E\d{2,})?|EP\d{1,2}|Part\s?\d+|Complete|Dual\s?Audio|Collection|Pack|Vol\s?\d+)\b).*(19\d{2}|20\d{2}).*"

@app.on_message(filters.channel & filters.chat(SOURCE_CHANNEL_ID))
async def auto_forward(client, message):
    """Automatically forwards only movies from SOURCE_CHANNEL to DESTINATION_CHANNEL"""

    # Check if message contains media (Only forward media messages)
    if not message.media:
        print(f"❌ Skipped (No Media) - Message ID: {message.message_id}")
        return

    file_name = None
    file_size = None
    file_caption = message.caption if message.caption else ""

    if message.document:
        file_name = message.document.file_name
        file_size = get_size(message.document.file_size)
    elif message.video:
        file_name = message.video.file_name
        file_size = get_size(message.video.file_size)

    # Check if the file name matches a movie pattern
    if not file_name or not re.search(MOVIE_REGEX, file_name.lower()):
        print(f"⏭️ Skipped (Not a Movie) - {file_name}")
        return

    try:
        # Forward message with formatted caption
        await client.copy_message(
            chat_id=DESTINATION_CHANNEL_ID,
            from_chat_id=SOURCE_CHANNEL_ID,
            message_id=message.message_id,
            caption=CAPTION.format(file_name=file_name, file_size=file_size, file_caption=file_caption)
        )
        print(f"✅ Forwarded Movie - {file_name}")

    except Exception as e:
        print(f"❌ Error Forwarding Message: {e}")

    # Random sleep (2 to 5 seconds) to prevent spam
    await asyncio.sleep(random.uniform(2, 5))

def get_size(size):
    """Get size in readable format"""
    units = ["Bytes", "KB", "MB", "GB", "TB"]
    size = float(size)
    i = 0
    while size >= 1024.0 and i < len(units):
        i += 1
        size /= 1024.0
    return "%.2f %s" % (size, units[i])

print("✅ Live Movie Forwarding Bot is Running 24/7...")
app.run()
