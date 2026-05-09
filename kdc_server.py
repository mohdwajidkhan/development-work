import socket
import json
from crypto_utils import *
from config import *

# Generating keys for A and B
CLIENT_KEYS = {
    "A": generate_key(),
    "B": generate_key()
}

print("[KDC] Generated Keys:")
print("A:", CLIENT_KEYS["A"])
print("B:", CLIENT_KEYS["B"])

session_store = {}

def generate_session_key():
    return generate_key()

def create_ticket(client_id, session_key):
    ticket_data = {
        "session_key": session_key.decode(),
        "client_id": client_id,
        "timestamp": generate_timestamp()
    }
    return encrypt(CLIENT_KEYS["B"], ticket_data)

def handle_request(data):
    client_id = data["client_id"]
    target_id = data["target_id"]
    timestamp = data["timestamp"]

    if not is_valid_timestamp(timestamp):
        return {"error": "Replay attack detected"}

    session_key = generate_session_key()
    session_store[client_id] = session_key

    response_for_A = encrypt(CLIENT_KEYS["A"], {
        "session_key": session_key.decode(),
        "target": target_id,
        "timestamp": generate_timestamp()
    })

    ticket = create_ticket(client_id, session_key)

    return {
        "encrypted_data": response_for_A.decode(),
        "ticket": ticket.decode()
    }

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((KDC_HOST, KDC_PORT))
    server.listen(5)

    print("[KDC] Server running...")

    while True:
        client_socket, addr = server.accept()
        data = json.loads(client_socket.recv(4096).decode())

        response = handle_request(data)
        client_socket.send(json.dumps(response).encode())

        client_socket.close()

if __name__ == "__main__":
    start_server()
