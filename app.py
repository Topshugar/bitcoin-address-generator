import base64
import io

import qrcode
from flask import Flask, jsonify, render_template, request

from bitcoin_address_generator import (
    generate_wallets,
    validate_bitcoin_address,
    wallet_from_private_key_hex,
    wallet_from_wif,
)

app = Flask(__name__)


def generate_qr_data_url(value: str) -> str:
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(value)
    qr.make(fit=True)
    image = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buffer.getvalue()).decode("utf-8")


def add_qr_codes(wallets: list[dict]) -> list[dict]:
    for wallet in wallets:
        wallet["qr_code"] = generate_qr_data_url(wallet["bitcoin_address"])
    return wallets


@app.route("/", methods=["GET", "POST"])
def index():
    wallets = []
    count = request.form.get("count", 1, type=int) or 1
    error_message = None
    imported_message = None

    if request.method == "POST" and request.form.get("import_value", "").strip():
        import_value = request.form["import_value"].strip()
        try:
            if request.form.get("import_type") == "wif":
                wallet = wallet_from_wif(import_value)
            else:
                wallet = wallet_from_private_key_hex(import_value)
            wallets = add_qr_codes([wallet])
            imported_message = "Wallet imported successfully."
        except ValueError as exc:
            error_message = str(exc)
    else:
        count = min(max(count, 1), 20)
        wallets = add_qr_codes(generate_wallets(count))

    return render_template(
        "index.html",
        wallets=wallets,
        count=count,
        error_message=error_message,
        imported_message=imported_message,
    )


@app.get("/api/generate")
def api_generate():
    count = min(max(request.args.get("count", 1, type=int) or 1, 1), 20)
    return jsonify({"wallets": add_qr_codes(generate_wallets(count))})


@app.get("/api/validate")
def api_validate():
    address = request.args.get("address", "").strip()
    return jsonify({"address": address, "valid": validate_bitcoin_address(address)})


@app.get("/api/balance")
def api_balance():
    """Return an address balance from mempool.space without handling private keys."""
    import urllib.error
    import urllib.request

    address = request.args.get("address", "").strip()
    if not validate_bitcoin_address(address):
        return jsonify({"error": "Invalid legacy Bitcoin address."}), 400

    url = f"https://mempool.space/api/address/{address}"
    try:
        with urllib.request.urlopen(url, timeout=8) as response:
            data = __import__("json").load(response)
        chain = data.get("chain_stats", {})
        mempool = data.get("mempool_stats", {})
        confirmed = chain.get("funded_txo_sum", 0) - chain.get("spent_txo_sum", 0)
        pending = mempool.get("funded_txo_sum", 0) - mempool.get("spent_txo_sum", 0)
        return jsonify({
            "address": address,
            "confirmed_satoshis": confirmed,
            "pending_satoshis": pending,
            "confirmed_btc": confirmed / 100_000_000,
            "pending_btc": pending / 100_000_000,
            "source": "mempool.space",
        })
    except (urllib.error.URLError, TimeoutError, ValueError) as exc:
        return jsonify({"error": f"Balance lookup failed: {exc}"}), 502


if __name__ == "__main__":
    app.run(debug=True)
