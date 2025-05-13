import json
import os
from typing import Dict
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel

from sendtochatpete import chat_with_gpt  # Internal
from userprofile import UserProfile, load_profiles, save_profiles_to_file  # Internal
from textprettify import print_console # Internal

# Load config
with open(os.path.join(os.path.dirname(__file__), "resources", "config.json")) as f:
    config = json.load(f)

# FastAPI app initialization
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use specific origin later for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

profiles: Dict[str, UserProfile] = load_profiles()

class ChatRequest(BaseModel):
    user_name: str = ""
    input_text: str = ""
    bot_name: str = "Max"
    style: str = "friendly"
    category: str = "general"
    previous_input: str = ""
    previous_output: str = ""

# Endpoint for chat command
@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        # Call the function to chat with GPT
        response = await chat_with_gpt(
            request.user_name,
            request.input_text,
            request.bot_name,
            request.style,
            request.category,
            request.previous_input,
            request.previous_output
        )
        return {"response": response}
    except HTTPException as http_exc:
        # Handle known exceptions with specific status codes
        if http_exc.status_code == 500:
            return JSONResponse(
                status_code=500,
                content={"response": "Oops! Sorry, you are disconnected from the world and I can't hear you."}
            )
        else:
            return JSONResponse(
                status_code=http_exc.status_code,
                content={"response": f"An error occurred: {http_exc.detail}"}
            )
    except Exception as e:
        # Any other unexpected error defaults to 500
        print_console(f"GPT call failed: {e}")
        return JSONResponse(
            status_code=500,
            content={"response": "Oops! We're sorry, you are disconnected from the world. "}
        )

# Endpoint for creating a profile command
@app.post("/profile")
async def save_profile(profile: UserProfile, overwrite: bool = Query(False)):
    print_console("Received profile:")
    print_console(f"Name: {profile.name}")
    print_console(f"Interests: {profile.interests}")
    key = profile.name.strip().lower()

    if key in profiles and not overwrite:
        raise HTTPException(
            status_code=409,
            detail=f"Profile for {profile.name} already exists. Please choose another user name."
        )

    profiles[key] = profile
    save_profiles_to_file()
    return {"message": f"Profile for {profile.name} {'updated' if key in profiles else 'saved'}"}

# Endpoint for getting the user profile
@app.get("/profile/{user_id}")
async def get_profile(user_id: str):
    return profiles.get(user_id.lower(), {"name": "", "interests": ""})

# Endpoint for getting all user profiles
@app.get("/profiles")
def get_all_profiles():
    return [p.model_dump() for p in profiles.values()]

# Endpoint for the root
@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <html>
        <head>
            <title>C-For-T API</title>
        </head>
        <body style="background-color: #121212; color: #f0f0f0; font-family: sans-serif; text-align: center; padding-top: 50px;">
            <h1>Hello! Welcome to the C-For-T API</h1>
            <p>Use the <a href="/docs" style="color: #90caf9;">/docs</a> endpoint to test the chat endpoint!</p>
        </body>
    </html>
    """