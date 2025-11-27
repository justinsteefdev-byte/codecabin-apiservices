from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ContactForm(BaseModel):
    name: str
    email: str
    subject: str
    message: str

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

@app.post("/contact")
async def send_contact_message(form: ContactForm):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        raise HTTPException(status_code=500, detail="Telegram configuration missing")

    text = f"""
New Contact Form Submission:
---------------------------
Name: {form.name}
Email: {form.email}
Subject: {form.subject}
Message: {form.message}
    """

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return {"status": "success", "message": "Message sent successfully"}
    except requests.exceptions.RequestException as e:
        print(f"Error sending Telegram message: {e}")
        raise HTTPException(status_code=500, detail="Failed to send message")

@app.get("/")
def read_root():
    return {"message": "Code Cabin API is running"}
