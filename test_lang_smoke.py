import os, sys, traceback
root = r"d:\\Github python\\HK01(12.12.2025)(COMPETITION)"
# avoid real network calls; set a dummy token so import-time prompt is skipped
os.environ['TELEGRAM_TOKEN'] = 'DUMMY_TOKEN'
# run in demo/test mode so no external HTTP calls happen
os.environ['TEST_MODE'] = '1'
# ensure project dir importable
sys.path.insert(0, root)

try:
    import importlib
    mod = importlib.import_module('telegram_whatsapp_bot')
    import user_prefs
    chat = 999999
    print('initial lang for', chat, '->', user_prefs.get_lang(chat))
    print('\n--- send language set: "en" ---')
    mod.process_command(chat, 'en', 'Tester')
    print('lang now ->', user_prefs.get_lang(chat))
    print('\n--- /commands (should show English) ---')
    mod.process_command(chat, '/commands', 'Tester')
    print('\n--- /start (English) ---')
    mod.process_command(chat, '/start', 'Tester')
    print('\n--- send language set: "zh" ---')
    mod.process_command(chat, 'zh', 'Tester')
    print('lang now ->', user_prefs.get_lang(chat))
    print('\n--- /commands (should show Chinese) ---')
    mod.process_command(chat, '/commands', 'Tester')
    print('\nSmoke test completed without crashing.')
except Exception:
    traceback.print_exc()
