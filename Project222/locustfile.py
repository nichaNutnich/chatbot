import json
from locust import HttpUser, TaskSet, task, between

# class COurt(HttpUser):
#     wait_time = between(1, 2)  # Wait between 1 to 2 seconds between tasks

#     @task
#     def add_user(self):
#         payload = {
#             'customer_id': 'testcustomer_id',
#             'customer_date': '2024-06-15',
#             'customer_time': '1',  # Assuming '1' corresponds to a valid time ID
#             'customer_court': '1',  # Assuming '1' corresponds to a valid court ID
#             'customer_name': 'Test User',
#             'customer_number': '0123456789'
#         }
#         self.client.post('/users', params=payload)

# if __name__ == '__main__':
#     import os
#     os.system("locust -f locustfile.py")
class UserBehavior(TaskSet):
    @task(1)
    def add_user(self):
        payload = {
            'customer_id': '1',
            'customer_date': '2024-06-10',
            'customer_time': '1',
            'customer_court': '1',
            'customer_name': 'John Doe',
            'customer_number': '1234567890'
        }
        self.client.post("/users", params=payload)

    # @task(2)
    # def get_users(self):
    #     self.client.get("/users")

    @task(3)
    def check_user(self):
        self.client.get("/check", params={
            'customer_date': '2024-06-10',
            'customer_time': '1'
        })

    @task(4)
    def show_users(self):
        self.client.get("/show", params={'customer_name': 'John Doe'})

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 5)

if __name__ == '__main__':
    import os
    os.system("locust -f locustfile.py")