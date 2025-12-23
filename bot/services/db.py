import os
from supabase import create_client, Client
from dotenv import load_dotenv
import random
import logging

load_dotenv()

logger = logging.getLogger(__name__)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in .env")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_active_vocab(word: str):
    logger.info("DB: get_active_vocab word=%s", word)
    response = supabase.table("active_vocab").select("*").eq("word", word).execute()
    logger.debug("DB: get_active_vocab returned rows=%s", len(response.data) if response.data else 0)
    return response.data

def insert_active_vocab(word: str, reading: str = None, meaning: str = None, priority: int = 1):
    data = {
        "word": word,
        "reading": reading,
        "meaning": meaning,
        "priority": priority,
        "status": "active"
    }
    logger.info("DB: insert_active_vocab word=%s", word)
    response = supabase.table("active_vocab").insert(data).execute()
    logger.debug("DB: insert_active_vocab response=%s", response.data)
    return response.data

def get_grammar_patterns(compatibility_tag: str = None):
    # In a real scenario, we might want to filter by compatibility
    # For now, let's just fetch all casual patterns
    logger.info("DB: get_grammar_patterns compatibility_tag=%s", compatibility_tag)
    response = supabase.table("grammar_patterns").select("*").eq("register", "casual").execute()
    logger.debug("DB: get_grammar_patterns returned rows=%s", len(response.data) if response.data else 0)
    return response.data

def insert_example_phrase(vocab_id: str, grammar_id: str, sentence: str, meaning: str, note: str):
    data = {
        "vocab_id": vocab_id,
        "grammar_id": grammar_id,
        "sentence_ja": sentence,
        "sentence_en": meaning,
        "usage_note": note
    }
    logger.info("DB: insert_example_phrase vocab_id=%s grammar_id=%s", vocab_id, grammar_id)
    response = supabase.table("example_phrases").insert(data).execute()
    logger.debug("DB: insert_example_phrase response=%s", response.data)
    return response.data

def get_random_active_vocab(limit: int = 3):
    # In a real app, use a proper random or LRU query.
    # Supabase/Postgres doesn't have a simple unique specific RANDOM() in simple select without RPC sometimes, 
    # but let's try a simple fetch and shuffle in python for MVP if dataset is small.
    # Or just fetch top N.
    logger.info("DB: get_random_active_vocab limit=%d", limit)
    response = supabase.table("active_vocab").select("*").eq("status", "active").limit(50).execute()
    if response.data:
        sample = random.sample(response.data, k=min(limit, len(response.data)))
        logger.debug("DB: get_random_active_vocab returning %d rows", len(sample))
        return sample
    logger.debug("DB: get_random_active_vocab returning empty list")
    return []

def get_grammar_pattern_by_text(text: str):
    logger.info("DB: get_grammar_pattern_by_text text=%s", text)
    response = supabase.table("grammar_patterns").select("*").eq("pattern", text).execute()
    logger.debug("DB: get_grammar_pattern_by_text returned rows=%s", len(response.data) if response.data else 0)
    return response.data

def get_random_example_phrase(limit: int = 1):
    # Retrieve a larger batch to select from randomly in memory to simulate random selection
    # Adjust limit as table grows
    logger.info("DB: get_random_example_phrase limit=%d", limit)
    response = supabase.table("example_phrases").select("*").limit(20).execute()
    if response.data:
        sample = random.sample(response.data, k=min(limit, len(response.data)))
        logger.debug("DB: get_random_example_phrase returning %d rows", len(sample))
        return sample
    logger.debug("DB: get_random_example_phrase returning empty list")
    return []

def get_example_phrases_by_vocab_id(vocab_id: str):
    logger.info("DB: get_example_phrases_by_vocab_id vocab_id=%s", vocab_id)
    response = supabase.table("example_phrases").select("*").eq("vocab_id", vocab_id).execute()
    logger.debug("DB: get_example_phrases_by_vocab_id returned rows=%s", len(response.data) if response.data else 0)
    return response.data

def delete_active_vocab(vocab_id: str):
    # active_vocab cascade deletes example_phrases
    logger.info("DB: delete_active_vocab vocab_id=%s", vocab_id)
    response = supabase.table("active_vocab").delete().eq("id", vocab_id).execute()
    logger.debug("DB: delete_active_vocab response=%s", response.data)
    return response.data
