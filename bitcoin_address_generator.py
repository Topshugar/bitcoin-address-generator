import hashlib
import os

import base58
from ecdsa import SECP256k1, SigningKey

SECP256K1_ORDER = SECP256k1.order


def sha256(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()


def ripemd160(data: bytes) -> bytes:
    try:
        return hashlib.new("ripemd160", data).digest()
    except ValueError as exc:
        raise RuntimeError("RIPEMD160 is not available in this Python build.") from exc


def checksum(payload: bytes) -> bytes:
    return sha256(sha256(payload))[:4]


def private_key_to_wif(private_key: bytes) -> str:
    payload = b"\x80" + private_key + b"\x01"
    return base58.b58encode(payload + checksum(payload)).decode("ascii")


def private_key_to_address(private_key: bytes) -> str:
    verifying_key = SigningKey.from_string(private_key, curve=SECP256k1).get_verifying_key()
    public_key = verifying_key.to_string("compressed")
    payload = b"\x00" + ripemd160(sha256(public_key))
    return base58.b58encode(payload + checksum(payload)).decode("ascii")


def _validate_private_key(private_key: bytes) -> None:
    if len(private_key) != 32 or not 1 <= int.from_bytes(private_key, "big") < SECP256K1_ORDER:
        raise ValueError("Private key is outside the valid secp256k1 range.")


def generate_random_private_key() -> bytes:
    while True:
        private_key = os.urandom(32)
        if 1 <= int.from_bytes(private_key, "big") < SECP256K1_ORDER:
            return private_key


def wallet_from_private_key(private_key: bytes) -> dict:
    _validate_private_key(private_key)
    return {
        "private_key_hex": private_key.hex(),
        "wif": private_key_to_wif(private_key),
        "bitcoin_address": private_key_to_address(private_key),
    }


def generate_wallet() -> dict:
    return wallet_from_private_key(generate_random_private_key())


def generate_wallets(count: int = 1) -> list[dict]:
    if not 1 <= count <= 20:
        raise ValueError("count must be between 1 and 20.")
    return [generate_wallet() for _ in range(count)]


def wallet_from_private_key_hex(value: str) -> dict:
    try:
        private_key = bytes.fromhex(value.strip())
    except ValueError as exc:
        raise ValueError("Private key is not valid hexadecimal.") from exc
    if len(private_key) != 32:
        raise ValueError("Private key must be exactly 64 hex characters.")
    return wallet_from_private_key(private_key)


def wallet_from_wif(value: str) -> dict:
    try:
        decoded = base58.b58decode(value.strip())
    except ValueError as exc:
        raise ValueError("WIF is not valid Base58.") from exc
    if len(decoded) not in (37, 38) or decoded[-4:] != checksum(decoded[:-4]):
        raise ValueError("WIF checksum or length is invalid.")
    payload = decoded[:-4]
    if payload[0] != 0x80:
        raise ValueError("Only Bitcoin mainnet WIF is supported.")
    private_key = payload[1:-1] if len(payload) == 34 and payload[-1] == 0x01 else payload[1:]
    return wallet_from_private_key(private_key)


def validate_bitcoin_address(address: str) -> bool:
    if not 26 <= len(address) <= 35:
        return False
    try:
        decoded = base58.b58decode(address)
    except ValueError:
        return False
    return len(decoded) == 25 and decoded[0] == 0x00 and decoded[-4:] == checksum(decoded[:-4])


if __name__ == "__main__":
    print(generate_wallet())
