from bot.services import db
import asyncio

async def main():
    print("Testing get_random_example_phrase...")
    try:
        phrases = db.get_random_example_phrase()
        print(f"Result type: {type(phrases)}")
        print(f"Result count: {len(phrases)}")
        if phrases:
            print("First phrase sample:", phrases[0].get('sentence_ja'))
        else:
            print("No phrases returned (might be empty DB).")
        print("✅ DB Verification Successful")
    except Exception as e:
        print(f"❌ DB Verification Failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
