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

# Try to import QR scanner libraries
try:
    from PIL import Image
    import pyzbar.pyzbar as pyzbar
    QR_SCAN_AVAILABLE = True
except ImportError:
    QR_SCAN_AVAILABLE = False

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

def loading_effect():
    print("\033[92m[*] Processing", end="")
    for i in range(3):
        time.sleep(0.3)
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
    print(f"\033[93m[i] Location: {os.path.abspath(out_file)}\033[0m\n")

def scan_qr_image(image_path):
    """Scan QR code from image file and return the data"""
    if not QR_SCAN_AVAILABLE:
        return None, "PIL or pyzbar not installed. Run: pip install pillow pyzbar"
    
    try:
        if not os.path.exists(image_path):
            return None, f"File not found: {image_path}"
        
        # Open and scan image
        img = Image.open(image_path)
        decoded_objects = pyzbar.decode(img)
        
        if not decoded_objects:
            return None, "No QR code found in image"
        
        # Get data from first QR code
        qr_data = decoded_objects[0].data.decode('utf-8')
        return qr_data, None
        
    except Exception as e:
        return None, f"Error scanning QR: {str(e)}"

# ================= INTERACTIVE MENU =================
def interactive_menu():
    hacker_banner()
    
    # Show QR scan status
    if not QR_SCAN_AVAILABLE:
        print("\033[91m[!] Warning: QR scanning not available!\033[0m")
        print("\033[93m[!] Install required packages: pip install pillow pyzbar\033[0m\n")
    
    while True:
        print("\033[96m" + "═"*70 + "\033[0m")
        print("\033[92m  [1] 📝 Create Encrypted QR\033[0m")
        print("\033[93m  [2] 📄 Create Plain QR\033[0m")
        print("\033[91m  [3] 🔓 Decrypt from QR Image File\033[0m")
        print("\033[91m  [4] ⌨️  Decrypt from Text (Manual Paste)\033[0m")
        print("\033[91m  [5] ❌ Exit\033[0m")
        print("\033[96m" + "═"*70 + "\033[0m")
        
        choice = input("\n\033[92m[?] Select option > \033[0m")
        
        if choice == "1":
            # Create Encrypted QR
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
                print("\033[92m[✓] ENCRYPTED QR CREATED!\033[0m")
                print(f"\033[93m[!] Password: {password}\033[0m")
                print(f"\033[93m[!] Share this password with recipient!\033[0m\n")
            except Exception as e:
                print(f"\033[91m[✗] Error: {e}\033[0m")
        
        elif choice == "2":
            # Create Plain QR
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
            print("\033[92m[✓] PLAIN QR CREATED!\033[0m\n")
        
        elif choice == "3":
            # Decrypt directly from QR image file
            if not QR_SCAN_AVAILABLE:
                print("\033[91m[!] QR scanning not available!\033[0m")
                print("\033[93m[!] Install: pip install pillow pyzbar\033[0m")
                input("\nPress Enter to continue...")
                continue
            
            print("\n\033[93m[!] Enter path to QR image file:\033[0m")
            print("\033[90m(Example: encrypted_qr.png or C:/path/to/qr.png)\033[0m")
            image_path = input("\033[92m> \033[0m").strip()
            
            if not image_path:
                print("\033[91m[!] No file path entered!\033[0m")
                continue
            
            print("\n\033[93m[!] Scanning QR code from image...\033[0m")
            loading_effect()
            
            encrypted_text, error = scan_qr_image(image_path)
            
            if error:
                print(f"\033[91m[✗] {error}\033[0m")
                continue
            
            print(f"\033[92m[✓] QR scanned successfully!\033[0m")
            print(f"\033[90mData preview: {encrypted_text[:80]}...\033[0m\n")
            
            print("\033[93m[!] Enter the password:\033[0m")
            password = input("\033[92m> \033[0m")
            
            if not password:
                print("\033[91m[!] Password required!\033[0m")
                continue
            
            loading_effect()
            
            try:
                decrypted = decrypt_payload(encrypted_text.strip(), password)
                print("\n\033[96m" + "═"*70 + "\033[0m")
                print("\033[92m[✓] DECRYPTED MESSAGE:\033[0m")
                print("\033[97m" + "═"*70 + "\033[0m")
                print(f"\n\033[93m{decrypted.decode('utf-8')}\033[0m\n")
                print("\033[96m" + "═"*70 + "\033[0m\n")
            except Exception as e:
                print(f"\033[91m[✗] Decryption failed: {e}\033[0m")
                print("\033[93m[!] Make sure you entered the correct password!\033[0m\n")
        
        elif choice == "4":
            # Manual text decryption
            print("\n\033[93m[!] Paste the encrypted text from QR:\033[0m")
            print("\033[90m(Scan QR with phone/app and paste the text here)\033[0m")
            print("\033[90m(Text should start with 'ENC1$')\033[0m")
            encrypted_text = input("\033[92m> \033[0m").strip()
            
            if not encrypted_text:
                print("\033[91m[!] No text entered!\033[0m")
                continue
            
            if not encrypted_text.startswith("ENC1$"):
                print("\033[91m[!] Invalid format! Text should start with 'ENC1$'\033[0m")
                print("\033[93m[!] Make sure you copied the complete encrypted text\033[0m")
                continue
            
            print("\n\033[93m[!] Enter the password:\033[0m")
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
                print(f"\033[91m[✗] Decryption failed: {e}\033[0m")
                print("\033[93m[!] Check password or encrypted text\033[0m\n")
        
        elif choice == "5":
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
        # Check and install requirements提示
        if not QR_SCAN_AVAILABLE:
            print("\033[93m[!] For QR scanning feature, install:\033[0m")
            print("\033[96m    pip install pillow pyzbar\033[0m\n")
            time.sleep(2)
        
        interactive_menu()
    except KeyboardInterrupt:
        print("\n\033[91m\n[!] Interrupted! Exiting...\033[0m")
        sys.exit(0)
