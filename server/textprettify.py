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
    # Define emoji pattern more precisely, excluding em dash (—)
    emoji_pattern = re.compile(
        "[" 
        u"\U0001F600-\U0001F64F"  # Emoticons
        u"\U0001F300-\U0001F5FF"  # Symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # Transport & map
        u"\U0001F1E0-\U0001F1FF"  # Flags
        u"\U00002600-\U000026FF"  # Misc symbols
        # Skipping u"\u2700-\u27BF" to avoid catching em dash or useful dashes
        "]+",
        flags=re.UNICODE
    )

    # Remove emoji after punctuation cleanly
    text = re.sub(r'([.!?])\s*' + emoji_pattern.pattern, r'\1', text)

    # Remove other emojis with space (not extra punctuation)
    text = emoji_pattern.sub(" ", text)

    # Fix merged words like "game.definitely" → "game. definitely"
    text = re.sub(r"([a-zA-Z])(\.)([a-zA-Z])", r"\1. \3", text)

    # Normalize whitespace and punctuation
    text = re.sub(r"\.\s*\.+", ".", text)
    text = re.sub(r"\s{2,}", " ", text)
    text = re.sub(r"\s+\.", ".", text)
    text = re.sub(r"\.\s*$", ".", text.strip())

    # Capitalize first word after sentence-ending punctuation
    def capitalize_sentences(s):
        return re.sub(r'(?<=[.!?])\s+([a-z])', lambda m: ' ' + m.group(1).upper(), s[0].upper() + s[1:])

    return capitalize_sentences(text)

