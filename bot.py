from pyrogram import Client, __version__, idle
from pyrogram.raw.all import layer
from config import API_ID, API_HASH, BOT_TOKEN
import logging

# Configure Logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="forward-bot",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=50,
            plugins={"root": "plugins"},
            sleep_threshold=5,
        )

    async def start(self):
        await super().start()
        me = await self.get_me()
        logging.info(f"🚀 {me.first_name} (v{__version__}, Layer {layer}) started as @{me.username}")
        await idle()  # Keeps bot running

    async def stop(self, *args):
        await super().stop()
        logging.info("❌ Bot stopped.")

app = Bot()
app.run()
