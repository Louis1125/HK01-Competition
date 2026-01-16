import json
from pathlib import Path
from typing import Optional, Dict, Any

DATA_FILE = Path("patients.json")

DEFAULT_DATA = {
    "P001": {"name": "Chan Tai Man", "phone": "+85291234567", "consent": True},
    "P002": {"name": "Lee Siu Ming", "phone": "+85292345678", "consent": False},
    "P003": {"name": "Wong Mei Ling", "phone": "+85293456789", "consent": True},
}


def load_data() -> Dict[str, Dict[str, Any]]:
    if not DATA_FILE.exists():
        save_data(DEFAULT_DATA)
        return DEFAULT_DATA.copy()
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))


def save_data(data: Dict[str, Dict[str, Any]]):
    DATA_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def get_patient(pid: str) -> Optional[Dict[str, Any]]:
    data = load_data()
    return data.get(pid)


def set_consent(pid: str, consent: bool) -> bool:
    data = load_data()
    if pid not in data:
        return False
    data[pid]['consent'] = bool(consent)
    save_data(data)
    return True


def add_or_update_patient(pid: str, info: Dict[str, Any]):
    data = load_data()
    data[pid] = info
    save_data(data)
