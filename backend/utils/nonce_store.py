# utils/nonce_store.py

used_nonces = set()

def is_nonce_used(nonce):
    return nonce in used_nonces

def mark_nonce_used(nonce):
    used_nonces.add(nonce)
