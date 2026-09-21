# Bitcoin Address Generator

This project generates a random Bitcoin private key and derives a Bitcoin wallet address using the secp256k1 curve.

## Features

- Generates a random 32-byte private key
- Derives a compressed Bitcoin public key
- Creates a Bitcoin address in Base58Check format
- Exports the wallet in WIF format

## Requirements

Python 3.9+

Install the required dependency:

```bash
pip install ecdsa
```

## Run

```bash
python bitcoin_address_generator.py
```

## Example Output

```text
Private key (hex): 5c27e6d9a4f6d8f7d1c9d4d7f0d2f7f8d6e7d3a7b6d4c6b5f6e7d9b4a3c2d1
WIF: 5HueCGU8rMjxQhvkeCw5k5m7n8Hf8mJvJ7J5T1Y3YJH2w5K5Wg2
Bitcoin address: 1J7d8Y4Q8t3S8mT8G8M2p8tP8pW4u7H7pY
```

## Important

This is an educational project for learning Bitcoin address generation. It is not a production wallet and should not be used to store real funds.

## File Structure

- `bitcoin_address_generator.py` — main script
