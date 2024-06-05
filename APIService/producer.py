import json
import pika
from models import db, User, Time
from flask import Flask


def send_to_rabbitmq(customer_id, customer_date, customer_time, customer_court, customer_name, customer_number):
    # ตั้งค่าการเชื่อมต่อกับ RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # สร้าง Exchange ชื่อ 'user_created_exchange' แบบ direct
    channel.exchange_declare(exchange='user_created_exchange', exchange_type='direct')

    #สร้างข้อความที่จะส่งไปยัง RabbitMQ โดยแปลงข้อมูลเป็นรูปแบบ JSON string
    message = {
        'customer_id': customer_id,
        'customer_date': str(customer_date),
        'customer_time': customer_time,
        'customer_court': customer_court,
        'customer_name': customer_name,
        'customer_number': customer_number
        # 'time_id': time_id
    }
    # ตรวจสอบและแปลงข้อมูลประเภท bytes เป็น string (ถ้ามี)
    for key, value in message.items():
        if isinstance(value, bytes):
            message[key] = value.decode('utf-8')
    message_str = json.dumps(message)  # แปลง dictionary เป็น JSON string
    # message_str = "234234234"


    # ส่งข้อความไปยัง Exchange
    channel.basic_publish(exchange='my_exchange', routing_key='my_routing_key', body=message_str)
    print(f" [x] Sent '{message_str}'")

    # ปิดการเชื่อมต่อ
    connection.close()

    # Return ข้อความเป็น text
    return f"Sent message to RabbitMQ: {message_str}"

# ฟังก์ชันสำหรับ query ข้อมูลการจองทั้งหมดจากฐานข้อมูล
def query_all_user_data():
    users = db.session.query(User).all()  # ดึงข้อมูลการจองทั้งหมดจากฐานข้อมูล
    user_data_list = []
    for user in users:
        time_entry = db.session.query(Time).filter(Time.time_range.contains(user.customer_time)).first()
        if not time_entry:
            print(f"No time entry found for time range containing: {user.customer_time}")
            continue
        user_data_list.append({
            'customer_id': user.customer_id,
            'customer_date': str(user.customer_date),  # แปลงวันที่เป็น string เพื่อให้ JSON serializable
            'customer_time': user.customer_time,
            'customer_court': user.customer_court,
            'customer_name': user.customer_name,
            'customer_number': user.customer_number
            # 'time_id': time_entry.id  # เพิ่ม time_id ในข้อมูลที่จะส่ง
        })
    return user_data_list

if __name__ == "__main__":
    from app import app  # นำเข้าแอปเพื่อใช้ app context

    with app.app_context():
        user_data_list = query_all_user_data()
        if user_data_list:
            for user_data in user_data_list:
                response = send_to_rabbitmq(**user_data)
                print(response)
        else:
            print("ไม่พบข้อมูลการจองในฐานข้อมูล")
# user_data_list = query_all_user_data()
# if user_data_list:
#     for user_data in user_data_list:
#         response = send_to_rabbitmq(**user_data)
#         print(response)
# else:
#     print("ไม่พบข้อมูลการจองในฐานข้อมูล")
