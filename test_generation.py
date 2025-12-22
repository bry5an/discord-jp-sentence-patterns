import asyncio
import os
from bot.services import db, llm
from dotenv import load_dotenv

load_dotenv()

async def test_workflow():
    print("--- Starting Test Workflow ---")
    
    # 1. Test Grammar Pattern fetching
    print("\n1. Fetching Grammar Patterns...")
    patterns = db.get_grammar_patterns("casual")
    if not patterns:
        print("⚠️ No grammar patterns found. Please seed the database.")
        # Attempt to seed one for testing
        # In real usage, user should run migrations/seeds. 
        # But we can't easily seed from python without a proper seed function or running sql.
        # Let's hope the user ran the seed.sql provided in the implementation plan logic (Step 16).
        return
    print(f"Found {len(patterns)} patterns.")
    test_pattern = patterns[0]
    print(f"Using pattern: {test_pattern['pattern']}")

    # 2. Test Vocab Insertion
    print("\n2. Testing Vocab Insertion...")
    test_word = "テスト"
    existing = db.get_active_vocab(test_word)
    if existing:
        print(f"Word {test_word} already exists, using it.")
        vocab_id = existing[0]['id']
    else:
        print(f"Inserting {test_word}...")
        res = db.insert_active_vocab(test_word, "てすと", "test usage")
        vocab_id = res[0]['id']
        print(f"Inserted vocab ID: {vocab_id}")

    # 3. Test Sentence Generation
    print("\n3. Testing Sentence Generation (LLM)...")
    sentences = await llm.generate_sentences(
        vocab=test_word,
        reading="てすと",
        meaning="test usage",
        grammar_pattern=test_pattern['pattern'],
        grammar_meaning=test_pattern.get('meaning', '')
    )
    
    if not sentences:
        print("❌ No sentences generated.")
    else:
        print(f"Generated {len(sentences)} sentences.")
        print(f"Example: {sentences[0]}")

    # 4. Test Storing Sentences
    print("\n4. Testing Storing Sentences...")
    for s in sentences:
        db.insert_example_phrase(
            vocab_id=vocab_id,
            grammar_id=test_pattern['id'],
            sentence=s['japanese'],
            meaning=s['english'],
            note=s.get('note', '')
        )
    print("✅ Stored sentences.")

if __name__ == "__main__":
    asyncio.run(test_workflow())
