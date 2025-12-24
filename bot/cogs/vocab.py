import discord
from discord.ext import commands
from bot.services import db, llm, dictionary
import logging
import random
from bot.config import ACTIVE_VOCAB_CHANNEL

class VocabCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        logger = logging.getLogger(__name__)
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        # Check if in the correct channel
        if message.channel.name != ACTIVE_VOCAB_CHANNEL:
            return

        vocab_text = message.content.strip()
        logger.info("Vocab inbox: received '%s' from %s in %s", vocab_text, message.author, message.channel.name)
        
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
        logger.info("Selected %d grammar patterns for %s", len(selected_patterns), vocab_text)
        
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

    @commands.command(name="remove_vocab")
    async def remove_vocab(self, ctx, *, word: str):
        """Removes a vocabulary word and all associated sentences."""
        
        # 1. Check if word exists
        # We need a way to get ID from word. 
        # reusing get_active_vocab which returns a list
        existing = db.get_active_vocab(word)
        if not existing:
            await ctx.send(f"❌ Vocabulary word **{word}** not found.")
            return

        vocab_entry = existing[0]
        vocab_id = vocab_entry['id']
        
        # 2. Fetch sentences to show what will be deleted
        phrases = db.get_example_phrases_by_vocab_id(vocab_id)
        phrase_count = len(phrases)
        
        # 3. Confirmation Embed
        embed = discord.Embed(
            title=f"🗑️ Remove '{word}'?",
            description=f"This will delete the word and **{phrase_count}** associated example sentences.",
            color=discord.Color.red()
        )
        
        if phrases:
            preview_text = "\n".join([f"• {p['sentence_ja']}" for p in phrases[:3]])
            if phrase_count > 3:
                preview_text += f"\n...and {phrase_count - 3} more."
            embed.add_field(name="Sentences to be deleted:", value=preview_text, inline=False)
            
        embed.set_footer(text="React with ✅ to confirm or wait 30s to cancel.")
        
        confirmation_msg = await ctx.send(embed=embed)
        await confirmation_msg.add_reaction("✅")

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == "✅" and reaction.message.id == confirmation_msg.id

        try:
            import asyncio
            await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
        except asyncio.TimeoutError:
            await confirmation_msg.edit(content="❌ Deletion cancelled (timed out).", embed=None)
            await confirmation_msg.clear_reactions()
            return

        # 4. Delete
        try:
            db.delete_active_vocab(vocab_id)
            await confirmation_msg.edit(content=f"✅ Successfully deleted **{word}** and {phrase_count} sentences.", embed=None)
            await confirmation_msg.clear_reactions()
        except Exception as e:
            await confirmation_msg.edit(content=f"❌ Error deleting: {e}", embed=None)

async def setup(bot):
    await bot.add_cog(VocabCog(bot))
