from concurrent.futures import ThreadPoolExecutor
from flask import Flask, request, jsonify
from models import db, User, Court, Time
from config import Config
from datetime import datetime
import pika
from encryption import encrypt_data, decrypt_data
from cryptography.fernet import Fernet
from reset import reset_bookings
from producer import send_to_rabbitmq
# from notify import schedule_notification
# from flask_bcrypt import Bcrypt, check_password_hash

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
# bcrypt = Bcrypt(app)

key = Fernet.generate_key()

executor = ThreadPoolExecutor(max_workers=10)

# สร้าง context เพื่อสร้างตารางและข้อมูลเบื้องต้น
with app.app_context():
    db.create_all()

    # เพิ่มข้อมูลสนามถ้ายังไม่มี
    if not Court.query.first():
        courts = ['A01', 'A02', 'A03', 'A04', 'A05', 'A06', 'A07', 'A08', 'A09', 'A10']
        for court_name in courts:
            new_court = Court(name=court_name)
            db.session.add(new_court)
        db.session.commit()

    # เพิ่มข้อมูลเวลาถ้ายังไม่มี
    if not Time.query.first():
        times = ['17.00-18.00', '18.00-19.00', '19.00-20.00', '20.00-21.00', '21.00-22.00']
        for time_range in times:
            new_time = Time(time_range=time_range)
            db.session.add(new_time)
        db.session.commit()


@app.route('/users', methods=['POST'])
def process_add_user():
    future = executor.submit(add_user)
    result = future.result()
    return result

def add_user():
    # print("Thread started for add_user")
    customer_id = request.args.get('customer_id')
    customer_date = request.args.get('customer_date')
    customer_time_id = request.args.get('customer_time')
    customer_court = request.args.get('customer_court')
    customer_name = request.args.get('customer_name')
    customer_number = request.args.get('customer_number')
    if not all([customer_id, customer_date, customer_time_id, customer_court, customer_name, customer_number]):
        return jsonify({'error': 'Missing required parameters'}), 400

    try:
        customer_date = datetime.strptime(customer_date, '%Y-%m-%d').date()
        customer_time_id = int(customer_time_id)
        customer_court = int(customer_court)
        # ตรวจสอบว่า customer_number เป็น string หรือ unicode
        if not isinstance(customer_number, str):
           raise ValueError("Customer number must be a string")

    except ValueError as e:
        return jsonify({'error': str(e)}), 402

    if customer_date < datetime.now().date():
        return 'ทำการจองไม่สำเร็จ : กรุณาพิมพ์ "เริ่มทำการจอง" เพื่อเริ่มทำการจองใหม่'

    existing_booking = User.query.filter_by(customer_date=customer_date, customer_time=customer_time_id, customer_court=customer_court).first()
    if existing_booking:
      return jsonify({'error': 'Court is already booked for the given date and time'}), 200


    encrypted_customer_number = encrypt_data(str(customer_number), key)  # แปลง customer_number เป็น string ก่อนเข้ารหัส
    print(customer_id, customer_date, customer_time_id, customer_court, customer_name, customer_number)
    send_to_rabbitmq(customer_id, customer_date, customer_time_id, customer_court, customer_name, customer_number)
    
    new_user = User(
        customer_id=customer_id,
        customer_date=customer_date,
        customer_time=customer_time_id,
        customer_court=customer_court,
        customer_name=customer_name,
        customer_number=encrypted_customer_number
    )

    try:
        db.session.add(new_user)
        db.session.commit()

        # ดึง time_range จากฐานข้อมูล
        time_range = Time.query.get(customer_time_id).time_range

        # ถอดรหัส customer_number ก่อนส่งข้อความคืนให้ผู้ใช้
        decrypted_customer_number = decrypt_data(encrypted_customer_number, key)

        return (
            f"ทำการจองสำเร็จแล้ว:\n"
            f"  Date: {str(customer_date)}\n"
            f"  Time: {time_range}\n"
            f"  Court: {customer_court}\n"
            f"  Name: {customer_name}\n"
            f"  Customer Number: {decrypted_customer_number}"
        ), 201
        
    except Exception as e:
        db.session.rollback()
        return f'Error: {str(e)}', 500

@app.route('/users', methods=['GET'])
def prprocess_get_users():
    future = executor.submit(get_users)
    result = future.result()
    return result

def get_users():
    users = User.query.all()
    user_list = []
    for user in users:
        try:
            decrypted_customer_number = decrypt_data(user.customer_number, key)
        except Exception as e:
            return f'Error: {str(e)}', 500

        user_info = {
            'customer_id': user.customer_id,  
            'customer_date': str(user.customer_date),
            'customer_time': user.customer_time,
            'customer_court': user.customer_court,
            'customer_name': user.customer_name,
            'customer_number': decrypted_customer_number
        }
        user_list.append(user_info)

    return jsonify(user_list), 200

@app.route('/datetime', methods=['GET'])
def process_datetime():
    future = executor.submit(separate_and_store_datetime)
    result = future.result()
    return result

def separate_and_store_datetime():
    customer_date = request.args.get('customer_date')

    if not all([customer_date]):
        return jsonify({'error': 'ขาดพารามิเตอร์ที่จำเป็น'}), 401

    try:
        # แปลงวันที่และเวลา
        customer_date = datetime.strptime(customer_date, '%Y-%m-%d').date()
    except ValueError as e:
        return jsonify({'error': str(e)}), 402

    if customer_date < datetime.now().date():
        return '{{DL_การจอง1}}'


    try:
        db.session.commit()

        # ดึง time_range จากฐานข้อมูล
        # time_range = Time.query.get(customer_time_id).time_range
        return '{{DL_การจอง2}}'
        # return (
        #     f"  Date: {str(customer_date)}\n"

        #     # f"  Time: {time_range}\n"
        # ), 201
    except Exception as e:
        db.session.rollback()
        return f'Error: {str(e)}', 500

@app.route('/check_date', methods=['POST'])
def process_check_date():
    future = executor.submit(check_date)
    result = future.result()
    return result

def check_date():
    customer_date = request.args.get('customer_date')
    customer_date = datetime.strptime(customer_date, '%Y-%m-%d').date()
    if customer_date < datetime.now().date():
        return 'ไม่สามารถทำการจองได้'
    return 'Date is valid'


@app.route('/check', methods=['GET'])
def process_check_user():
    future = executor.submit(check_user)
    result = future.result()
    return result

def check_user():
    customer_date = request.args.get('customer_date')
    customer_time = request.args.get('customer_time')

    if not customer_date or not customer_time:
        return jsonify({'error': 'Missing parameters'}), 400

    try:
        customer_date = datetime.strptime(customer_date, '%Y-%m-%d').date()
        customer_time = int(customer_time)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

    existing_booking = User.query.filter_by(customer_date=customer_date, customer_time=customer_time).all()
    booked_courts = {booking.customer_court for booking in existing_booking}

    all_courts = Court.query.all()
    available_courts = [court for court in all_courts if court.id not in booked_courts]

    if not available_courts:
        return 'All courts are booked'

    available_courts_list = [court.name for court in available_courts]
    response_string = "Available courts:\n" + "\n".join([f"{court.id}. {court.name}" for court in available_courts])

    return response_string, 200


@app.route('/show', methods=['GET'])
def process_show_users():
    future = executor.submit(show_users)
    result = future.result()
    return result

def show_users():
    customer_name = request.args.get('customer_name')
    if not customer_name: 
        return 'Missing customer_name parameter', 400

    bookings = User.query.filter_by(customer_name=customer_name).all()
    if not bookings:
        return 'User not found', 404

    bookings_dict = {}
    for index, booking in enumerate(bookings, start=1):
        time = Time.query.filter_by(id=booking.customer_time).first()
        time_range = time.time_range if time else 'Unknown'

        bookings_dict[index] = {
            'Date': str(booking.customer_date),
            'Time': time_range,
            'Court': booking.customer_court,
            'Name': booking.customer_name,
            'Phone Number': booking.customer_number
        }

    formatted_text = "การจองทั้งหมด:\n"
    for index, booking in bookings_dict.items():
        formatted_text += (
            f"Booking {index}:\n"
            f"  Date: {booking['Date']}\n"
            f"  Time: {booking['Time']}\n"
            f"  Court: {booking['Court']}\n"
            f"  Name: {booking['Name']}\n"
            # f"  Phone Number: {booking['Phone Number']}\n"
            "\n"
        )

    return formatted_text


if __name__ == "__main__":
    with app.app_context():
        reset_bookings()
        # from notify import schedule_notification
        # schedule_notification()
    app.run()
