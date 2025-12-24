from discord.ext import commands
from bot.services import db, llm

GRAMMAR_INBOX_CHANNEL = "grammar-inbox"


class GrammarCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        # Check if in the correct channel
        if message.channel.name != GRAMMAR_INBOX_CHANNEL:
            return

        grammar_text = message.content.strip()

        # Validation
        if not grammar_text:
            return

        # Check existing grammar
        existing = db.get_grammar_pattern_by_text(grammar_text)
        if not existing:
            # If it's not in our known grammar list, maybe we ignore it or tell the user?
            # For now, let's silently ignore or maybe add a "unknown grammar" emoji reaction?
            # The Requirement says: "Validate grammar exists in grammar_patterns".
            await message.add_reaction("❓")
            return

        grammar_data = existing[0]

        # Select 2-3 existing active vocab words
        vocab_list = db.get_random_active_vocab(limit=3)

        if not vocab_list:
            await message.reply("No active vocabulary found to practice with!")
            return

        processing_msg = await message.reply(
            f"Practicing {grammar_text} with {len(vocab_list)} words..."
        )

        generated_count = 0

        for vocab in vocab_list:
            sentences = await llm.generate_sentences(
                vocab=vocab["word"],
                reading=vocab.get("reading", ""),
                meaning=vocab.get("meaning", ""),
                grammar_pattern=grammar_data["pattern"],
                grammar_meaning=grammar_data.get("meaning", ""),
            )

            # Constraints: "One sentence per example" (per vocab word)
            # The LLM generates 2 by default, let's just pick 1 if valid.
            if sentences:
                s = sentences[0]  # Pick the first one
                db.insert_example_phrase(
                    vocab_id=vocab["id"],
                    grammar_id=grammar_data["id"],
                    sentence=s["japanese"],
                    meaning=s["english"],
                    note=s.get("note", ""),
                )
                generated_count += 1

        await processing_msg.edit(
            content=f"✅ Generated {generated_count} sentences for {grammar_text}"
        )


async def setup(bot):
    await bot.add_cog(GrammarCog(bot))
