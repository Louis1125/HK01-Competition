import os
import requests
from flask import Flask, request
from datetime import datetime

app = Flask(__name__)
TOKEN = os.getenv("TELEGRAM_TOKEN")  # Set this in environment / Railway secrets
DEFAULT_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")  # Optional


def send_msg(chat_id, text):
    """Send Telegram message (safe no-exception wrapper)."""
    if not TOKEN:
        app.logger.warning("TELEGRAM_TOKEN not set; skipping send")
        return False
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True,
    }
    try:
        resp = requests.post(url, json=payload, timeout=8)
        resp.raise_for_status()
        return True
    except Exception as e:
        app.logger.exception("Failed to send Telegram message: %s", e)
        return False


@app.route("/")
def home():
    return "🏥 SmartElderCare Bot is running!"


@app.route("/webhook", methods=["POST"])
def webhook():
    """Simple webhook handler to respond to basic commands.

    This is intentionally small — expand handlers here to integrate
    with your main programme via HTTP/DB as needed.
    """
    data = request.json or {}

    if "message" in data:
        msg = data["message"]
        chat_id = msg["chat"]["id"]
        text = msg.get("text", "").strip() or ""

        # Basic command handling
        if text == "/start":
            send_msg(chat_id, "🏥 *SmartElderCare Bot*\nChoose language or use /help to list commands")
        elif text == "/patients":
            send_msg(chat_id, "👥 *Patients:*\n• P001: Chan Tai Man\n• P002: Lee Siu Ming")
        elif text.startswith("/alert "):
            # Example: /alert P001 Missed medication
            send_msg(chat_id, f"🚨 Alert sent: {text[7:].strip()}")
        elif text == "/help":
            send_msg(chat_id, "/start - Welcome\n/help - List commands\n/patients - List sample patients")
        else:
            # Echo unknown commands for debugging
            send_msg(chat_id, f"📨 Unrecognized command: {text}\nUse /help to see commands")

    return ("OK", 200)


@app.route("/health")
def health():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
