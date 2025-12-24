import discord
from discord.ext import commands


class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # correct usage is to remove default help command in main or here.
        # often easier to do in cog load/unload.
        self._original_help_command = bot.help_command
        bot.help_command = None

    def cog_unload(self):
        self.bot.help_command = self._original_help_command

    @commands.command(name="help")
    async def help_command(self, ctx):
        """Shows this help message."""

        embed = discord.Embed(
            title="🇯🇵 Bot Commands & Features",
            description="Here is what I can do to help you learn Japanese!",
            color=discord.Color.blurple(),
        )

        # General Commands
        embed.add_field(
            name="🛠️ Commands",
            value=(
                "`!daily_vocab`\n"
                "Manually trigger the daily vocabulary post.\n\n"
                "`!remove_vocab <word>`\n"
                "Remove a word and its sentences from the database.\n"
            ),
            inline=False,
        )

        # Features
        embed.add_field(
            name="📥 Automation Channels",
            value=(
                "**#active-vocab-inbox**\n"
                "Type a Japanese word here to add it to your list. "
                "The bot will look it up and generate sentences.\n\n"
                "**#grammar-inbox**\n"
                "Type a grammar pattern here (exact match) to generate new sentences "
                "using your active vocabulary.\n"
            ),
            inline=False,
        )

        embed.add_field(
            name="📅 Daily Drill",
            value=(
                "**#vocab-daily**\n"
                "I will post a random sentence from your collection every day at midnight UTC."
            ),
            inline=False,
        )

        embed.set_footer(text="Ganbatte! (Good luck!)")

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(HelpCog(bot))
