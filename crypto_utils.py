from cryptography.fernet import Fernet
import time
import json

def generate_key():
    return Fernet.generate_key()

def encrypt(key, data):
    f = Fernet(key)
    return f.encrypt(json.dumps(data).encode())

def decrypt(key, token):
    f = Fernet(key)
    return json.loads(f.decrypt(token).decode())

def generate_timestamp():
    return int(time.time())

def is_valid_timestamp(ts, window=60):
    return abs(time.time() - ts) < window
