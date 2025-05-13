from openai import OpenAI, OpenAIError, RateLimitError
import json
import os

from botprofile import get_ai_profile_payload # Internal
from userprofile import get_user_profile_payload # Internal
from textprettify import deEmojify, print_console # Internal

with open(os.path.join(os.path.dirname(__file__), "resources", "config.json")) as f:
    config = json.load(f)

client = OpenAI(
  api_key=config["chatgpt_api_key"]
)

default_response = {
    "choices": [{
        "message": {
            "role": "wingman",
            "content": "Sorry, I can't connect to the server right now. Here's a default response while we're offline."
        }
    }]
}

# Not used - implement fallback service, when premium is over rate limit
def completions_with_fallback(fallback_model: str, payload_bot: str, payload_user: str):
    try:
        return client.chat.completions.create(
            model="gpt-4o-mini",
            store=True,
            messages=[payload_bot, payload_user]
        )
    except RateLimitError:
        print_console("Primary model hit rate limit, falling back...")
        return client.chat.completions.create(
            model=fallback_model,
            store=True,
            messages=[payload_bot, payload_user]
        )
    except OpenAIError as e:
        print_console(f"OpenAI API call failed: {e}")
        return default_response  # Or re-raise if appropriate


def get_improved_input(user_input, style, category, profile_info, previous_input=None, previous_output=None):
    prompt_parts = [
        "We are close friends having a discussion with these parameters:",
        f"My profile: {profile_info}",
        f"Category: {category}",
    ]
    
    # Add previous input/answer only if provided
    if previous_input and previous_output:
        prompt_parts.extend([
            f"Previous Input: '{previous_input}'",
            f"Previous Answer: '{previous_output}'"
        ])
    
    prompt_parts.extend([
        f"Response Style: {style}",
        f"Answer Length: Short",
        f"I'm saying: '{user_input}'"
    ])
    
    return " ".join(prompt_parts)

async def chat_with_gpt(user_name, user_input, bot_name, style, category, previous_input=None, previous_output=None):
    # Set up the bot
    payload_content = get_ai_profile_payload(bot_name, style)
    payload_bot = {"role": "system", "content": payload_content}
    #{"role": "system", "content": "You are Max, a gaming enthusiast and a close friend, giving insightful opinions in \"{style}\" style. "}

    # Append user message with profile information
    profile_info = get_user_profile_payload(user_name)
    print_console(f"User profile: {profile_info}")
    print_console(f"[DEBUG] style={style}")

    improved_input = get_improved_input(user_input, style, category, profile_info, previous_input, previous_output)
    payload_user = {"role": "user", "content": improved_input}

    print_console("Calling gpt API with:")
    print_console(f"Bot payload: {payload_bot}")
    print_console(f"User payload: {payload_user}")

    # Call OpenAI API, use fallback in case exceeding the free tier rate
    try:
        response = completions_with_fallback(
            fallback_model="gpt-3.5-turbo",
            payload_bot=payload_bot,
            payload_user=payload_user
        )
        #response = client.chat.completions.create(
        #    model="gpt-4o-mini",
        #    store=True,
        #    messages=[payload_bot, payload_user]
        #)
    except Exception as e:
        # Overriding throwing an exception from the call and giving default response
        print_console(f"API call failed: {e}")
        response = default_response

    ai_response = response.choices[0].message.content
    print_console(f"Response: {ai_response}")   
    # Error handling: check if the response is less than 4 characters
    if len(ai_response) < 4:
        ai_response = "I'm sleeping. Or pretending."

    deEmojified = deEmojify(ai_response)
    return deEmojified.encode("ascii", errors="ignore").decode()  # Return the response text instead of printing it

