import os
import requests
from typing import Dict, Any

PROVIDER = os.environ.get("WHATSAPP_PROVIDER", "twilio").lower()  # 'meta' or 'twilio'
TEST_MODE = os.environ.get('TEST_MODE', '').strip() in ('1', 'true', 'yes')

# --- Meta WhatsApp Cloud API settings ---
META_TOKEN = os.environ.get("WHATSAPP_TOKEN")           # long-lived token for Meta Cloud API
META_PHONE_ID = os.environ.get("PHONE_NUMBER_ID")       # phone number id from Business Manager
META_API_VERSION = os.environ.get("WHATSAPP_API_VERSION", "v15.0")

# --- Twilio settings ---
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_FROM = os.environ.get("TWILIO_WHATSAPP_FROM")  # e.g. 'whatsapp:+1415xxxxxxx'


def _send_meta_text(to: str, message: str) -> Dict[str, Any]:
    # In normal mode this sends via Meta Cloud API.
    if TEST_MODE:
        # simulated response for demo/testing
        print(f"[TEST MODE] Meta WhatsApp send to {to}: {message}")
        return {"status": "ok", "provider": "meta", "to": to, "body": message}
    if not META_TOKEN or not META_PHONE_ID:
        raise RuntimeError("META WhatsApp not configured (WHATSAPP_TOKEN, PHONE_NUMBER_ID)")
    url = f"https://graph.facebook.com/{META_API_VERSION}/{META_PHONE_ID}/messages"
    headers = {"Authorization": f"Bearer {META_TOKEN}", "Content-Type": "application/json"}
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": message}
    }
    r = requests.post(url, headers=headers, json=payload, timeout=10)
    r.raise_for_status()
    return r.json()


def _send_twilio_text(to: str, message: str) -> Dict[str, Any]:
    if TEST_MODE:
        # simulated response for demo/testing
        print(f"[TEST MODE] Twilio WhatsApp send to {to}: {message}")
        return {"status": "ok", "provider": "twilio", "to": to, "body": message}
    if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN or not TWILIO_WHATSAPP_FROM:
        raise RuntimeError("Twilio not configured (TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_FROM)")
    url = f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_ACCOUNT_SID}/Messages.json"
    data = {
        "From": TWILIO_WHATSAPP_FROM,
        "To": f"whatsapp:{to}",
        "Body": message
    }
    r = requests.post(url, data=data, auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN), timeout=10)
    r.raise_for_status()
    return r.json()


def send_whatsapp_text(to_phone: str, message: str) -> Dict[str, Any]:
    """
    Send a WhatsApp text using configured provider.
    `to_phone` must be in E.164 format, e.g. +85291234567
    Returns provider response (dict) or raises on error.
    """
    to_phone = to_phone.strip()
    if PROVIDER == "meta":
        return _send_meta_text(to_phone, message)
    else:
        return _send_twilio_text(to_phone, message)
