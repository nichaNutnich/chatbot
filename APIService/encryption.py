from cryptography.fernet import Fernet

# def generate_key():
#     """สร้างและคืนค่าคีย์ใหม่"""
#     return Fernet.generate_key()

# key = Fernet.generate_key()
# cipher_suite = Fernet(key)
def encrypt_data(data, key):
    cipher_suite = Fernet(key)
    encrypted_data = cipher_suite.encrypt(data.encode()).decode()
    return encrypted_data

def decrypt_data(encrypted_data, key):
    cipher_suite = Fernet(key)
    decrypted_data = cipher_suite.decrypt(encrypted_data.encode()).decode()
    return decrypted_data

# key = Fernet.generate_key()