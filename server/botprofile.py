import sys

from textprettify import print_console # Internal

def get_ai_profile_payload(profile_name: str, style: str = "Neutral") -> str:
    payload_content =  f"Your name is {profile_name}, you are a conversational emotional support human and a so-called wingman, giving insightful opinions in \"{style}\" style about social interactions and human connection."
    print_console(f"Wingman: {profile_name}, style: {style}")

    return payload_content

# Optional test when running as script
if __name__ == "__main__":
    args = sys.argv[1:] # exclude script name
    if len(args) > 0: # name
        name = args[0] if len(args[0]) > 3 else "Max"
    else:
        name = "Max"
    if len(args) > 1: # style
        style = args[1] if len(args[1]) > 0 else "Friendly"
    else:
        style = "Friendly"

    get_ai_profile_payload(name, style)
