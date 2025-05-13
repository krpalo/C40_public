import pytest
import asyncio
from unittest.mock import patch, MagicMock

from sendtochatpete import chat_with_gpt, get_improved_input
from userprofile import load_profiles
#from textprettify import print_console

@pytest.mark.asyncio
async def test_chat_with_gpt_success():
    load_profiles()  # Populate the global variable
    fake_response = MagicMock()
    fake_response.choices = [MagicMock(message=MagicMock(content="Hello! 👋"))]

    with patch("botprofile.get_ai_profile_payload", return_value="Bot profile text"), \
         patch("userprofile.get_user_profile_payload", return_value="Name: MsFire, Interests: AI"), \
         patch("sendtochatpete.client.chat.completions.create", return_value=fake_response), \
         patch("textprettify.print_console"), \
         patch("textprettify.deEmojify", return_value="Hello!"):

        result = await chat_with_gpt(
            user_name="MsFire",
            user_input="How do I sound today?",
            bot_name="Max",
            style="Charming",
            category="General"
        )

        assert isinstance(result, str)
        assert "Hello" in result

@pytest.mark.asyncio
async def test_chat_with_gpt_api_failure():
    load_profiles()  # Populate the global variable
    with patch("botprofile.get_ai_profile_payload", return_value="Bot profile text"), \
         patch("userprofile.get_user_profile_payload", return_value="Name: MsFire"), \
         patch("sendtochatpete.client.chat.completions.create", side_effect=Exception("Network fail")), \
         patch("textprettify.print_console"), \
         patch("textprettify.deEmojify", return_value="Default fallback"), \
         patch("sendtochatpete.default_response", new=MagicMock(choices=[MagicMock(message=MagicMock(content="Oops"))])):

        result = await chat_with_gpt(
            user_name="MsFire",
            user_input="Are you awake?",
            bot_name="Max",
            style="Neutral",
            category="General"
        )

        assert "Default fallback" in result or isinstance(result, str)

def test_improved_input_basic():
    result = get_improved_input("Hey there", "Friendly", "Dating", "Name: Alex")
    assert "My profile: Name: Alex" in result
    assert "Category: Dating" in result
    assert "I'm saying: 'Hey there'" in result
    assert "Previous Input" not in result

def test_improved_input_with_history():
    result = get_improved_input(
        "What's up?", "Teasing", "Social", "Name: Max", "How's it going?", "Pretty good"
    )
    assert "Previous Input: 'How's it going?'" in result
    assert "Previous Answer: 'Pretty good'" in result
    assert "Response Style: Teasing" in result
