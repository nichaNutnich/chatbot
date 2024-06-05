import pika
import json
# import schedule
from notify import send_message
from datetime import datetime, timedelta
from redis import Redis
from rq_scheduler import Scheduler
# from rq import Queue
import pytz

# ตั้งค่า Redis และ RQ-Scheduler
redis_conn = Redis()
scheduler = Scheduler(connection=redis_conn)
# queue = Queue(connection=redis_conn)

def callback(ch, method, properties, body):
    data = json.loads(body.decode())
    print(" [x] Received", data)
    print(data["customer_date"])
    message2 = add_job(data)
    if message2:
        print(message2)

def add_job(data):
    customer_date = data["customer_date"]
    # customer_time = data["customer_time"]
    customer_time = str(data["customer_time"])
    customer_court = data["customer_court"]
    customer_name = data["customer_name"]
    # print("test1:",customer_date)
    # datetime_format = "%Y-%m-%d %H:%M"
    # date_obj = datetime.datetime.strptime(customer_date, datetime_format)
    # try:
    #     time_id = data["time_id"]
    #     time_id_dt = datetime.fromtimestamp(time_id)
    # except KeyError:
    #     print("Missing key 'time_id' in the data. Skipping job.")
    #     return None
    
    try:
        date_obj = datetime.strptime(customer_date, "%Y-%m-%d").date()
    except ValueError as e:
        print(f"Invalid date format: {e}")
        return None
    # print("test1:",type(date_obj))
    # print("test1:",type(str(datetime.now().date())))
    # print("test2:",customer_time)
    # print("test3:",customer_court)
    # print("test4:",customer_name)
    
    if date_obj == datetime.now().date():
        if customer_time.isdigit() and len(customer_time) <= 2:
            customer_time = customer_time.zfill(2) + ":00"
        elif len(customer_time.split(':')) == 2:
            hours, minutes = customer_time.split(':')
            customer_time = hours.zfill(2) + ":" + minutes.zfill(2)
        else:
            print("Invalid time format")
            return None

        # Calculate the notification time, 1 hour before the booking time
        notification_time_str = f"{customer_date} {customer_time}"
        notification_time = datetime.strptime(notification_time_str, "%Y-%m-%d %H:%M")
        notification_time -= timedelta(hours=1)
        
        # Convert notification time to UTC
        notification_time = notification_time.astimezone(pytz.UTC)
        
        # Check if it's time to send the notification
        print(notification_time)
        # print(datetime.now(pytz.UTC))
        if notification_time > datetime.now(pytz.UTC):
            # Add the job to the scheduler
            scheduler.enqueue_at(notification_time, send_message, customer_name, customer_court, customer_time)
            message = f"คุณ {customer_name} วันนี้มีการจองคอร์ทแบดมินตัน {customer_court} ในช่วงเวลา {customer_time}"
            print(message)
            # # แปลง datetime กลับเป็น string
            # date_string = date_obj.strftime("%Y-%m-%d")
            # print("Customer Date as String:", date_string)

            return message
        else:
            print("Time does not match. Skipping job.")
            return None
    else:
        print("Not for today.")
        return None



    
# ตั้งค่าการเชื่อมต่อกับ RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# ตรวจสอบว่า exchange 'my_exchange' มีอยู่หรือไม่ ถ้าไม่มีให้สร้าง exchange
channel.exchange_declare(exchange='my_exchange', exchange_type='direct')

# สร้าง queue ชื่อ 'my_queue'
channel.queue_declare(queue='my_queue')

# เชื่อมต่อ queue กับ exchange โดยใช้ routing_key 'my_routing_key'
channel.queue_bind(exchange='my_exchange', queue='my_queue', routing_key='my_routing_key')

# กำหนด callback ให้กับ queue
channel.basic_consume(queue='my_queue', on_message_callback=callback, auto_ack=True)

# แจ้งเตือนเมื่อรอรับข้อความ
print(' [*] Waiting for messages. To exit press CTRL+C')

# เริ่มรับข้อความแบบ Asynchronous
channel.start_consuming()
