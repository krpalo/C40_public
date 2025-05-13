import pytest
from botprofile import get_ai_profile_payload
from textprettify import deEmojify

# botprofile tests
def test_default_style():
    result = get_ai_profile_payload("Max")
    assert "Your name is Max" in result
    assert '"Neutral" style' in result

def test_custom_style():
    result = get_ai_profile_payload("Luna", "Charming")
    assert "Your name is Luna" in result
    assert '"Charming" style' in result


def test_deEmojify_short_example():
    input_text = (
        "Hey MsFire! I can’t check that directly, but generally, the OpenAI API's free tier has some limits 🚫. "
        "If you’re diving into that, it could be like strategizing for a game🔥definitely worth looking into!"
    )

    expected_output = (
        "Hey MsFire! I can’t check that directly, but generally, the OpenAI API's free tier has some limits. "
        "If you’re diving into that, it could be like strategizing for a game. Definitely worth looking into!"
    )

    assert deEmojify(input_text) == expected_output
