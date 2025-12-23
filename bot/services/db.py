import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in .env")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_active_vocab(word: str):
    response = supabase.table("active_vocab").select("*").eq("word", word).execute()
    return response.data

def insert_active_vocab(word: str, reading: str = None, meaning: str = None, priority: int = 1):
    data = {
        "word": word,
        "reading": reading,
        "meaning": meaning,
        "priority": priority,
        "status": "active"
    }
    response = supabase.table("active_vocab").insert(data).execute()
    return response.data

def get_grammar_patterns(compatibility_tag: str = None):
    # In a real scenario, we might want to filter by compatibility
    # For now, let's just fetch all casual patterns
    response = supabase.table("grammar_patterns").select("*").eq("register", "casual").execute()
    return response.data

def insert_example_phrase(vocab_id: str, grammar_id: str, sentence: str, meaning: str, note: str):
    data = {
        "vocab_id": vocab_id,
        "grammar_id": grammar_id,
        "sentence_ja": sentence,
        "sentence_en": meaning,
        "usage_note": note
    }
    response = supabase.table("example_phrases").insert(data).execute()
    return response.data

def get_random_active_vocab(limit: int = 3):
    # In a real app, use a proper random or LRU query.
    # Supabase/Postgres doesn't have a simple unique specific RANDOM() in simple select without RPC sometimes, 
    # but let's try a simple fetch and shuffle in python for MVP if dataset is small.
    # Or just fetch top N.
    response = supabase.table("active_vocab").select("*").eq("status", "active").limit(50).execute()
    import random
    if response.data:
        return random.sample(response.data, k=min(limit, len(response.data)))
    return []

def get_grammar_pattern_by_text(text: str):
    response = supabase.table("grammar_patterns").select("*").eq("pattern", text).execute()
    return response.data

def get_random_example_phrase(limit: int = 1):
    # Retrieve a larger batch to select from randomly in memory to simulate random selection
    # Adjust limit as table grows
    response = supabase.table("example_phrases").select("*").limit(20).execute()
    import random
    if response.data:
        return random.sample(response.data, k=min(limit, len(response.data)))
    return []
