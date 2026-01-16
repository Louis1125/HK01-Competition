# Demo script that simulates an issue and sends alerts to patients using alerts.py
import os, sys
root = r"d:\\Github python\\HK01(12.12.2025)(COMPETITION)"
sys.path.insert(0, root)

# enable TEST_MODE for safe demo
os.environ['TEST_MODE'] = '1'

from alerts import send_alert_to_patients, pretty_report

if __name__ == '__main__':
    issue = {
        'type': 'FALL_DETECTED',
        'timestamp': '2026-01-10T06:00:00Z',
        'details': 'Motion sensor indicated a possible fall in room 201.'
    }

    msg = f"ALERT: {issue['type']} at {issue['timestamp']} - {issue['details']}"
    print('Triggering alert with message:\n', msg)
    report = send_alert_to_patients(msg)
    print('\nReport summary:')
    print(pretty_report(report))
    print('\nFull report JSON:')
    import json
    print(json.dumps(report, ensure_ascii=False, indent=2))
