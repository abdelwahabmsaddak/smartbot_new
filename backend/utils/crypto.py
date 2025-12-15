from cryptography.fernet import Fernet
import os

FERNET_KEY = os.environ.get("FERNET_KEY")  # تحطها في Render ENV
fernet = Fernet(FERNET_KEY)

def encrypt(text: str) -> str:
    return fernet.encrypt(text.encode()).decode()

def decrypt(text: str) -> str:
    return fernet.decrypt(text.encode()).decode()
