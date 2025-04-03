import logging
import re
import asyncio
from config import SOURCE_CHANNEL, DESTINATION_CHANNELS, MOVIE_REGEX, CAPTION_TEMPLATE

async def forward_message(client, message, collection):
    try:
        if message.chat.id != SOURCE_CHANNEL:
            return

        # Extract filename if it's a document
        file_name = message.document.file_name if message.document else "Unknown File"

        # Check if message matches regex pattern
        if MOVIE_REGEX and not re.search(MOVIE_REGEX, message.caption or ""):
            logging.info(f"⚠️ Skipped: {file_name} (Does not match regex)")
            return  # Skip if it doesn't match

        # Check if message was already forwarded
        exists = await collection.find_one({"message_id": message.id})
        if exists:
            logging.info(f"⚠️ Skipped: {file_name} (Already forwarded)")
            return

        # Format caption
        original_caption = message.caption or ""
        new_caption = CAPTION_TEMPLATE.format(original_caption=original_caption, file_name=file_name)

        # Forward with modified caption to multiple channels
        for channel in DESTINATION_CHANNELS:
            if message.text:
                await client.send_message(
                    chat_id=channel,
                    text=new_caption,
                    reply_to_message_id=message.id if message.media else None
                )
            else:
                await client.copy_message(
                    chat_id=channel,
                    from_chat_id=SOURCE_CHANNEL,
                    message_id=message.id,
                    caption=new_caption
                )
            logging.info(f"✅ Forwarded: {file_name} to {channel}")

        # Save forwarded message ID in database
        await collection.insert_one({"message_id": message.id})
    
    except Exception as e:
        logging.error(f"❌ Error forwarding {file_name}: {e}")
        await asyncio.sleep(5)  # Floodwait prevention - retry after delay
