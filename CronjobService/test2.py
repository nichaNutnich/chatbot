from redis import Redis

# ตั้งค่า Redis
redis_conn = Redis()

# ตรวจสอบการเชื่อมต่อกับ Redis
try:
    redis_conn.ping()
    print("เชื่อมต่อกับ Redis ได้สำเร็จ")
except redis.ConnectionError:
    print("ไม่สามารถเชื่อมต่อกับ Redis ได้")
