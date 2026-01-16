"""
Simple test script to verify Telegram bot token and chat id can receive messages.
Set the environment variables `TELEGRAM_TOKEN` and `TELEGRAM_CHAT_ID` before running.
This script prints full Telegram response on error to help diagnose 400/401 issues.
"""
import os
import requests
import json

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

if not TELEGRAM_TOKEN:
    print('Please set TELEGRAM_TOKEN environment variable (Bot token from BotFather)')
    raise SystemExit(1)
if not CHAT_ID:
    print('Please set TELEGRAM_CHAT_ID environment variable (your numeric chat id or @username)')
    raise SystemExit(1)

# sanitize token: remove surrounding quotes/spaces if accidentally pasted
TELEGRAM_TOKEN = TELEGRAM_TOKEN.strip().strip('"').strip("'")
api_url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}'

def get_me():
    r = requests.get(api_url + '/getMe', timeout=8)
    try:
        r.raise_for_status()
    except Exception:
        print('getMe failed:', r.status_code, r.text)
        return None
    return r.json()

print('Calling getMe to validate token...')
me = get_me()
if not me:
    print('Token appears invalid or network issue. Check token and connectivity.')
    raise SystemExit(1)
print('Bot info:', json.dumps(me, indent=2, ensure_ascii=False))

msg = os.getenv('TEST_MESSAGE', 'Test message from send_telegram_test')
payload = {'chat_id': CHAT_ID, 'text': msg}
print('Sending test message to', CHAT_ID)
resp = requests.post(api_url + '/sendMessage', json=payload, timeout=8)
if resp.status_code != 200:
    print('sendMessage failed:', resp.status_code)
    try:
        print(resp.json())
    except Exception:
        print(resp.text)
else:
    print('sendMessage OK:', resp.json())
