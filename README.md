# Bitcoin Address Generator

Educational Flask app for generating and inspecting **legacy Bitcoin mainnet addresses**.

## Included features

- Secure OS randomness for demo key generation
- secp256k1 key/address derivation
- Private-key hex and WIF import
- Bulk generation (1–20 wallets)
- Base58Check legacy-address validation
- QR codes, copy buttons, CSV export, and light/dark theme
- Browser-only recent-wallet history
- Read-only balance lookup through mempool.space

## Run

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000/.

## Balance lookup

The dashboard queries the public mempool.space API for a legacy address balance. It never sends private keys to that service. Network availability and API limits apply.

## Safety

This is an educational demo, not a production wallet. Never paste a real private key or WIF into a website, commit secrets, export private keys to CSV, or use generated keys for real funds. Browser history and CSV files can expose private keys.

The app does not sign or broadcast transactions. Any transaction-builder work should be done offline with a reviewed wallet library and testnet first.
