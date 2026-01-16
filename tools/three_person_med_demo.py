"""
Three-person medication demo

This script creates a small in-memory demo of three elders, their medications and schedules,
then simulates reminders and missed-dose checks. It is safe to run and does not modify the
real database. Output is printed to the console and a timeline JSON is saved to demo_recordings/.

Run:
    python tools/three_person_med_demo.py

"""
import importlib.util
import sys
import time
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAIN_FILE = ROOT / 'HK01 Competition 12-12-2025 main programme.py'
OUT_DIR = ROOT / 'demo_recordings'
OUT_DIR.mkdir(exist_ok=True)

# load main module without running main()
spec = importlib.util.spec_from_file_location('main_programme', str(MAIN_FILE))
main_prog = importlib.util.module_from_spec(spec)
loader = spec.loader
sys.path.insert(0, str(ROOT))
loader.exec_module(main_prog)

# Demo data for three elders
ELDERS = [
    {'elder_id': 1, 'name': 'Mr. Chan', 'phone': '+85260000001', 'external_id': 'HK0001', 'emergency_contact': '+85290000001'},
    {'elder_id': 2, 'name': 'Mrs. Lee', 'phone': '+85260000002', 'external_id': 'HK0002', 'emergency_contact': '+85290000002'},
    {'elder_id': 3, 'name': 'Mr. Ho', 'phone': '+85260000003', 'external_id': 'HK0003', 'emergency_contact': '+85290000003'},
]

MEDS = [
    {'med_id': 1, 'elder_id': 1, 'name': 'Aspirin', 'dosage': '100mg', 'reason': 'Hypertension'},
    {'med_id': 2, 'elder_id': 2, 'name': 'Metformin', 'dosage': '500mg', 'reason': 'Diabetes'},
    {'med_id': 3, 'elder_id': 3, 'name': 'Atorvastatin', 'dosage': '20mg', 'reason': 'Cholesterol'},
]

SCHEDULES = [
    {'schedule_id': 1, 'med_id': 1, 'time': '09:00'},
    {'schedule_id': 2, 'med_id': 2, 'time': '09:30'},
    {'schedule_id': 3, 'med_id': 3, 'time': '10:00'},
]

# Minimal in-memory manager used only for demo
class DemoManager:
    def __init__(self, elders, meds, schedules):
        self._elders = {e['elder_id']: e for e in elders}
        self._meds = {m['med_id']: m for m in meds}
        self._schedules = schedules
    def get_elder(self, elder_id):
        return self._elders.get(elder_id)
    def get_all_elders(self):
        return list(self._elders.values())
    def get_medications(self, elder_id):
        return [m for m in self._meds.values() if m['elder_id'] == elder_id]
    def get_schedules(self, elder_id=None):
        if elder_id is None:
            return self._schedules
        meds = self.get_medications(elder_id)
        med_ids = {m['med_id'] for m in meds}
        return [s for s in self._schedules if s['med_id'] in med_ids]
    def get_medication_photo(self, med_id):
        return None

# attach demo manager to main module so helpers like send_panic_alert can use it
demo_mgr = DemoManager(ELDERS, MEDS, SCHEDULES)
main_prog.manager = demo_mgr

# helper timeline
timeline = []

def now_ts():
    return time.strftime('%Y-%m-%d %H:%M:%S')

def rec(event, details=None):
    entry = {'ts': now_ts(), 'event': event, 'details': details}
    timeline.append(entry)
    print('[DEMO]', entry['ts'], event, '-', details or '')

# 1) Show all three people's meds and schedules
rec('demo_start', 'Three-person medication demo starting')
for elder in demo_mgr.get_all_elders():
    rec('elder_info', {'elder': elder})
    meds = demo_mgr.get_medications(elder['elder_id'])
    rec('meds_list', {'elder_id': elder['elder_id'], 'meds': meds})
    scheds = demo_mgr.get_schedules(elder['elder_id'])
    rec('schedules_list', {'elder_id': elder['elder_id'], 'schedules': scheds})

# 2) Simulate reminders for each schedule in short succession (fast demo)
rec('reminder_phase_start', 'Simulating reminders for each elder')
for s in SCHEDULES:
    med = next((m for m in MEDS if m['med_id'] == s['med_id']), None)
    if not med:
        continue
    elder = demo_mgr.get_elder(med['elder_id'])
    title = 'Reminder: {}'.format(med['name'])
    body = '{}: {} ({}) due at {}'.format(elder['name'], med['name'], med['dosage'], s['time'])
    # use existing helpers (they will log or no-op if not configured)
    try:
        main_prog.send_fcm_notification(title, body)
    except Exception:
        pass
    try:
        main_prog.send_whatsapp_message(body, phone=elder.get('phone'))
    except Exception:
        pass
    rec('reminder_sent', {'elder': elder['name'], 'med': med['name'], 'time': s['time']})
    time.sleep(0.4)

# 3) Simulate one missed dose: elder 2 misses medication
rec('missed_dose_detected', {'elder': demo_mgr.get_elder(2)['name'], 'med': 'Metformin'})
try:
    main_prog.send_whatsapp_message('Missed dose: Metformin for {}'.format(demo_mgr.get_elder(2)['name']), phone=demo_mgr.get_elder(2)['phone'])
except Exception:
    pass

# 4) Simulate manual confirm/lookup using last-4 digits for elder 1
last4 = demo_mgr.get_elder(1)['phone'][-4:]
rec('manual_verify', {'elder': demo_mgr.get_elder(1)['name'], 'last4': last4})
# show meds for elder1
rec('showmeds', {'elder': demo_mgr.get_elder(1)['name'], 'meds': demo_mgr.get_medications(1)})

# 5) Save timeline
fname = OUT_DIR / ('three_person_med_demo_{}.json'.format(int(time.time())))
with open(fname, 'w', encoding='utf-8') as f:
    json.dump(timeline, f, indent=2, ensure_ascii=False)
rec('demo_end', 'Demo finished; timeline saved to {}'.format(str(fname)))

print('\nDemo complete. Timeline saved to: {}'.format(str(fname)))
print('You can record your screen while running this script for a short demo.')
