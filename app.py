from flask import Flask, render_template, jsonify, request
from bitcoin_address_generator import generate_wallet

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    wallet = generate_wallet()
    if request.method == "POST":
        wallet = generate_wallet()
    return render_template("index.html", wallet=wallet)


@app.route("/api/generate")
def api_generate():
    return jsonify(generate_wallet())


if __name__ == "__main__":
    app.run(debug=True)
