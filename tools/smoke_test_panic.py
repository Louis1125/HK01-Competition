# Smoke test for panic alert and fall-detection hook
# Loads the main programme module via importlib, injects a stub DETECTOR and manager,
# and calls send_panic_alert to ensure it runs without raising exceptions.
import importlib.util
import sys
from pathlib import Path
import time

MAIN_PATH = Path(r"d:/Github python/HK01(12.12.2025)(COMPETITION)/HK01 Competition 12-12-2025 main programme.py")
spec = importlib.util.spec_from_file_location("main_programme", str(MAIN_PATH))
module = importlib.util.module_from_spec(spec)
loader = spec.loader
assert loader is not None
# Ensure the project root is on sys.path so local imports succeed
sys.path.insert(0, str(MAIN_PATH.parent))
loader.exec_module(module)

# Inject a simple manager stub with get_elder
class ManagerStub:
    def get_elder(self, elder_id):
        return {
            'elder_id': elder_id,
            'name': 'Test Elder',
            'phone': None,
            'emergency_contact': '+10000000000'
        }

module.manager = ManagerStub()
# Ensure notifications are disabled (so the test doesn't call external APIs)
module.WHATSAPP_API_URL = None
module.WHATSAPP_TOKEN = None
module.WHATSAPP_PHONE_NUMBER = None
module.FCM_SERVER_KEY = None

print('Calling send_panic_alert directly...')
ok = module.send_panic_alert(elder_id=1, note='smoke test')
print('send_panic_alert returned:', ok)

# Test calling a stubbed detector detect_fall and triggering the background path
class DetectorStub:
    def detect_fall(self, path):
        print('DetectorStub.detect_fall called with', path)
        return True

module.DETECTOR = DetectorStub()
module.identified = [{'person_id': 1}]
module.LAST_IDENTIFIED = 1

print('Simulating fall hook: dispatching background alert thread...')
import threading
try:
    threading.Thread(target=module.send_panic_alert, args=(1, 'fall-detection-smoke'), daemon=True).start()
    print('Background thread started')
except Exception as e:
    print('Failed to start background thread:', e)

print('Smoke test complete')
