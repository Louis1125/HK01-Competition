# Test calling send_panic_alert with manager = None
import os, sys
from importlib.machinery import SourceFileLoader

root = r"d:\\Github python\\HK01(12.12.2025)(COMPETITION)"
sys.path.insert(0, root)
os.environ['TEST_MODE'] = '1'
module_path = r"d:\\Github python\\HK01(12.12.2025)(COMPETITION)\\HK01 Competition 12-12-2025 main programme.py"
loader = SourceFileLoader('hk_main', module_path)
mod = loader.load_module()

# Ensure manager missing
if 'manager' in mod.__dict__:
    del mod.__dict__['manager']

print('Calling send_panic_alert() with manager missing...')
ok = mod.send_panic_alert(elder_id=1, note='test no manager')
print('send_panic_alert returned:', ok)
import time
time.sleep(1)
print('Done.')
