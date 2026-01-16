"""
1-minute demonstration script (prototype) — (1-min demon).py

This script runs a short, self-contained prototype sequence that demonstrates:
 - Camera identification (simulated)
 - Medication reminder flow (simulated notification)
 - Emergency alert (panic) flow (simulated)

It does not modify the main programme and is safe to run without external credentials.
It records a small JSON timeline under `demo_recordings/` which you can use to assemble
a short 1-minute demo video (record your screen while the script runs).

Usage:
    python "(1-min demon).py"

Note: this script imports the main programme module in a non-invasive way and stubs a
minimal manager for demonstration to avoid touching your live database.
"""

import importlib.util
import sys
import time
import json
import os
from pathlib import Path

ROOT = Path(__file__).parent.resolve()
MAIN_FILE = ROOT / 'HK01 Competition 12-12-2025 main programme.py'
OUT_DIR = ROOT / 'demo_recordings'
OUT_DIR.mkdir(exist_ok=True)

# Load the main programme module without running its CLI main(). This lets us reuse helpers.
spec = importlib.util.spec_from_file_location('main_programme', str(MAIN_FILE))
main_prog = importlib.util.module_from_spec(spec)
loader = spec.loader
sys.path.insert(0, str(ROOT))
if loader is None:
    raise RuntimeError('Could not load main programme module')
loader.exec_module(main_prog)

# Minimal manager stub used only for demo - avoids DB dependencies
class DemoManager:
    def get_elder(self, elder_id):
        return {'elder_id': elder_id, 'name': 'Robert Brown', 'phone': '+10000000001', 'emergency_contact': '+10000000001'}
    def get_medications(self, elder_id):
        return [{'med_id': 1, 'name': 'Aspirin', 'dosage': '100mg', 'photo': None}]
    def get_schedules(self, elder_id=None):
        return [{'schedule_id': 1, 'time': '09:00', 'frequency': 'daily'}]
    def get_medication_photo(self, med_id):
        return None

# Attach the demo manager to the loaded module for helpers to use
main_prog.manager = DemoManager()

def now_ts():
    return time.strftime('%Y-%m-%d %H:%M:%S')

timeline = []

def record(event, details=None):
    entry = {'ts': now_ts(), 'event': event, 'details': details}
    timeline.append(entry)
    print('[DEMO]', entry['ts'], event, '-' , details or '')

# 1) Simulate camera identification sequence
record('demo_start', 'Starting 1-minute demo sequence')
record('camera_start', 'Simulated camera warm-up')

# Populate recent identifications (simulate several frames identifying same person)
now = time.time()
for i in range(5):
    sample = {'person_id': 1, 'name': 'Robert Brown', 'label': 'Robert Brown', 'confidence': 0.85 - i*0.05, 'ts': now - (5-i)}
    try:
        with main_prog.RECENT_IDENTIFICATIONS_LOCK:
            main_prog.RECENT_IDENTIFICATIONS.append(sample)
            # keep recent buffer trimmed
            main_prog.RECENT_IDENTIFICATIONS[:] = main_prog.RECENT_IDENTIFICATIONS[-main_prog.RECENT_MAX:]
    except Exception:
        # Fallback if lock not present
        main_prog.RECENT_IDENTIFICATIONS.append(sample)
    record('camera_frame', {'frame': i+1, 'identified': sample['name'], 'confidence': sample['confidence']})
    time.sleep(0.15)

record('camera_stop', 'Stopping camera and summarizing')
best = main_prog.summarize_recent_identifications(max_entries=5, max_age=main_prog.SUMMARY_MAX_AGE_SECONDS)
record('identification_summary', best)

# 2) Simulate medication reminder flow
record('reminder_trigger', 'Medication due for Robert Brown (Aspirin)')
meds = main_prog.manager.get_medications(1)
med_name = meds[0]['name'] if meds else 'Unknown'
# Use the existing notification helpers (will be no-ops if not configured)
title = 'Reminder: {}'.format(med_name)
body = '{} is due now.'.format(main_prog.manager.get_elder(1)['name'])
main_prog.send_fcm_notification(title, body)
main_prog.send_whatsapp_message(body, phone=main_prog.manager.get_elder(1).get('phone'))
record('reminder_sent', {'title': title, 'body': body})

# Optional: if a medication photo exists and OpenCV is available, show it briefly
photo = main_prog.manager.get_medication_photo(1) if hasattr(main_prog.manager, 'get_medication_photo') else None
if photo and os.path.exists(photo) and getattr(main_prog, '_cv2', None) is not None:
    try:
        img = main_prog._cv2.imread(photo)
        main_prog._cv2.imshow('Medication', img)
        main_prog._cv2.waitKey(2000)
        main_prog._cv2.destroyAllWindows()
        record('photo_shown', photo)
    except Exception as e:
        record('photo_show_failed', str(e))

# 3) Simulate fall detection -> emergency alert
record('fall_simulation', 'Simulating fall detected by camera')
# Use the panic helper - runs notifications in blocking mode here for demo
ok = main_prog.send_panic_alert(elder_id=1, note='demo: simulated fall')
record('panic_sent', {'result': ok})

# Save timeline to disk for later assembly into a demo video
out_file = OUT_DIR / ('demo_run_{}.json'.format(int(time.time())))
with open(out_file, 'w', encoding='utf-8') as f:
    json.dump(timeline, f, indent=2, ensure_ascii=False)

record('demo_end', 'Demo finished; timeline written to {}'.format(str(out_file)))

print('\nDemo complete. To make a 1-minute video:')
print(' - Run this script while recording your screen (e.g., with OBS).')
print(' - Alternatively, use the generated JSON in `demo_recordings/` to overlay captions on a recorded screen capture.')
print('\nRun: python "(1-min demon).py"')
