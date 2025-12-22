import discord
from discord.ext import commands
from bot.services import db, llm, dictionary
import random

ACTIVE_VOCAB_CHANNEL = "active-vocab-inbox"

class VocabCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        # Check if in the correct channel
        if message.channel.name != ACTIVE_VOCAB_CHANNEL:
            return

        vocab_text = message.content.strip()
        
        # Validation (Step 1)
        if not vocab_text or len(vocab_text) > 20: # arbitrary simple validation
            return

        # Check existing
        existing = db.get_active_vocab(vocab_text)
        if existing:
            await message.reply("Already added 👍")
            return

        # Dictionary Enrichment (Step 2)
        vocab_data = dictionary.lookup_word(vocab_text)

        # Insert into DB
        try:
            vocab_entry = db.insert_active_vocab(
                word=vocab_data.word,
                reading=vocab_data.reading,
                meaning=vocab_data.meaning
            )
            # db.insert_active_vocab returns a list of results (data) or similar depending on supabase-py version
            # Assuming it returns the inserted row(s) in 'data' list.
            if vocab_entry:
                vocab_id = vocab_entry[0]['id']
            else:
                await message.reply("Error adding vocab to DB.")
                return

        except Exception as e:
            await message.reply(f"Error saving to DB: {e}")
            return

        # Simple ACK to say we are working on it
        processing_msg = await message.reply("👀 Generating sentences...")

        # Select Grammar Patterns (Step 3)
        # Fetch casual patterns
        patterns = db.get_grammar_patterns(compatibility_tag="casual")
        
        # Randomly select 2-3
        if not patterns:
            await processing_msg.edit(content="✅ Added, but no grammar patterns found for generation.")
            return

        selected_patterns = random.sample(patterns, k=min(2, len(patterns)))
        
        generated_count = 0

        # Generate Sentences (Step 4 & 5)
        for pattern in selected_patterns:
            sentences = await llm.generate_sentences(
                vocab=vocab_data.word,
                reading=vocab_data.reading,
                meaning=vocab_data.meaning,
                grammar_pattern=pattern['pattern'],
                grammar_meaning=pattern.get('meaning', '')
            )

            for s in sentences:
                db.insert_example_phrase(
                    vocab_id=vocab_id,
                    grammar_id=pattern['id'],
                    sentence=s['japanese'],
                    meaning=s['english'],
                    note=s.get('note', '')
                )
                generated_count += 1
        
        # Confirmation (Step 6)
        await processing_msg.edit(content=f"✅ {vocab_text} added\n• {generated_count} grammar-based speaking examples generated")

async def setup(bot):
    await bot.add_cog(VocabCog(bot))
