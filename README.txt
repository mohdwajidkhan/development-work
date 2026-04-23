Secure Client Communication using KDC (Key Distribution Center)

Overview
This project implements a secure communication system using a Key Distribution Center (KDC) model. It simulates how two clients (Client A and Client B) securely exchange messages using session keys generated and distributed by a trusted server.

Features
- Confidential communication
- Protection against replay attacks
- Secure key exchange using encryption

Project Components

1. KDC Server (kdc_server.py)
- Generates secret keys for clients A and B
- Issues session keys upon request
- Creates encrypted tickets

2. Client A (client_a.py)
- Requests session key from KDC
- Decrypts session key
- Sends encrypted message to Client B

3. Client B (client_b.py)
- Receives ticket and message
- Validates timestamp
- Decrypts message and replies securely

4. Cryptographic Utilities (crypto_utils.py)
- Key generation
- Encryption & decryption using Fernet
- Timestamp validation

5. Configuration (config.py)
- Server host and ports
- Client ports
- Session timeout

How It Works

1. KDC generates keys for Client A and B
2. Client A requests session key
3. KDC sends encrypted session key and ticket
4. Client A communicates securely with Client B
5. Client B decrypts and responds

Security Features
- Symmetric encryption (Fernet)
- Timestamp-based replay protection
- Session key mechanism
- Encrypted ticket system

Requirements
- Python 3.x
- cryptography library

Install dependency:
pip install cryptography

How to Run

1. Start KDC Server:
python kdc_server.py

2. Start Client B:
python client_b.py
Enter key for B

3. Start Client A:
python client_a.py
Enter key for A

Performance Metrics
- Session key request time
- Communication time
- Total execution time

Limitations
- Works on localhost only
- No persistent session storage
- Basic error handling

Future Improvements
- GUI dashboard
- Multi-client support
- Use RSA encryption
- Add authentication system

Concepts Used
- Key Distribution Center (KDC)
- Symmetric Encryption
- Secure Session Communication
- Socket Programming

Author
This project demonstrates secure communication using Python and cryptography.
