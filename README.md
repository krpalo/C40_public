# Introly powered by C-For-T (Contender-for-Tinder) — AI Wingman App (frontend, backend)

This project aims to help people connect in a more meaningful way by using an AI "wingman" to suggest matches, socialize, or assist in real-world meetups.
Built with a **React + TypeScript frontend** and **FastAPI backend**.

---

## Getting Started (Full Setup)

### Requirements

- Python 3.8+ (using 3.1.13 initially)
- Node.js + npm (install from https://nodejs.org)
- Git (recommended)

---

## Backend (FastAPI)
1. Navigate to the server folder
cd server
2. Create and activate a virtual environment
python -m venv venv 
### activate it by running the script in venv\Scripts\activate
3. Install dependencies
pip install fastapi uvicorn pydantic
4. Start the backend server
uvicorn main:app --reload
### Now the API is running at: http://localhost:8000
### cleanup assets

## Frontend (React + Vite + TypeScript)
1. Navigate to root folder and create app
npm create vite@latest client -- --template react-ts
### setup React + Typescript
cd client
npm install
npm run dev
### Your app will open at: http://localhost:5173

In case of errors in running powershell (Execution policy) - magic spell:
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned