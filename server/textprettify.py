import re


# Set logging level: 0 - no logging, 1 - enable logging
log_level = 1  # Change this to 0 to disable logging

# Function to check if logging is enabled
def print_console(text):
    if log_level > 0:
        print(text)

def replace_with_dash(e):
    return (' - ', e.end)

def deEmojify(text):
    emoji_pattern = re.compile(
        "[" 
        u"\U0001F600-\U0001F64F"
        u"\U0001F300-\U0001F5FF"
        u"\U0001F680-\U0001F6FF"
        u"\U0001F1E0-\U0001F1FF"
        u"\U00002700-\U000027BF"
        u"\U00002600-\U000026FF"
        "]+",
        flags=re.UNICODE
    )

    text = emoji_pattern.sub(". ", text)

    # Fix merged words like "game.definitely" → "game. definitely"
    text = re.sub(r"([a-zA-Z])(\.)([a-zA-Z])", r"\1. \3", text)

    # Standard cleanup
    text = re.sub(r"\.\s*\.+", ".", text)
    text = re.sub(r"\s{2,}", " ", text)
    text = re.sub(r"\s+\.", ".", text)
    text = re.sub(r"\.\s*$", ".", text.strip())

    # Capitalize first word after sentence-ending period
    def capitalize_sentences(s):
        parts = re.split(r'(?<=[.!?])\s+', s)
        return ' '.join(part[0].upper() + part[1:] if part else '' for part in parts)

    return capitalize_sentences(text)

