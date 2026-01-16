import os
import requests
from flask import Flask, request, jsonify

# Local helpers (created alongside this file)
from whatsapp_provider import send_whatsapp_text
from patient_manager import get_patient, set_consent

app = Flask(__name__)
TOKEN = os.getenv("TELEGRAM_TOKEN")  # Set this in environment or via .env (do NOT commit)

# ========== SIMPLE MESSAGE SENDER ==========
def send_telegram(chat_id, text):
    """Send message to Telegram"""
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    try:
        response = requests.post(url, json=payload, timeout=5)
        return response.status_code == 200
    except Exception:
        return False

# ========== COMMAND HANDLERS ==========
def handle_start(chat_id, user_name):
    """Handle /start command"""
    welcome = f"""
🏥 *SmartElderCare Bot* - HK01 2025
────────────────────
Welcome, {user_name}!

I'm your assistant for elderly care monitoring.

*Quick Commands:*
/patients - View patients
/medications - Medication schedule
/alerts - Recent alerts
/compliance - 7-day reports
/emergency - Emergency contacts
/help - All commands
────────────────────
Type /help for more options!
    """
    send_telegram(chat_id, welcome)

def handle_help(chat_id):
    """Handle /help command"""
    help_text = """
🤖 *SmartElderCare Bot Commands*
────────────────────
*Patient Management*
/patients - List all patients
/medications - Medication schedules
/compliance - 7-day compliance reports

*Monitoring & Alerts*
/alerts - View recent alerts
/camera - Camera system status
/schedule - Daily care schedule

*Communication*
/emergency - Emergency contacts
/whatsapp - Send WhatsApp message: `/whatsapp P001 Hello` 
/consent - Manage WhatsApp consent: `/consent P001 yes`

*System*
/start - Start the bot
/help - This help message
────────────────────
*Example:* `/patients` or `/whatsapp P001 Hello`
    """
    send_telegram(chat_id, help_text)

def handle_patients(chat_id):
    """Handle /patients command"""
    patients_text = """
👥 *Patient List* - HK Elderly Care Center
────────────────────
*P001 - Chan Tai Man (78)*
📍 Room: A101
📞 Phone: +852 9123 4567
💊 Conditions: Diabetes, Hypertension
✅ WhatsApp: Enabled

*P002 - Lee Siu Ming (82)*
📍 Room: B203  
📞 Phone: +852 9234 5678
💊 Conditions: Arthritis, Hypertension
⏳ WhatsApp: Pending consent

*P003 - Wong Mei Ling (75)*
📍 Room: C305
📞 Phone: +852 9345 6789
💊 Conditions: Dementia
✅ WhatsApp: Enabled
────────────────────
Use: `/medications P001` for details
    """
    send_telegram(chat_id, patients_text)

def handle_alerts(chat_id):
    """Handle /alerts command"""
    alerts_text = """
🚨 *Recent Alerts* - Last 24 Hours
────────────────────
🟢 14:30 - P001: Medication taken (Metformin)
🟡 13:45 - CAM-B203: Person detected (87%)
🟢 12:00 - P002: Lunch medication reminder
🔴 10:15 - P001: Missed morning medication
🟡 09:30 - CAM-A101: Motion detected
────────────────────
*System Status:* All operational
*Next Check:* Automatic in 15 minutes
    """
    send_telegram(chat_id, alerts_text)

# ========== WEBHOOK HANDLER ==========
@app.route('/webhook', methods=['POST'])
def webhook():
    """Main Telegram webhook handler"""
    try:
        data = request.json
        if "message" in data:
            msg = data["message"]
            chat_id = msg["chat"]["id"]
            text = msg.get("text", "").strip()
            user_name = msg.get("from", {}).get("first_name", "User")

            print(f"📨 Received: {text} from {user_name}")

            # Handle commands
            if text == "/start" or text == "/start@SmartElderCareBot":
                handle_start(chat_id, user_name)
            elif text == "/help" or text == "/help@SmartElderCareBot":
                handle_help(chat_id)
            elif text == "/patients" or text == "/patients@SmartElderCareBot":
                handle_patients(chat_id)
            elif text == "/alerts" or text == "/alerts@SmartElderCareBot":
                handle_alerts(chat_id)
            elif text == "/compliance" or text == "/compliance@SmartElderCareBot":
                send_telegram(chat_id, "📊 *7-Day Compliance:*\nP001: 93% ✅\nP002: 96% ✅\nP003: 88% ⚠️")
            elif text == "/emergency" or text == "/emergency@SmartElderCareBot":
                send_telegram(chat_id, "🚨 *Emergency Contacts:*\nDr. Wong: +852 1234 5678\nNurse: Ext. 101\nAmbulance: 999")
            elif text == "/camera" or text == "/camera@SmartElderCareBot":
                send_telegram(chat_id, "📷 *Camera Status:*\nCAM-A101: ✅ Online\nCAM-B203: ✅ Online\nLast detection: 2 min ago")
            elif text == "/schedule" or text == "/schedule@SmartElderCareBot":
                send_telegram(chat_id, "📅 *Daily Schedule:*\n8am: Meds\n12pm: Lunch\n6pm: Meds\n9pm: Bedtime")

            # ===== WhatsApp: send message to patient =====
            elif text.startswith("/whatsapp "):
                parts = text.split(" ", 2)
                if len(parts) < 3:
                    send_telegram(chat_id, "Usage: /whatsapp <patient_id> <message>")
                else:
                    pid = parts[1].strip().upper()
                    msg_body = parts[2].strip()
                    patient = get_patient(pid)
                    if not patient:
                        send_telegram(chat_id, f"Unknown patient id: {pid}")
                    elif not patient.get("consent", False):
                        send_telegram(chat_id, f"Patient {pid} has not consented to WhatsApp messages.")
                    else:
                        try:
                            resp = send_whatsapp_text(patient["phone"], msg_body)
                            send_telegram(chat_id, f"WhatsApp sent to {patient['name']} ({patient['phone']}).")
                        except Exception as e:
                            send_telegram(chat_id, f"Failed to send WhatsApp: {e}")

            # ===== Consent management =====
            elif text.startswith("/consent "):
                parts = text.split()
                if len(parts) >= 3:
                    pid = parts[1].strip().upper()
                    val = parts[2].strip().lower()
                    ok = set_consent(pid, val in ("yes", "y", "true", "1", "on"))
                    send_telegram(chat_id, "Consent updated." if ok else "Patient not found.")
                else:
                    send_telegram(chat_id, "Usage: /consent <patient_id> <yes|no>")

            elif text.startswith("/"):
                # Unknown command
                send_telegram(chat_id, f"❌ Unknown command: `{text}`\nTry /help for available commands")
            else:
                # Regular message
                send_telegram(chat_id, f"📨 You said: `{text}`\nType /help for commands")

        return jsonify({"ok": True}), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/')
def home():
    return "🏥 SmartElderCare Bot is running! Add /webhook to Telegram"

# ========== SETUP WEBHOOK ==========
def setup_webhook():
    """Set Telegram webhook URL"""
    webhook_url = os.getenv("WEBHOOK_URL") or "YOUR_SERVER_URL/webhook"
    url = f"https://api.telegram.org/bot{TOKEN}/setWebhook"

    response = requests.post(url, json={"url": webhook_url})

    if response.status_code == 200:
        print(f"✅ Webhook set: {webhook_url}")
    else:
        print(f"❌ Webhook failed: {response.text}")
        print("ℹ️ For testing, use polling instead")

# ========== LOCAL TESTING ==========
def test_polling():
    """Test bot without webhook (local)"""
    print("🤖 Testing bot with polling...")
    print("📱 Open Telegram and send /start to your bot")

    offset = 0
    while True:
        try:
            url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
            params = {"offset": offset, "timeout": 30}

            response = requests.get(url, params=params, timeout=35)

            if response.status_code == 200:
                updates = response.json()

                if updates.get("ok") and updates.get("result"):
                    for update in updates["result"]:
                        offset = update["update_id"] + 1

                        # Process message
                        if "message" in update:
                            msg = update["message"]
                            chat_id = msg["chat"]["id"]
                            text = msg.get("text", "").strip()
                            user_name = msg.get("from", {}).get("first_name", "User")

                            print(f"Processing: {text}")

                            # Handle command
                            if text == "/start":
                                handle_start(chat_id, user_name)
                            elif text == "/help":
                                handle_help(chat_id)
                            elif text == "/patients":
                                handle_patients(chat_id)
                            # Add more commands as needed

        except KeyboardInterrupt:
            print("\n👋 Stopping bot...")
            break
        except Exception as e:
            print(f"Error: {e}")

# ========== MAIN ==========
if __name__ == "__main__":
    print("🏥 SmartElderCare Bot - HK01 2025")
    print("="*50)

    # Check token
    if not TOKEN:
        print("❌ Please set TELEGRAM_TOKEN as an environment variable or in your .env file.")
        print("1. Get token from @BotFather")
        print("2. Run (PowerShell): $env:TELEGRAM_TOKEN='your_token_here'")
        TOKEN = input("Or enter token now: ").strip()

    # Test connection
    test_url = f"https://api.telegram.org/bot{TOKEN}/getMe"
    response = requests.get(test_url)

    if response.status_code == 200:
        bot_info = response.json()["result"]
        print(f"✅ Bot: @{bot_info['username']} ({bot_info['first_name']})")
        print(f"✅ ID: {bot_info['id']}")

        # Choose mode
        choice = input("\nChoose mode:\n1. Webhook (for deployment)\n2. Polling (local testing)\nEnter 1 or 2: ").strip()

        if choice == "1":
            # Set webhook for deployment
            setup_webhook()
            port = int(os.getenv("PORT", 5000))
            print(f"🚀 Starting server on port {port}")
            app.run(host="0.0.0.0", port=port, debug=True)
        else:
            # Local polling for testing
            test_polling()
    else:
        print("❌ Invalid token! Please check your token.")
