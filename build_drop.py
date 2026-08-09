#!/usr/bin/env python3
"""Encrypt a self-contained HTML page and emit the password-gated index.html.

Usage: BENCH_PASSWORD=... build_drop.py <plaintext.html> <out.html> <posted-iso>
"""
import base64, json, os, sys, secrets, datetime
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

ITERATIONS = 310_000

def main():
    src, out, posted = sys.argv[1], sys.argv[2], sys.argv[3]
    password = os.environ.get("BENCH_PASSWORD")
    if not password:
        sys.exit("BENCH_PASSWORD not set (see .env)")

    plaintext = open(src, "rb").read()
    salt = secrets.token_bytes(16)
    nonce = secrets.token_bytes(12)
    key = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt,
                     iterations=ITERATIONS).derive(password.encode())
    ct = AESGCM(key).encrypt(nonce, plaintext, None)

    payload = json.dumps({
        "salt": base64.b64encode(salt).decode(),
        "nonce": base64.b64encode(nonce).decode(),
        "ct": base64.b64encode(ct).decode(),
    })

    template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 "wrapper.template.html")
    html = open(template_path).read()
    html = html.replace("{{PAYLOAD}}", payload).replace("{{POSTED}}", posted)
    open(out, "w").write(html)
    print(f"encrypted {len(plaintext)} bytes -> {out} ({len(ct)} ct bytes)")

if __name__ == "__main__":
    main()
