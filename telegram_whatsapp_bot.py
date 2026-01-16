import os
import requests
import json
from flask import Flask, request, jsonify
from datetime import datetime

# Local helpers
from whatsapp_provider import send_whatsapp_text
from patient_manager import get_patient, set_consent
import user_prefs

app = Flask(__name__)

# Read token from environment (do NOT hardcode secrets in files)
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

if not TELEGRAM_TOKEN:
    # Allow running interactively: prompt for token but still avoid saving it
    try:
        TELEGRAM_TOKEN = input('Enter TELEGRAM_TOKEN (will not be saved): ').strip()
    except Exception:
        TELEGRAM_TOKEN = None

TELEGRAM_API_URL = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}' if TELEGRAM_TOKEN else None


def send_telegram(chat_id, text, parse_mode='Markdown'):
    # Test mode: print to console instead of calling Telegram API
    if os.environ.get('TEST_MODE', '').strip().lower() in ('1', 'true', 'yes'):
        print(f"[TEST MODE] Telegram -> {chat_id}: {text}")
        return True

    if not TELEGRAM_API_URL:
        print('Telegram token not configured; cannot send message')
        return False
    url = TELEGRAM_API_URL + '/sendMessage'
    payload = {'chat_id': chat_id, 'text': text, 'parse_mode': parse_mode, 'disable_web_page_preview': True}
    try:
        r = requests.post(url, json=payload, timeout=8)
        # Provide richer error logging for HTTP errors so users can see Telegram response body
        try:
            r.raise_for_status()
            return True
        except requests.exceptions.HTTPError as http_err:
            # Try to show response content (may contain JSON with description)
            body = None
            try:
                body = r.json()
            except Exception:
                body = r.text
            print(f'Failed to send telegram message: {r.status_code} {r.reason} - {body}')
            # Persist error detail for offline inspection
            try:
                import pathlib
                p = pathlib.Path('logs')
                p.mkdir(exist_ok=True)
                logf = p / 'telegram_errors.log'
                with open(logf, 'a', encoding='utf-8') as fh:
                    import datetime
                    fh.write('---\n')
                    fh.write(datetime.datetime.utcnow().isoformat() + 'Z\n')
                    fh.write('chat_id: ' + str(chat_id) + '\n')
                    fh.write('payload: ' + str(payload) + '\n')
                    fh.write('response_status: ' + str(r.status_code) + '\n')
                    fh.write('response_body: ' + str(body) + '\n')
            except Exception:
                pass
            return False
    except Exception as e:
        print('Failed to send telegram message (network/error):', e)
        return False


def process_command(chat_id: int, text: str, user: str):
    """Language-aware command processor. Accepts commands with or without leading '/'."""
    if not text:
        send_telegram(chat_id, 'No text found in message')
        return

    # allow users to set language quickly by typing 'en' or 'zh'
    low = text.strip().lower()
    if low in ('en', 'english', '1'):
        user_prefs.set_lang(chat_id, 'en')
        send_telegram(chat_id, 'Language set to English. Type /commands to see available commands.')
        return
    if low in ('zh', 'zh-tw', '中文', '繁體', '2'):
        user_prefs.set_lang(chat_id, 'zh')
        send_telegram(chat_id, '語言已設為繁體中文。輸入 /commands 查看可用指令。')
        return

    lang = user_prefs.get_lang(chat_id)
    # normalize command: remove leading '/', take first token, strip any @botname suffix
    raw_cmd = text.lstrip('/').split()[0]
    cmd = raw_cmd.split('@')[0].lower()

    # debug printing to help diagnose why some commands may not be recognized
    if os.environ.get('TEST_MODE', '').strip().lower() in ('1', 'true', 'yes') or os.environ.get('DEBUG', '').strip().lower() in ('1', 'true', 'yes'):
        print(f"[DEBUG] chat={chat_id} user={user} raw_text={repr(text)} normalized_cmd={cmd} lang={lang}")

    # Localized responses
    if cmd in ('start',):
        if lang == 'zh':
            send_telegram(chat_id, f'🏥 SmartElderCare 機器人\n嗨 {user}！輸入 /commands 查看指令')
        else:
            send_telegram(chat_id, f'🏥 SmartElderCare Bot\nHello {user}! Type /commands for commands')
        return

    if cmd in ('help', 'commands'):
        if lang == 'zh':
            # Short Chinese command list (23-44 as requested elsewhere)
            send_telegram(chat_id, (
                '可用指令（繁體中文）示例：\n'
                '23. 開始 (start)\n'
                '24. 幫助 (help)\n'
                '25. 列出病人 (patients)\n'
                '26. 傳送 WhatsApp (whatsapp <id> <訊息>)\n'
                '27. 測試 WhatsApp (test_whatsapp)\n'
                '28. 同意設定 (consent <id> <yes|no>)\n'
                '\n輸入英文指令也會被接受，但顯示以您選擇的語言為主。'
            ))
        else:
            send_telegram(chat_id, (
                'Available commands (English) example:\n'
                '1. start\n'
                '2. help\n'
                '3. patients\n'
                '4. whatsapp <id> <message>\n'
                '5. test_whatsapp\n'
                '6. consent <id> <yes|no>\n'
                '\nYou can type "en" or "zh" to switch language.'
            ))
        return

    # Core command implementations
    if cmd == 'patients' or (lang == 'zh' and cmd in ('列出病人', '病人')):
        p = get_patient('P001')
        send_telegram(chat_id, f"P001: {p.get('name')} - {p.get('phone')} - consent={p.get('consent')}")
        return

    if cmd == 'whatsapp' or (lang == 'zh' and cmd in ('whatsapp', '傳送')):
        parts = text.split(' ', 2)
        if len(parts) < 3:
            send_telegram(chat_id, 'Usage: /whatsapp <patient_id> <message>')
            return
        pid = parts[1].strip().upper()
        body = parts[2].strip()
        patient = get_patient(pid)
        if not patient:
            send_telegram(chat_id, f'Unknown patient id: {pid}')
            return
        if not patient.get('consent', False):
            send_telegram(chat_id, f'Patient {pid} has not consented to WhatsApp messages.')
            return
        try:
            resp = send_whatsapp_text(patient['phone'], body)
            send_telegram(chat_id, f'WhatsApp sent to {patient["name"]} ({patient["phone"]}).')
        except Exception as e:
            send_telegram(chat_id, f'Failed to send WhatsApp: {e}')
        return

    if cmd == 'test_whatsapp' or (lang == 'zh' and cmd in ('test_whatsapp', '測試')):
        pid = 'P001'
        patient = get_patient(pid)
        if not patient:
            send_telegram(chat_id, 'Test patient P001 not found')
            return
        if not patient.get('consent', False):
            send_telegram(chat_id, 'P001 has not consented to WhatsApp messages')
            return
        try:
            now = datetime.utcnow().isoformat()
            test_msg = f'Test message from SmartElderCare at {now} UTC'
            resp = send_whatsapp_text(patient['phone'], test_msg)
            s = json.dumps(resp, ensure_ascii=False)
            if len(s) > 800:
                s = s[:800] + '...'
            send_telegram(chat_id, f'Test send OK. Provider response:\n{s}')
        except Exception as e:
            send_telegram(chat_id, f'Test send failed: {e}')
        return

    if cmd == 'consent' or (lang == 'zh' and cmd in ('consent', '同意')):
        parts = text.split()
        if len(parts) >= 3:
            pid = parts[1].strip().upper()
            val = parts[2].strip().lower()
            ok = set_consent(pid, val in ('yes', 'y', 'true', '1', 'on'))
            if lang == 'zh':
                send_telegram(chat_id, '同意已更新。' if ok else '找不到病人。')
            else:
                send_telegram(chat_id, 'Consent updated.' if ok else 'Patient not found.')
        else:
            if lang == 'zh':
                send_telegram(chat_id, '用法: /consent <patient_id> <yes|no>')
            else:
                send_telegram(chat_id, 'Usage: /consent <patient_id> <yes|no>')
        return

    # Fallback
    if lang == 'zh':
        send_telegram(chat_id, '無法理解您的指令。輸入 /commands 查看可用指令。')
    else:
        send_telegram(chat_id, "I didn't understand that. Try /commands")


@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if not data:
        return jsonify({'ok': False, 'error': 'no json'}), 400
    # Basic Telegram update handling
    msg = data.get('message') or data.get('edited_message')
    if not msg:
        return jsonify({'ok': True})

    chat_id = msg['chat']['id']
    text = msg.get('text', '').strip()
    user = msg.get('from', {}).get('first_name', 'User')

    if not text:
        send_telegram(chat_id, 'No text found in message')
        return jsonify({'ok': True})
    # Delegate to language-aware processor
    process_command(chat_id, text, user)

    return jsonify({'ok': True})


@app.route('/')
def home():
    return 'SmartElderCare Telegram→WhatsApp bridge'


def setup_webhook():
    webhook_url = os.getenv('WEBHOOK_URL')
    if not webhook_url or not TELEGRAM_TOKEN:
        print('Set WEBHOOK_URL and TELEGRAM_TOKEN in environment to use webhook mode')
        return
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/setWebhook'
    resp = requests.post(url, json={'url': webhook_url})
    print('setWebhook response:', resp.status_code, resp.text)


if __name__ == '__main__':
    # Quick CLI to run in polling or webhook mode
    if not TELEGRAM_TOKEN:
        print('TELEGRAM_TOKEN not configured. Exiting.')
        raise SystemExit(1)

    print('SmartElderCare Telegram→WhatsApp bridge')
    choice = input('Choose mode: 1=webhook, 2=polling > ').strip()
    if choice == '1':
        setup_webhook()
        port = int(os.getenv('PORT', '5000'))
        app.run(host='0.0.0.0', port=port)
    else:
        # Polling loop
        offset = 0
        print('Starting polling loop. Press Ctrl-C to stop.')
        while True:
            try:
                url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates'
                r = requests.get(url, params={'offset': offset, 'timeout': 30}, timeout=35)
                if r.status_code == 200:
                    data = r.json()
                    for update in data.get('result', []):
                        offset = update['update_id'] + 1
                        if 'message' in update:
                            msg = update['message']
                            chat_id = msg['chat']['id']
                            text = msg.get('text', '').strip()
                            user = msg.get('from', {}).get('first_name', 'User')
                            process_command(chat_id, text, user)
                else:
                    print('getUpdates returned', r.status_code, r.text)
            except KeyboardInterrupt:
                print('\nStopping polling loop')
                break
            except Exception as e:
                print('Polling error:', e)
                import time
                time.sleep(2)
