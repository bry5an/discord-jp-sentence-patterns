import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY must be set in .env")

# Initialize the client for the new SDK
client = genai.Client(api_key=GEMINI_API_KEY)

# Use gemini-flash-latest
MODEL_ID = "gemini-3-flash-preview"


async def generate_sentences(
    vocab: str,
    reading: str,
    meaning: str,
    grammar_pattern: str,
    grammar_meaning: str = "",
):
    prompt = f"""
    You are helping an adult male Japanese learner practice spoken Japanese.
    
    Generate 2 short, natural, casual spoken Japanese sentences.
    
    Target Vocabulary: {vocab} ({reading}) - {meaning}
    Target Grammar Pattern: {grammar_pattern} {f"({grammar_meaning})" if grammar_meaning else ""}
    
    Constraints:
    - Must use the word: {vocab}
    - Must use the grammar pattern: {grammar_pattern}
    - Avoid workplace or school settings
    - Use casual, everyday contexts e.g., chatting with friends, family (particularly to small children or wife), shopping
    - First-person if possible
    - Avoid rare or stiff/formal vocabulary
    - One sentence per example
    
    Output Format:
    Return a JSON array of objects, where each object has:
    - "japanese": The Japanese sentence
    - "english": Natural English translation
    - "note": A short conversational usage note (e.g. "Used when complaining lightly")
    
    Example Output:
    [
        {{
            "japanese": "ねえ、この映画、気になってるんだけど、一緒に見に行かない？",
            "english": "Hey, I'm curious about this movie, wanna go see it together?",
            "note": "Inviting a friend casually"
        }}
    ]
    """

    try:
        # Use aio (asyncio) client
        response = await client.aio.models.generate_content(
            model=MODEL_ID,
            contents=prompt,
            config=types.GenerateContentConfig(response_mime_type="application/json"),
        )
        return json.loads(response.text)
    except Exception as e:
        print(f"Error generating sentences: {e}")
        return []
