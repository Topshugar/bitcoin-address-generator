<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Bitcoin Address Generator</title>
    <style>
      :root {
        --bg: #0f172a;
        --panel: #111827;
        --panel-soft: #1f2937;
        --text: #f8fafc;
        --muted: #cbd5e1;
        --highlight: #f59e0b;
        --highlight-2: #22c55e;
        --border: #374151;
      }
      * { box-sizing: border-box; }
      body {
        margin: 0;
        font-family: Arial, sans-serif;
        background: linear-gradient(135deg, #0f172a, #111827);
        color: var(--text);
        min-height: 100vh;
        padding: 32px 16px;
      }
      .container {
        max-width: 1100px;
        margin: 0 auto;
      }
      .card {
        background: rgba(17, 24, 39, 0.9);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.35);
      }
      h1 {
        margin-top: 0;
        color: var(--highlight);
      }
      .controls {
        display: flex;
        gap: 12px;
        margin: 20px 0 28px;
        align-items: center;
        flex-wrap: wrap;
      }
      input[type="number"] {
        background: #0f172a;
        color: var(--text);
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 12px 14px;
        width: 110px;
      }
      button {
        background: var(--highlight);
        color: #0f172a;
        border: 0;
        border-radius: 8px;
        padding: 12px 18px;
        font-weight: bold;
        cursor: pointer;
      }
      button.secondary {
        background: var(--highlight-2);
        color: #052e16;
      }
      .wallet-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
        gap: 20px;
      }
      .wallet {
        background: rgba(31, 41, 55, 0.8);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 18px;
      }
      .wallet h3 {
        margin-top: 0;
        color: var(--highlight);
      }
      .field {
        margin-bottom: 12px;
      }
      label {
        display: block;
        font-weight: bold;
        color: var(--muted);
        margin-bottom: 6px;
      }
      .value {
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 12px 14px;
        word-break: break-all;
        color: var(--text);
      }
      .validation {
        margin-top: 18px;
        display: flex;
        gap: 12px;
        align-items: center;
        flex-wrap: wrap;
      }
      .validation input {
        flex: 1;
        min-width: 260px;
        background: #0f172a;
        border: 1px solid var(--border);
        color: var(--text);
        border-radius: 8px;
        padding: 12px 14px;
      }
      .status {
        font-weight: bold;
        min-width: 120px;
      }
    </style>
  </head>
  <body>
    <div class="container">
      <div class="card">
        <h1>Bitcoin Address Generator</h1>

        <form method="post">
          <div class="controls">
            <label for="count">Generate wallets:</label>
            <input id="count" name="count" type="number" min="1" max="20" value="{{ count }}" />
            <button type="submit">Generate</button>
          </div>
        </form>

        <div class="validation">
          <input id="addressInput" type="text" placeholder="Enter a Bitcoin address to validate" />
          <button class="secondary" type="button" id="validateBtn">Validate</button>
          <div class="status" id="validationStatus">Waiting...</div>
        </div>

        <div class="wallet-grid" style="margin-top: 24px;">
          {% for wallet in wallets %}
          <div class="wallet">
            <h3>Wallet {{ loop.index }}</h3>

            <div class="field">
              <label>Private Key (hex)</label>
              <div class="value">{{ wallet.private_key_hex }}</div>
            </div>

            <div class="field">
              <label>WIF</label>
              <div class="value">{{ wallet.wif }}</div>
            </div>

            <div class="field">
              <label>Bitcoin Address</label>
              <div class="value">{{ wallet.bitcoin_address }}</div>
            </div>
          </div>
          {% endfor %}
        </div>
      </div>
    </div>

    <script>
      document.getElementById('validateBtn').addEventListener('click', function () {
        const address = document.getElementById('addressInput').value.trim();
        const statusEl = document.getElementById('validationStatus');

        if (!address) {
          statusEl.textContent = 'Enter an address';
          statusEl.style.color = '#fbbf24';
          return;
        }

        fetch('/api/validate?address=' + encodeURIComponent(address))
          .then(response => response.json())
          .then(data => {
            if (data.valid) {
              statusEl.textContent = 'Valid Bitcoin address';
              statusEl.style.color = '#4ade80';
            } else {
              statusEl.textContent = 'Invalid Bitcoin address';
              statusEl.style.color = '#f87171';
            }
          })
          .catch(() => {
            statusEl.textContent = 'Error';
            statusEl.style.color = '#f87171';
          });
      });
    </script>
  </body>
</html>
