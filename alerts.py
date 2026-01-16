import os
import json
from typing import List, Optional

from patient_manager import load_data, get_patient
from whatsapp_provider import send_whatsapp_text

TEST_MODE = os.environ.get('TEST_MODE', '').strip().lower() in ('1', 'true', 'yes')


def send_alert_to_patients(message: str, patient_ids: Optional[List[str]] = None) -> dict:
    """Send `message` to all consenting patients or a subset by `patient_ids`.

    Returns a report dict with results per patient id.
    """
    data = load_data()
    report = {'sent': [], 'skipped': [], 'failed': {}}

    # Filter patient list
    for pid, info in data.items():
        pid_u = pid.upper()
        if patient_ids and pid_u not in [p.upper() for p in patient_ids]:
            continue
        consent = info.get('consent', False)
        phone = info.get('phone')
        name = info.get('name', pid)
        if not consent:
            report['skipped'].append({'id': pid_u, 'reason': 'no_consent'})
            continue
        if not phone:
            report['failed'][pid_u] = 'no_phone'
            continue
        try:
            resp = send_whatsapp_text(phone, message)
            report['sent'].append({'id': pid_u, 'phone': phone, 'resp': resp})
        except Exception as e:
            report['failed'][pid_u] = str(e)

    return report


def pretty_report(report: dict) -> str:
    parts = []
    parts.append(f"Sent: {len(report.get('sent', []))}")
    parts.append(f"Skipped: {len(report.get('skipped', []))}")
    parts.append(f"Failed: {len(report.get('failed', {}))}")
    return '\n'.join(parts)
