import requests
import time
import os

SESSION_ID = os.environ.get("TIKTOK_SESSION_ID")
HEADERS = {
    "Cookie": f"sessionid={SESSION_ID}",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def check_and_reply():
    try:
        response = requests.get("https://tiktok.com", headers=HEADERS).json()
        my_uid = response.get("my_uid")
        
        for chat in response.get("chat_list", []):
            chat_id = chat.get("chat_id")
            latest_message = chat.get("latest_message", {})
            
            # אם הצ'אט חדש לגמרי וריק
            if not latest_message:
                send_run(chat_id)
                continue
            
            # אם מישהו אחר שלח את ההודעה האחרונה
            sender_uid = latest_message.get("sender_uid")
            if sender_uid != my_uid:
                send_run(chat_id)
                
    except Exception as e:
        print("Error:", e)

def send_run(chat_id):
    try:
        data = {"chat_id": chat_id, "text": "RUN", "type": 1}
        requests.post("https://tiktok.com", headers=HEADERS, json=data)
        print(f"Sent RUN to chat: {chat_id}")
        time.sleep(1) 
    except Exception as e:
        print("Failed to send message:", e)

while True:
    check_and_reply()
    time.sleep(4)
