import os
import hashlib
import base58

# Install: pip install ecdsa
from ecdsa import SigningKey, SECP256k1


def sha256(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()


def ripemd160(data: bytes) -> bytes:
    try:
        return hashlib.new('ripemd160', data).digest()
    except ValueError:
        raise RuntimeError("RIPEMD160 is not available in this Python build.")


def checksum(payload: bytes) -> bytes:
    return sha256(sha256(payload).digest())[:4]


def private_key_to_wif(priv_key: bytes, compressed: bool = True) -> str:
    payload = b"\x80" + priv_key
    if compressed:
        payload += b"\x01"
    return base58.b58encode(payload + checksum(payload)).decode()


def private_key_to_address(priv_key: bytes) -> str:
    sk = SigningKey.from_string(priv_key, curve=SECP256k1)
    vk = sk.get_verifying_key()
    pubkey = vk.to_string("compressed")
    pubkey_hash = ripemd160(sha256(pubkey))
    payload = b"\x00" + pubkey_hash
    address = payload + checksum(payload)
    return base58.b58encode(address).decode()


def generate_random_private_key() -> bytes:
    return os.urandom(32)


if __name__ == "__main__":
    priv = generate_random_private_key()
    print("Private key (hex):", priv.hex())
    print("WIF:", private_key_to_wif(priv))
    print("Bitcoin address:", private_key_to_address(priv))
