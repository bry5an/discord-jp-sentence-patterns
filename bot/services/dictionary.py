import requests
from urllib.parse import quote

class DictionaryResult:
    def __init__(self, word, reading=None, meaning=None):
        self.word = word
        self.reading = reading if reading else ""
        self.meaning = meaning if meaning else ""

def lookup_word(word: str) -> DictionaryResult:
    """
    Look up a word on Jisho.org (unofficial API).
    Returns a DictionaryResult with the top match.
    """
    try:
        # Jisho has a "pubic" API endpoint
        url = f"https://jisho.org/api/v1/search/words?keyword={quote(word)}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if not data['data']:
            return DictionaryResult(word, reading="", meaning="")
            
        first_match = data['data'][0]
        
        # Get reading (furigana)
        # Japanese array usually has objects with 'word' and 'reading'.
        japanese_entry = first_match.get('japanese', [{}])[0]
        reading = japanese_entry.get('reading', '')
        # If the word itself is kana only, reading might be the word, or empty.
        
        # Get meanings (senses)
        senses = first_match.get('senses', [])
        meanings_list = []
        for sense in senses[:3]: # grab top 3 senses
            english_definitions = sense.get('english_definitions', [])
            meanings_list.extend(english_definitions)
            
        meaning_str = ", ".join(meanings_list[:5]) # join top 5 definitions
        
        return DictionaryResult(word, reading=reading, meaning=meaning_str)

    except Exception as e:
        print(f"Error checking dictionary: {e}")
        return DictionaryResult(word, reading="", meaning="")
