import re
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)  # keep only letters
    words = [w for w in text.split() if w not in ENGLISH_STOP_WORDS]
    return " ".join(words)
