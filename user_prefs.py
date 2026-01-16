import json
from pathlib import Path
from typing import Dict

PREF_FILE = Path('user_prefs.json')

DEFAULT_PREFS: Dict[str, Dict[str, str]] = {}

def load_prefs() -> Dict[str, Dict[str, str]]:
    if not PREF_FILE.exists():
        save_prefs(DEFAULT_PREFS)
        return DEFAULT_PREFS.copy()
    try:
        return json.loads(PREF_FILE.read_text(encoding='utf-8'))
    except Exception:
        return {}

def save_prefs(prefs: Dict[str, Dict[str, str]]):
    PREF_FILE.write_text(json.dumps(prefs, indent=2, ensure_ascii=False), encoding='utf-8')

def get_lang(chat_id: int) -> str:
    prefs = load_prefs()
    entry = prefs.get(str(chat_id), {})
    return entry.get('lang', 'en')

def set_lang(chat_id: int, lang: str) -> bool:
    lang = (lang or 'en').strip().lower()
    if lang not in ('en', 'zh'):
        return False
    prefs = load_prefs()
    prefs.setdefault(str(chat_id), {})['lang'] = lang
    save_prefs(prefs)
    return True
