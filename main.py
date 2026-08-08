import requests
import time
import os
from threading import Thread
from flask import Flask

app = Flask('')
@app.route('/')
def home():
    return "Bot is alive!"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

Thread(target=run_flask).start()

SESSION_ID = os.environ.get("TIKTOK_SESSION_ID")
HEADERS = {
    "Cookie": f"sessionid={SESSION_ID}",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def check_and_reply():
    try:
        # 1. סריקת תיבת ההודעות הרגילה
        response = requests.get("https://tiktok.com", headers=HEADERS).json()
        my_uid = response.get("my_uid")
        
        for chat in response.get("chat_list", []):
            chat_id = chat.get("chat_id")
            latest_message = chat.get("latest_message", {})
            
            if not latest_message:
                send_help(chat_id)
                continue
            
            if latest_message.get("sender_uid") != my_uid:
                send_help(chat_id)
                
        # 2. סריקת תיבת הבקשות (Requests) למי שלא חבר שלך
        req_response = requests.get("https://tiktok.com", headers=HEADERS).json()
        for req_chat in req_response.get("chat_list", []):
            chat_id = req_chat.get("chat_id")
            
            # הבוט מאשר את הבקשה אוטומטית כדי להעביר אותה לצ'אט הרגיל
            requests.post("https://tiktok.com", headers=HEADERS, json={"chat_id": chat_id})
            # שולח את הודעת המצוקה
            send_help(chat_id)
                
    except Exception as e:
        print("Error:", e)

def send_help(chat_id):
    try:
        data = {"chat_id": chat_id, "text": "HELP", "type": 1}
        requests.post("https://tiktok.com", headers=HEADERS, json=data)
        print(f"Sent HELP to chat: {chat_id}")
        time.sleep(1) 
    except Exception as e:
        print("Failed to send message:", e)

while True:
    check_and_reply()
    time.sleep(4)
