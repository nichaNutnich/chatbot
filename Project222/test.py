from concurrent.futures import ThreadPoolExecutor
import time

def task(number):
    print(f"Processing task {number}...")
    time.sleep(2)  # สร้างการหน่วงเวลา 2 วินาที
    print(f"Task {number} completed.")

if __name__ == "__main__":
    # สร้าง ThreadPoolExecutor กับจำนวนเธรดตามที่ต้องการ
    executor = ThreadPoolExecutor(max_workers=5)

    # สร้างงานที่จะส่งให้ ThreadPoolExecutor ประมวลผล
    tasks = [executor.submit(task, i) for i in range(10)]

    # รอให้งานทั้งหมดเสร็จสมบูรณ์
    for future in tasks:
        future.result()

    # หลังจากที่งานทั้งหมดเสร็จสมบูรณ์แล้ว
    print("All tasks completed.")
