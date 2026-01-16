"""
MAIN STARTUP SCRIPT
Run this to start the medication management system (minimal package)
"""

import sys
from pathlib import Path

# Add code directory to path
code_dir = Path(__file__).parent / 'code'
sys.path.insert(0, str(code_dir))

# Check if required code files exist
required_files = [
    'elder_medication_system.py',
    'main.py',
    'yolov4_detector.py'
]

missing = [f for f in required_files if not (code_dir / f).exists()]
if missing:
    print("[ERROR] Missing files:")
    for f in missing:
        print(f"  - {f}")
    sys.exit(1)

print("[STARTING] Medication Management System (minimal)")
print("[PATH] Using code directory:", code_dir)


if __name__ == '__main__':
    try:
        from main import main
        main()
    except KeyboardInterrupt:
        print("\n[EXIT] Program terminated by user")
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
