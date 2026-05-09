import socket
import json
import time
from crypto_utils import *
from config import *

CLIENT_KEY_B = input("Enter Key for B from KDC: ").encode()

def start_server():
    server = socket.socket()
    server.bind(("127.0.0.1", CLIENT_B_PORT))
    server.listen(5)

    print("[B] Waiting for connections...")

    while True:
        client_socket, addr = server.accept()

        start = time.time()

        data = json.loads(client_socket.recv(4096).decode())

        ticket = data["ticket"].encode()
        message = data["message"].encode()

        # Decrypting ticket
        ticket_data = decrypt(CLIENT_KEY_B, ticket)
        session_key = ticket_data["session_key"].encode()

        if not is_valid_timestamp(ticket_data["timestamp"]):
            print("[B] Replay attack detected")
            return

        # Decrypting message
        decrypted_msg = decrypt(session_key, message)
        print("[B] Message from A:", decrypted_msg["msg"])

        # Sending response
        response = encrypt(session_key, {
            "msg": "Hello A, secure channel established",
            "timestamp": generate_timestamp()
        })

        client_socket.send(response)

        end = time.time()
        print("[PERFORMANCE B] Processing time:", round(end - start, 6), "seconds")

        client_socket.close()

if __name__ == "__main__":
    start_server()