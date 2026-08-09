# Workbench

A temporary, password-gated surface. One drop at a time; each new drop replaces
the last; drops expire after 24 hours (hourly GitHub Action resets the bench).

The published `index.html` contains only an AES-256-GCM ciphertext of the
current drop plus an unlock form — content is encrypted locally before it is
ever committed, and decryption happens in the browser (WebCrypto, PBKDF2).

Tooling is in this repo (`bench` CLI, `build_drop.py`, `wrapper.template.html`);
the password lives only in a gitignored `.env` on the owner's machine.
