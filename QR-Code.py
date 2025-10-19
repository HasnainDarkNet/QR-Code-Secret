#!/usr/bin/env python3
"""
───────────────────────────────────────────────
     QR Secret Encoder / Decoder by
          HasnainDarkNet👑
───────────────────────────────────────────────

Usage:
  # Plain (no encryption)
  python3 qr_secret.py make "This is a secret message" qr_plain.png

  # Encrypted QR (password protected)
  python3 qr_secret.py makeenc "This is a secret message" qr_enc.png mypassword

  # Decrypt scanned encrypted payload (paste the scanned text)
  python3 qr_secret.py decrypt "ENC1$<b64salt>$<b64nonce>$<b64ct>" mypassword

───────────────────────────────────────────────
"""

import sys
import qrcode
import base64
import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# ──────────────── HasnainDarkNet👑 Encryption Helpers ────────────────
def derive_key(password: bytes, salt: bytes, iterations: int = 200000) -> bytes:
    """Derives AES-256 key from password + salt."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
    )
    return kdf.derive(password)

def encrypt_message(message: bytes, password: str) -> str:
    """Encrypt message using AES-GCM, return ENC1 payload."""
    salt = os.urandom(16)
    key = derive_key(password.encode('utf-8'), salt)
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    ct = aesgcm.encrypt(nonce, message, None)
    b64 = lambda x: base64.urlsafe_b64encode(x).decode('utf-8')
    payload = f"ENC1${b64(salt)}${b64(nonce)}${b64(ct)}"
    return payload

def decrypt_payload(payload: str, password: str) -> bytes:
    """Decrypt ENC1 payload using AES-GCM."""
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

# ──────────────── HasnainDarkNet👑 QR Code Helpers ────────────────
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
    print(f"\n[👑 HasnainDarkNet] QR saved as: {out_file}")
    print("[i] If content is long, use a scanner that supports large payloads.\n")

# ──────────────── HasnainDarkNet👑 CLI ────────────────
def print_usage():
    print("───────────────────────────────────────────────")
    print(" 🔐 QR Secret Tool — HasnainDarkNet👑")
    print("───────────────────────────────────────────────")
    print("Usage:")
    print("  python3 qr_secret.py make \"your secret text\" out_qr.png")
    print("  python3 qr_secret.py makeenc \"your secret text\" out_qr.png password")
    print("  python3 qr_secret.py decrypt \"ENC1$...\" password")
    print("───────────────────────────────────────────────")

# ──────────────── HasnainDarkNet👑 Main ────────────────
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_usage(); sys.exit(1)
    cmd = sys.argv[1].lower()

    if cmd == "make":
        if len(sys.argv) != 4:
            print_usage(); sys.exit(1)
        _, _, text, out = sys.argv
        make_qr(text, out)

    elif cmd == "makeenc":
        if len(sys.argv) != 5:
            print_usage(); sys.exit(1)
        _, _, text, out, pwd = sys.argv
        payload = encrypt_message(text.encode('utf-8'), pwd)
        make_qr(payload, out)
        print(f"[+] Encrypted payload created by HasnainDarkNet👑\n")

    elif cmd == "decrypt":
        if len(sys.argv) != 4:
            print_usage(); sys.exit(1)
        _, _, payload_text, pwd = sys.argv
        try:
            pt = decrypt_payload(payload_text, pwd)
            print(f"\n[+] Decrypted message by HasnainDarkNet👑:")
            print("───────────────────────────────────────────────")
            print(pt.decode('utf-8'))
            print("───────────────────────────────────────────────")
        except Exception as e:
            print("Error decrypting:", e)
    else:
        print_usage()
