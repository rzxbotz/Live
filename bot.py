import logging
import asyncio
import aiohttp
from pyrogram import Client, filters
from motor.motor_asyncio import AsyncIOMotorClient
from config import API_ID, API_HASH, BOT_TOKEN, MONGO_URI, SESSION_NAME, SOURCE_CHANNEL
from plugins.forward import forward_message

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Initialize Pyrogram client
app = Client(SESSION_NAME, api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Initialize MongoDB
mongo_client = AsyncIOMotorClient(MONGO_URI)
db = mongo_client["movie_forwarder"]
collection = db["messages"]

# Web support using aiohttp
from aiohttp import web

async def index(request):
    return web.Response(text="✅ Movie Forward Bot is running!")

web_app = web.Application()
web_app.router.add_get("/", index)

async def start_web():
    runner = web.AppRunner(web_app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8080)
    await site.start()

# Listener for new messages in the source channel
@app.on_message(filters.channel & filters.chat(SOURCE_CHANNEL))
async def handle_new_message(client, message):
    await forward_message(client, message, collection)

# Start bot and web server
async def main():
    """Start bot and web server asynchronously."""
    await start_web()
    await app.start()
    logger.info("Bot started successfully.")
    await asyncio.Event().wait()  # Keeps the bot running without conflicts

# Fix AsyncIO Event Loop Issue
if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(main())
