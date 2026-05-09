import socket
import json
import time
from crypto_utils import *
from config import *

CLIENT_KEY_A = input("Enter Key for A from KDC: ").encode()

def request_session():
    sock = socket.socket()
    sock.connect((KDC_HOST, KDC_PORT))

    request = {
        "client_id": "A",
        "target_id": "B",
        "timestamp": generate_timestamp()
    }

    start = time.time()

    sock.send(json.dumps(request).encode())
    response = json.loads(sock.recv(4096).decode())

    end = time.time()
    print("[PERFORMANCE] Session key request time:", round(end - start, 6), "seconds")

    sock.close()
    return response

def communicate_with_B(ticket, session_key):
    sock = socket.socket()
    sock.connect(("127.0.0.1", CLIENT_B_PORT))

    message = encrypt(session_key, {
        "msg": "Hello from A",
        "timestamp": generate_timestamp()
    })

    start = time.time()

    sock.send(json.dumps({
        "ticket": ticket,
        "message": message.decode()
    }).encode())

    response = sock.recv(4096)

    end = time.time()
    print("[PERFORMANCE] Communication time:", round(end - start, 6), "seconds")

    # Decrypt Response
    decrypted_response = decrypt(session_key, response)
    print("[A] Decrypted Response:", decrypted_response["msg"])

    sock.close()

def main():
    total_start = time.time()

    response = request_session()

    encrypted_data = response["encrypted_data"].encode()
    ticket = response["ticket"]

    decrypted = decrypt(CLIENT_KEY_A, encrypted_data)
    session_key = decrypted["session_key"].encode()

    print("[A] Session Key Received")

    communicate_with_B(ticket, session_key)

    total_end = time.time()
    print("[PERFORMANCE] Total execution time:", round(total_end - total_start, 6), "seconds")

if __name__ == "__main__":
    main()