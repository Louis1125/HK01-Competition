# Demo runner for telegram_whatsapp_bot in TEST_MODE
# This script simulates chat interactions for two chat IDs (English and Chinese)

import os, sys
root = r"d:\\Github python\\HK01(12.12.2025)(COMPETITION)"
sys.path.insert(0, root)
# ensure demo/test mode
os.environ['TEST_MODE'] = '1'
os.environ['TELEGRAM_TOKEN'] = 'DUMMY'

from telegram_whatsapp_bot import process_command
import user_prefs

print('--- Demo start ---')

eng_chat = 1001
zh_chat = 2002

# Ensure default prefs
print('Initial prefs:', user_prefs.get_lang(eng_chat), user_prefs.get_lang(zh_chat))

print('\n-- English user: set language to English (en)')
process_command(eng_chat, 'en', 'Alice')

print('\n-- English user: /commands')
process_command(eng_chat, '/commands', 'Alice')

print('\n-- English user: /start')
process_command(eng_chat, '/start', 'Alice')

print('\n-- English user: /patients')
process_command(eng_chat, '/patients', 'Alice')

print('\n-- English user: /whatsapp P001 Hello from demo')
process_command(eng_chat, '/whatsapp P001 Hello from demo', 'Alice')

print('\n-- English user: /test_whatsapp')
process_command(eng_chat, '/test_whatsapp', 'Alice')

print('\n-- English user: /consent P002 yes')
process_command(eng_chat, '/consent P002 yes', 'Alice')

print('\n-- Chinese user: set language to Chinese (zh)')
process_command(zh_chat, 'zh', '王小明')

print('\n-- Chinese user: /commands')
process_command(zh_chat, '/commands', '王小明')

print('\n-- Chinese user: 傳送 WhatsApp P001 測試訊息')
process_command(zh_chat, 'whatsapp P001 測試訊息', '王小明')

print('\nFinal prefs file contents (user_prefs.json):')
try:
    import json
    print(json.dumps(__import__('pathlib').Path('user_prefs.json').read_text(encoding='utf-8'), indent=2, ensure_ascii=False))
except Exception as e:
    print('Could not read user_prefs.json:', e)

print('\n--- Demo end ---')
