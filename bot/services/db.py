import os
from supabase import create_client, Client
from dotenv import load_dotenv
import random
import logging
from datetime import datetime, timezone

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in .env")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

logger = logging.getLogger(__name__)


def get_active_vocab(word: str):
    response = supabase.table("active_vocab").select("*").eq("word", word).execute()
    return response.data


def insert_active_vocab(
    word: str, reading: str = None, meaning: str = None, priority: int = 1
):
    data = {
        "word": word,
        "reading": reading,
        "meaning": meaning,
        "priority": priority,
        "status": "active",
    }
    response = supabase.table("active_vocab").insert(data).execute()
    return response.data


def get_grammar_patterns(compatibility_tag: str = None):
    # In a real scenario, we might want to filter by compatibility
    # For now, let's just fetch all casual patterns
    response = (
        supabase.table("grammar_patterns")
        .select("*")
        .eq("register", "casual")
        .execute()
    )
    return response.data


def insert_example_phrase(
    vocab_id: str, grammar_id: str, sentence: str, meaning: str, note: str
):
    data = {
        "vocab_id": vocab_id,
        "grammar_id": grammar_id,
        "sentence_ja": sentence,
        "sentence_en": meaning,
        "usage_note": note,
    }
    response = supabase.table("example_phrases").insert(data).execute()
    return response.data


def get_random_active_vocab(limit: int = 3):
    # In a real app, use a proper random or LRU query.
    # Supabase/Postgres doesn't have a simple unique specific RANDOM() in simple select without RPC sometimes,
    # but let's try a simple fetch and shuffle in python for MVP if dataset is small.
    # Or just fetch top N.
    response = (
        supabase.table("active_vocab")
        .select("*")
        .eq("status", "active")
        .limit(50)
        .execute()
    )
    if response.data:
        return random.sample(response.data, k=min(limit, len(response.data)))
    return []


def get_grammar_pattern_by_text(text: str):
    response = (
        supabase.table("grammar_patterns").select("*").eq("pattern", text).execute()
    )
    return response.data


def get_random_example_phrase(limit: int = 1):
    # Retrieve a larger batch to select from randomly in memory to simulate random selection
    # Adjust limit as table grows
    response = supabase.table("example_phrases").select("*").limit(20).execute()
    if response.data:
        return random.sample(response.data, k=min(limit, len(response.data)))
    return []


def get_prioritized_example_phrase(limit: int = 1, sample_pool: int = 200):
    """Select example phrases preferring unused vocab first, then fewer-times-used.

    This fetches up to `sample_pool` example phrases, aggregates usage counts
    from `usage_history` grouped by `vocab_id`, and then chooses from the
    lowest-scoring bucket (unused first, then lower total times_used).
    """
    # Fetch a sample pool of example phrases to choose from
    resp = supabase.table("example_phrases").select("*").limit(sample_pool).execute()
    phrases = resp.data or []
    if not phrases:
        return []

    # Fetch usage history rows and aggregate times_used per vocab_id
    uh_resp = supabase.table("usage_history").select("vocab_id,times_used").execute()
    uh_rows = uh_resp.data or []
    totals: dict = {}
    for r in uh_rows:
        vid = r.get("vocab_id")
        if not vid:
            continue
        totals[vid] = totals.get(vid, 0) + (r.get("times_used") or 0)

    # Compute score: (used_flag, total_times_used) where used_flag=0 for unused (preferred)
    def score(p):
        vid = p.get("vocab_id")
        total = totals.get(vid, 0)
        used_flag = 0 if total == 0 else 1
        return (used_flag, total)

    # Bucket phrases by score
    buckets = {}
    for p in phrases:
        k = score(p)
        buckets.setdefault(k, []).append(p)

    best_score = min(buckets.keys())
    candidates = buckets[best_score]

    # Randomly choose up to `limit` from the best bucket
    chosen = random.sample(candidates, k=min(limit, len(candidates)))
    return chosen


def get_example_phrases_by_vocab_id(vocab_id: str):
    response = (
        supabase.table("example_phrases").select("*").eq("vocab_id", vocab_id).execute()
    )
    return response.data


def delete_active_vocab(vocab_id: str):
    # active_vocab cascade deletes example_phrases
    response = supabase.table("active_vocab").delete().eq("id", vocab_id).execute()
    return response.data

# Add helper to fetch an active_vocab row by id
def get_active_vocab_by_id(vocab_id: str):
    response = supabase.table("active_vocab").select("*").eq("id", vocab_id).execute()
    if response.data:
        return response.data[0]
    return None


def log_usage(vocab_id: str, grammar_id: str | None = None):
    """Record usage of a vocab/grammar pair in `usage_history`.

    If a row exists for (vocab_id, grammar_id) increment `times_used` and
    update `last_used`. Otherwise insert a new row.
    """
    if not vocab_id:
        logger.debug("log_usage called without vocab_id")
        return None

    # Build existence query: handle NULL grammar_id separately
    if grammar_id is None:
        existing = (
            supabase.table("usage_history")
            .select("*")
            .eq("vocab_id", vocab_id)
            .is_("grammar_id", None)
            .execute()
        )
    else:
        existing = (
            supabase.table("usage_history")
            .select("*")
            .eq("vocab_id", vocab_id)
            .eq("grammar_id", grammar_id)
            .execute()
        )

    now_iso = datetime.now(timezone.utc).isoformat()

    if existing.data and len(existing.data) > 0:
        row = existing.data[0]
        new_count = (row.get("times_used") or 0) + 1
        logger.info("Updating usage_history for vocab_id=%s grammar_id=%s times=%d", vocab_id, grammar_id, new_count)
        updated = (
            supabase.table("usage_history")
            .update({"times_used": new_count, "last_used": now_iso})
            .eq("id", row.get("id"))
            .execute()
        )
        return updated.data

    # Insert new usage row (let DB defaults handle last_used/times_used if desired)
    payload = {"vocab_id": vocab_id, "grammar_id": grammar_id}
    logger.info("Inserting usage_history for vocab_id=%s grammar_id=%s", vocab_id, grammar_id)
    inserted = supabase.table("usage_history").insert(payload).execute()
    return inserted.data