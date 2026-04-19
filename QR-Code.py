#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║            QR SECRET ENCODER / DECODER                       ║                                        
╚══════════════════════════════════════════════════════════════╝
"""

import sys
import qrcode
import base64
import os
import time
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# ================= HACKER STYLE FUNCTIONS =================
def hacker_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\033[92m" + """
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║                         QR SECRET ENCODER / DECODER                           ║
║                           HasnainDarkNet👑                                   ||
╚═══════════════════════════════════════════════════════════════════════════════╝
    """ + "\033[0m")
    print("\n\033[93m[!] Welcome to QR Secret Tool - Hacker Edition\033[0m\n")

def type_effect(text, delay=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def loading_effect():
    print("\033[92m[*] Processing", end="")
    for i in range(3):
        time.sleep(0.5)
        print(".", end="", flush=True)
    print(" Done!\033[0m\n")

# ================= ENCRYPTION FUNCTIONS =================
def derive_key(password: bytes, salt: bytes, iterations: int = 200000) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
    )
    return kdf.derive(password)

def encrypt_message(message: bytes, password: str) -> str:
    salt = os.urandom(16)
    key = derive_key(password.encode('utf-8'), salt)
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    ct = aesgcm.encrypt(nonce, message, None)
    b64 = lambda x: base64.urlsafe_b64encode(x).decode('utf-8')
    payload = f"ENC1${b64(salt)}${b64(nonce)}${b64(ct)}"
    return payload

def decrypt_payload(payload: str, password: str) -> bytes:
    if not payload.startswith("ENC1$"):
        raise ValueError("Payload not in expected ENC1 format.")
    try:
        _, b64salt, b64nonce, b64ct = payload.split("$", 3)
    except Exception:
        raise ValueError("Invalid payload format.")
    salt = base64.urlsafe_b64decode(b64salt)
    nonce = base64.urlsafe_b64decode(b64nonce)
    ct = base64.urlsafe_b64decode(b64ct)
    key = derive_key(password.encode('utf-8'), salt)
    aesgcm = AESGCM(key)
    pt = aesgcm.decrypt(nonce, ct, None)
    return pt

# ================= QR CODE FUNCTIONS =================
def make_qr(text: str, out_file: str, box_size=10, border=4):
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_Q,
        box_size=box_size,
        border=border,
    )
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(out_file)
    print(f"\n\033[92m[👑] QR saved as: {out_file}\033[0m")
    print(f"\033[93m[i] File location: {os.path.abspath(out_file)}\033[0m\n")

# ================= INTERACTIVE MENU =================
def interactive_menu():
    hacker_banner()
    
    while True:
        print("\033[96m" + "═"*70 + "\033[0m")
        print("\033[93m  [1] 🔐 Create Encrypted QR (Secret Message)\033[0m")
        print("\033[92m  [2] 📝 Create Plain QR\033[0m")
        print("\033[94m  [3] 🔓 Decrypt QR Message\033[0m")
        print("\033[91m  [4] ❌ Exit\033[0m")
        print("\033[96m" + "═"*70 + "\033[0m")
        
        choice = input("\n\033[92m[?] Select option > \033[0m")
        
        if choice == "1":
            # Encrypted QR
            print("\n\033[93m[!] Enter your secret message:\033[0m")
            secret = input("\033[92m> \033[0m")
            if not secret:
                print("\033[91m[!] No message entered!\033[0m")
                continue
            
            print("\n\033[93m[!] Set a password:\033[0m")
            password = input("\033[92m> \033[0m")
            if not password:
                print("\033[91m[!] Password required!\033[0m")
                continue
            
            print("\n\033[93m[!] Output filename (e.g., secret_qr.png):\033[0m")
            filename = input("\033[92m> \033[0m")
            if not filename:
                filename = "encrypted_qr.png"
            if not filename.endswith('.png'):
                filename += '.png'
            
            loading_effect()
            
            try:
                payload = encrypt_message(secret.encode('utf-8'), password)
                make_qr(payload, filename)
                print("\033[92m[✓] ENCRYPTED QR CREATED SUCCESSFULLY!\033[0m")
                print(f"\033[93m[!] Password: {password}\033[0m")
                print(f"\033[93m[!] Share this password with recipient!\033[0m\n")
            except Exception as e:
                print(f"\033[91m[✗] Error: {e}\033[0m")
        
        elif choice == "2":
            # Plain QR
            print("\n\033[93m[!] Enter your message:\033[0m")
            message = input("\033[92m> \033[0m")
            if not message:
                print("\033[91m[!] No message entered!\033[0m")
                continue
            
            print("\n\033[93m[!] Output filename (e.g., qr_code.png):\033[0m")
            filename = input("\033[92m> \033[0m")
            if not filename:
                filename = "plain_qr.png"
            if not filename.endswith('.png'):
                filename += '.png'
            
            loading_effect()
            make_qr(message, filename)
            print("\033[92m[✓] PLAIN QR CREATED SUCCESSFULLY!\033[0m\n")
        
        elif choice == "3":
            # Decrypt
            print("\n\033[93m[!] Paste the encrypted QR text:\033[0m")
            encrypted_text = input("\033[92m> \033[0m")
            if not encrypted_text:
                print("\033[91m[!] No text entered!\033[0m")
                continue
            
            print("\n\033[93m[!] Enter password:\033[0m")
            password = input("\033[92m> \033[0m")
            if not password:
                print("\033[91m[!] Password required!\033[0m")
                continue
            
            loading_effect()
            
            try:
                decrypted = decrypt_payload(encrypted_text, password)
                print("\n\033[96m" + "═"*70 + "\033[0m")
                print("\033[92m[✓] DECRYPTED MESSAGE:\033[0m")
                print("\033[97m" + "═"*70 + "\033[0m")
                print(f"\n\033[93m{decrypted.decode('utf-8')}\033[0m\n")
                print("\033[96m" + "═"*70 + "\033[0m\n")
            except Exception as e:
                print(f"\033[91m[✗] Decryption failed: {e}\033[0m\n")
        
        elif choice == "4":
            print("\n\033[91m[!] Exiting QR Secret Tool...\033[0m")
            print("\033[93m[!] Stay Secure! - HasnainDarkNet👑\033[0m\n")
            sys.exit(0)
        
        else:
            print("\033[91m[!] Invalid option! Try again.\033[0m")
        
        input("\n\033[93m[!] Press Enter to continue...\033[0m")
        hacker_banner()

# ================= MAIN =================
if __name__ == "__main__":
    try:
        interactive_menu()
    except KeyboardInterrupt:
        print("\n\033[91m\n[!] Interrupted! Exiting...\033[0m")
        sys.exit(0)
