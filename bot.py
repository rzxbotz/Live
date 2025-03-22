import logging
import asyncio
import time
import psutil
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

# Start time for uptime calculation
start_time = time.time()

async def get_bot_uptime():
    uptime_seconds = int(time.time() - start_time)
    uptime_minutes = uptime_seconds // 60
    uptime_hours = uptime_minutes // 60
    uptime_days = uptime_hours // 24
    uptime_string = f"{uptime_days % 7} Days : {uptime_hours % 24} Hours : {uptime_minutes % 60} Minutes : {uptime_seconds % 60} Seconds"
    return uptime_string

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

# Ping Command
@app.on_message(filters.command("ping"))
async def ping(_, message):
    start_t = time.time()
    rm = await message.reply_text("👀")
    end_t = time.time()
    
    time_taken_s = (end_t - start_t) * 1000
    uptime = await get_bot_uptime()
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    
    await rm.edit(
        f"🏓 𝖯𝗂𝗇𝗀: <code>{time_taken_s:.3f} ms</code>\n"
        f"⏰ 𝖴𝗉𝗍𝗂𝗆𝖾: <code>{uptime}</code>\n"
        f"🤖 𝖢𝖯𝖴 𝖴𝗌𝖺𝗀𝖾: <code>{cpu_usage} %</code>\n"
        f"📥 𝖱𝖺𝗆 𝖴𝗌𝖺𝗀𝖾: <code>{ram_usage} %</code>"
    )

# Start Command
@app.on_message(filters.command("start"))
async def check_alive(_, message):
    await message.reply_text("𝖡𝗎𝖽𝖽𝗒 𝖨 𝖺𝗆 𝖠𝗅𝗂𝗏𝖾 🗿", quote=True)

# Start bot and web server
async def main():
    """Start bot and web server asynchronously."""
    await start_web()
    await app.start()
    logger.info("Bot started successfully.")
    await asyncio.Event().wait()  # Keeps the bot running

# Fix AsyncIO Event Loop Issue
if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
    except RuntimeError:
        loop = asyncio.new_event_loop()  # Fixed syntax error
        asyncio.set_event_loop(loop)
        loop.run_until_complete(main())
        
