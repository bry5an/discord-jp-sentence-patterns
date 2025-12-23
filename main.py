import asyncio
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# Bot Setup
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")

async def main():
    if not DISCORD_TOKEN:
        print("Error: DISCORD_TOKEN not found in .env")
        return

    # Load extensions (Cogs)
    initial_extensions = [
        "bot.cogs.vocab",
        "bot.cogs.grammar",
        "bot.cogs.daily",
    ]

    for extension in initial_extensions:
        try:
            await bot.load_extension(extension)
        except Exception as e:
            print(f"Failed to load extension {extension}: {e}")

    await bot.start(DISCORD_TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
