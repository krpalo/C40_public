import json
import os
import sys

from pydantic import BaseModel
from typing import List

from textprettify import print_console # Internal

class UserProfile(BaseModel):
    name: str
    interests: List[str]

DATA_FILE = os.path.join(os.path.dirname(__file__), "resources", "userprofiles.json")


def load_profiles():
    global profiles
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            profiles = {key.lower(): UserProfile(name=value["name"], interests=value["interests"]) for key, value in data.items()}
    return profiles

def save_profiles_to_file():
    # Load the existing profiles from the file first
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        # If the file doesn't exist, initialize with an empty dictionary
        data = {}

    # Update the existing data with the current profiles
    for normalized_name, profile in profiles.items():
        # Keep the original casing for `name`, while using normalized lowercase as the key
        data[normalized_name] = profile.model_dump()

    # Write the updated profiles back to the file
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_user_profile_payload(profile_name: str) -> dict:
    key = profile_name.strip().lower()

    if key not in profiles:
        return "undefined"

    # Check if category exists, and gather keywords
    interests = profiles[key].interests
    interests_summary = ", ".join(interests)
    payload_content =  f"My name is {profile_name}. My interests include: {interests_summary}."
    print_console(f"User profile payload: {payload_content}")

    return payload_content

# Optional test when running as script
if __name__ == "__main__":
    args = sys.argv[1:] # exclude script name
    if len(args) > 0: # name
        name = args[0] if len(args[0]) > 3 else "anonymous"
    else:
        name = "anonymous"

    get_user_profile_payload(name)
