from datetime import datetime, time
import requests
import schedule
import time

LINE_ACCESS_TOKEN = "C3tihcrrXb5mURTniOUvMmhEEEDJNfBpeAx/1dm7YMoZLO4Lb/99sdMyrwDCnkZl0f8vajQYe8WK0qvp83xzdaSrEoFn6U8gfFVFGSONzqbI3UYtbFP0M5TxAdHCP3nulNWONIf6DmuW79uRBoYpRgdB04t89/1O/w1cDnyilFU="
LINE_API_URL = "https://api.line.me/v2/bot/message/push"


headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + LINE_ACCESS_TOKEN,
}

payload = {
    "to": "U5a1b59669e2b66147f131937624b2d3c",
    "messages":[
        {
            "type":"text",
            "text":"Hello, world1"
        },
        {
            "type":"text",
            "text":"Hello, world2"
        }
    ]
}

def send_message():
    response = requests.post(LINE_API_URL, headers=headers, json=payload)
    print("Message sent. Response Status Code:", response.status_code)

def schedule_messages():
    schedule.every().day.at("14:47").do(send_message)

schedule_messages()

try:
    while True:
        schedule.run_pending()
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopping the scheduler.")