from models import User, db  # นำเข้าโมดูล User และ db จากไฟล์ models.py
from datetime import datetime
# from flask_apscheduler import APScheduler
# import time

# def print_numbers(stop_at):
#     num = 1
#     while num <= stop_at:  # เพิ่มเงื่อนไขการหยุด
#         print(num)
#         num += 1
#         time.sleep(1)

# # เรียกใช้ฟังก์ชัน
# print_numbers(10)  # พิมพ์ตัวเลขจนถึง 10

def reset_bookings():
    current_date = datetime.now().date()
    # เปลี่ยนเงื่อนไขการค้นหาเป็นวันที่น้อยกว่าวันปัจจุบัน
    bookings_to_reset = User.query.filter(User.customer_date < current_date).all()
    for booking in bookings_to_reset:
        db.session.delete(booking)
    db.session.commit()

if __name__ == "__main__":
    reset_bookings()
    # schedule_notification()
