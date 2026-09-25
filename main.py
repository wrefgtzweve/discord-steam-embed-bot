import interactions
import os
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] - %(levelname)s - %(message)s")

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intent = interactions.Intents.new(
    default=True,
    message_content=True
)

bot = interactions.Client(
    token=DISCORD_TOKEN,
    intents=intent,
    send_command_tracebacks=False,
    delete_unused_application_cmds=True
)
bot.load_extension("modules.steam_embed")


@interactions.listen()
async def on_ready():
    print("SteamEmbed Started")

bot.start()