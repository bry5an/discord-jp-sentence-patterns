import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY must be set in .env")

genai.configure(api_key=GEMINI_API_KEY)

# Use a model that supports JSON mode if possible, or just prompt carefully.
# gemini-1.5-flash is good for this.
model = genai.GenerativeModel("gemini-flash-latest")

async def generate_sentences(vocab: str, reading: str, meaning: str, grammar_pattern: str, grammar_meaning: str = ""):
    prompt = f"""
    You are helping an adult male Japense learner practice spoken Japanese.
    
    Generate 2 short, natural, casual spoken Japanese sentences.
    
    Target Vocabulary: {vocab} ({reading}) - {meaning}
    Target Grammar Pattern: {grammar_pattern} {f'({grammar_meaning})' if grammar_meaning else ''}
    
    Constraints:
    - Must use the word: {vocab}
    - Must use the grammar pattern: {grammar_pattern}
    - First-person if possible
    - Sound like everyday conversation between friends
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
        response = await model.generate_content_async(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        return json.loads(response.text)
    except Exception as e:
        print(f"Error generating sentences: {e}")
        return []
