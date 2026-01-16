# Test script: load main programme module, inject fake manager, call send_panic_alert
import os, sys
from importlib.machinery import SourceFileLoader

root = r"d:\\Github python\\HK01(12.12.2025)(COMPETITION)"
sys.path.insert(0, root)
# Run in TEST_MODE to avoid real HTTP calls
os.environ['TEST_MODE'] = '1'

module_path = r"d:\\Github python\\HK01(12.12.2025)(COMPETITION)\\HK01 Competition 12-12-2025 main programme.py"
loader = SourceFileLoader('hk_main', module_path)
mod = loader.load_module()

# Inject a fake manager object into module globals
class FakeManager:
    def get_elder(self, elder_id):
        return {'name': 'Test Elder', 'phone': '+85291234567', 'emergency_contact': '+85291234567'}
    def get_elder_by_name(self, name):
        return {'name': name, 'phone': '+85291234567'}

mod.manager = FakeManager()

print('Calling send_panic_alert()...')
ok = mod.send_panic_alert(elder_id=1, note='test run')
print('send_panic_alert returned:', ok)

# Wait a moment to allow background alerts thread (if any) to print
import time
time.sleep(1)
print('Done.')
