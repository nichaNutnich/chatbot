from flask_sqlalchemy import SQLAlchemy

# สร้างตัวแปร db ที่ใช้สำหรับเชื่อมต่อกับฐานข้อมูล
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # ตั้งค่าให้ id เป็นคีย์หลักและ auto-generated
    customer_id = db.Column(db.String, index=True, unique=False, nullable=True)  
    customer_date = db.Column(db.Date, nullable=True)
    customer_time = db.Column(db.Integer, nullable=True)
    customer_court = db.Column(db.Integer, nullable=True)
    customer_name = db.Column(db.String(100), nullable=True)
    customer_number = db.Column(db.String(100), nullable=True)


class Court(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=True, unique=True)

class Time(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time_range = db.Column(db.String(20), nullable=True, unique=True)
    
# app = create_app()
# def create_table():
#     with app.app_context():
#       db.create_all()



# create_table()

# def add_initial_data():
#     courts = ['A01', 'A02', 'A03', 'A04', 'A05', 'A06', 'A07', 'A08', 'A09', 'A10']
#     times = ['17.00-18.00', '18.00-19.00', '19.00-20.00', '20.00-21.00', '21.00-22.00']

#     for court_name in courts:
#         court = Court(name=court_name)
#         db.session.add(court)

#     for time_range in times:
#         time = Time(time_range=time_range)
#         db.session.add(time)

#     db.session.commit()

# if __name__ == '__main__':
#     add_initial_data()

