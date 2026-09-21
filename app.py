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


def generate_wallet() -> dict:
    private_key = generate_random_private_key()
    return {
        "private_key_hex": private_key.hex(),
        "wif": private_key_to_wif(private_key),
        "bitcoin_address": private_key_to_address(private_key),
    }


def generate_wallets(count: int = 1) -> list:
    if count < 1:
        raise ValueError("count must be at least 1")
    return [generate_wallet() for _ in range(count)]


def validate_bitcoin_address(address: str) -> bool:
    if not address or len(address) < 26 or len(address) > 35:
        return False

    try:
        decoded = base58.b58decode(address)
    except ValueError:
        return False

    if len(decoded) < 5:
        return False

    payload = decoded[:-4]
    checksum = decoded[-4:]
    expected_checksum = sha256(sha256(payload))[:4]
    return checksum == expected_checksum


if __name__ == "__main__":
    wallet = generate_wallet()
    print("Private key (hex):", wallet["private_key_hex"])
    print("WIF:", wallet["wif"])
    print("Bitcoin address:", wallet["bitcoin_address"])
