from datetime import datetime, timedelta
import requests
import schedule
import time
# from models import User, Court 

LINE_ACCESS_TOKEN = "C3tihcrrXb5mURTniOUvMmhEEEDJNfBpeAx/1dm7YMoZLO4Lb/99sdMyrwDCnkZl0f8vajQYe8WK0qvp83xzdaSrEoFn6U8gfFVFGSONzqbI3UYtbFP0M5TxAdHCP3nulNWONIf6DmuW79uRBoYpRgdB04t89/1O/w1cDnyilFU="
LINE_API_URL = "https://api.line.me/v2/bot/message/broadcast"

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + LINE_ACCESS_TOKEN,
}

def send_message(customer_name, customer_court, customer_time):

    payload = {
        "messages": [
            {
                "type": "text",
                "text": f"คุณ {customer_name} วันนี้มีการจองคอร์ทแบดมินตัน {customer_court} ในช่วงเวลา {customer_time}"
            }
        ]
    }
    response = requests.post(LINE_API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        # print(f"คุณ {user_name} วันนี้มีการจองคอร์ทแบดมินตัน {court_name} ในช่วงเวลา {time_range}")
        return "Message sent successfully."
    else:
        return f"Failed to send message. Response Status Code: {response.status_code}"
# try:
#     while True:
#         schedule.run_pending()
#         # print(datetime.now())
            
#         time.sleep(1)
# except KeyboardInterrupt:
#     print("Stopping the scheduler.")

# def send_message(customer_name, customer_court, customer_time):
#     payload = {
#         "messages": [
#             {
#                 "type": "text",
#                 "text": f"คุณ {customer_name} วันนี้มีการจองคอร์ทแบดมินตัน {customer_court} ในช่วงเวลา {customer_time}"
#             }
#         ]
#     }
#     response = requests.post(LINE_API_URL, headers=headers, json=payload)
#     print("Message sent. Response Status Code:", response.status_code)

# def schedule_messages():
#     schedule.every().day.at("14:55").do(send_message)

# schedule_messages()



# def schedule_notifications():
#     # with app.app_context():  # ตั้งค่า context ของแอปพลิเคชัน
#         today = datetime.now().date()
#         bookings = User.query.filter_by(customer_date=today).all() 
#         notifications = []  
#         for booking in bookings:
#             booking_time = datetime.strptime(booking.customer_date + ' ' + booking.time_range.split('-')[0], '%Y-%m-%d %H:%M')
#             notification_time = booking_time - timedelta(hours=1)
#             if notification_time > datetime.now():
#                 user_name = booking.customer_name
#                 court_name = Court.query.filter_by(id=booking.customer_court).first().name
#                 schedule_time = notification_time.strftime('%Y-%m-%d %H:%M:%S')
#                 # schedule.every().day.at(notification_time.strftime('%H:%M:%S')).do(send_message, user_name, court_name, booking.time_range)
#                 notification_info = f"ตั้งเวลาแจ้งเตือนที่ {schedule_time} สำหรับการจองของคุณ {user_name} คอร์ท {court_name} ช่วงเวลา {booking.time_range}"
#                 notifications.append(notification_info)
#         return notifications
# notification_info = schedule_notifications()
# try:
    
#     while True:
#         schedule.run_pending()
#         print(datetime.now())
#         time.sleep(1)
# except KeyboardInterrupt:
#     print("Stopping the scheduler.")


