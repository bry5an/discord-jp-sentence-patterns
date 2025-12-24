import discord
from discord.ext import commands, tasks
from bot.services import db
from bot.config import VOCAB_DAILY_CHANNEL, TIME_TO_POST


class DailyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.daily_post_loop.start()

    def cog_unload(self):
        self.daily_post_loop.cancel()

    async def post_random_vocab(self, channel):
        phrases = db.get_random_example_phrase(limit=1)
        if not phrases:
            await channel.send("Could not find any vocabulary phrases to post!")
            return

        phrase = phrases[0]

        # Fetch vocab metadata (reading/meaning) from active_vocab
        vocab = db.get_active_vocab_by_id(phrase.get("vocab_id"))
        reading = vocab.get("reading") if vocab else None
        # meaning = vocab.get("meaning") if vocab else None

        # Create Embed
        embed = discord.Embed(
            title="🇯🇵 Daily Japanese Vocabulary",
            description="Here is your daily sentence practice!",
            color=discord.Color.green(),
        )

        embed.add_field(name="Japanese", value=phrase["sentence_ja"], inline=False)
        if reading:
            embed.add_field(name="Reading", value=reading, inline=False)
        # if meaning:
        #     embed.add_field(name="Meaning", value=meaning, inline=False)
        if phrase.get("sentence_en"):
            # hide English translation behind a Discord spoiler
            embed.add_field(
                name="English", value=f"||{phrase['sentence_en']}||", inline=False
            )

        if phrase.get("usage_note"):
            embed.add_field(name="Note", value=phrase["usage_note"], inline=False)

        await channel.send(embed=embed)

        # Log usage in DB (records last used and increments times_used)
        try:
            db.log_usage(phrase.get("vocab_id"), phrase.get("grammar_id"))
        except Exception as e:
            # Avoid crashing the bot if DB logging fails
            print(f"Failed to log usage_history: {e}")

    @tasks.loop(time=TIME_TO_POST)
    async def daily_post_loop(self):
        # Find channel
        channel = discord.utils.get(
            self.bot.get_all_channels(), name=VOCAB_DAILY_CHANNEL
        )
        if channel:
            await self.post_random_vocab(channel)
        else:
            print(f"Channel {VOCAB_DAILY_CHANNEL} not found.")

    @daily_post_loop.before_loop
    async def before_daily_post_loop(self):
        await self.bot.wait_until_ready()

    @commands.command(name="daily_vocab")
    async def daily_vocab_command(self, ctx):
        """Manually trigger the daily vocab post."""
        await self.post_random_vocab(ctx.channel)


async def setup(bot):
    await bot.add_cog(DailyCog(bot))
