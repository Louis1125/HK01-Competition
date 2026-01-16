import os
import requests

key = os.environ.get('TEXTMEBOT_APIKEY')
phone = os.environ.get('PATIENT_WHATSAPP')
message = os.environ.get('MESSAGE') or 'Test message from SmartElderCare'
if not key or not phone:
    print('Missing TEXTMEBOT_APIKEY or PATIENT_WHATSAPP env vars')
    raise SystemExit(1)

url = 'https://api.textmebot.com/send.php'
params = {'phone': phone, 'text': message, 'apikey': key}
print('Sending test to', phone)
print('Message:', message)
try:
    r = requests.get(url, params=params, timeout=15)
    print('HTTP', r.status_code, 'content-length:', len(r.content if r.content is not None else b''))
    body = r.text or ''
    print('Response preview:', repr(body[:1000]))
except Exception as e:
    print('Request failed:', e)
    raise
