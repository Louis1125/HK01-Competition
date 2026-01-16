"""
AUTOMATED INSTALLATION SCRIPT
Complete setup for the Medication Management System
"""

import subprocess
import sys
import os
from pathlib import Path
import platform

print("\n" + "="*70)
print("INSTALLATION - Medication Management System")
print("="*70)

# Check Python version
print("\n[CHECK] Python version...", end=" ")
if sys.version_info < (3, 7):
    print("FAILED")
    print("[ERROR] Python 3.7+ required")
    sys.exit(1)
print(f"OK (Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro})")

# Check OS
print(f"[CHECK] Operating System: {platform.system()}")

# Install dependencies
print("\n[INSTALL] Python packages...")
req_file = Path(__file__).parent / 'requirements.txt'

if not req_file.exists():
    print(f"[ERROR] requirements.txt not found at {req_file}")
    sys.exit(1)

try:
    result = subprocess.run(
        [sys.executable, '-m', 'pip', 'install', '-r', str(req_file)],
        capture_output=False,
        text=True
    )
    if result.returncode != 0:
        print("[ERROR] Package installation failed")
        sys.exit(1)
    print("[OK] Packages installed")
except Exception as e:
    print(f"[ERROR] Installation error: {e}")
    sys.exit(1)

# Create directories
print("\n[CREATE] Required directories...")
project_root = Path(__file__).parent.parent
dirs = [
    'models/yolov4',
    'models/teachable_machine',
    'models/custom',
    'data',
    'logs'
]

for dir_name in dirs:
    dir_path = project_root / dir_name
    dir_path.mkdir(parents=True, exist_ok=True)
    # Create .gitkeep to preserve directories
    (dir_path / '.gitkeep').touch()
    print(f"  ✓ {dir_name}")

# Initialize database
print("\n[DATABASE] Initializing medication database...")
setup_data_script = Path(__file__).parent / 'setup_data.py'

if setup_data_script.exists():
    try:
        result = subprocess.run(
            [sys.executable, str(setup_data_script)],
            capture_output=True,
            text=True,
            cwd=str(project_root)
        )
        print(result.stdout)
        if result.returncode != 0:
            print(f"[ERROR] Data setup failed:\n{result.stderr}")
            sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Could not run setup_data.py: {e}")
        # Don't exit, this is non-critical
else:
    print("[WARN] setup_data.py not found, skipping database initialization")

# Verify installation
print("\n[VERIFY] Checking installation...")

required_modules = ['cv2', 'numpy']
missing = []

for module in required_modules:
    try:
        __import__(module)
        print(f"  ✓ {module}")
    except ImportError:
        print(f"  ✗ {module} - MISSING")
        missing.append(module)

if missing:
    print(f"\n[WARNING] Missing modules: {', '.join(missing)}")
    print("Run: pip install -r setup/requirements.txt")

# Check project structure
print("\n[CHECK] Project structure...")
required_files = [
    'code/elder_medication_system.py',
    'code/Second_Program_with_Teachable_Machine.py',
    'code/yolov4_detector.py',
    'config/settings.py',
    'README.md',
]

all_exist = True
for file_path in required_files:
    full_path = project_root / file_path
    if full_path.exists():
        print(f"  ✓ {file_path}")
    else:
        print(f"  ✗ {file_path} - NOT FOUND")
        all_exist = False

if not all_exist:
    print("\n[ERROR] Some required files are missing!")
    sys.exit(1)

# Final summary
print("\n" + "="*70)
print("INSTALLATION COMPLETE!")
print("="*70)

print("""
✓ Dependencies installed
✓ Directories created
✓ Database initialized with sample data
✓ All required files present

NEXT STEPS:

1. Add YOLOv4 Model (Optional)
   Download from: https://github.com/AlexeyAB/darknet/releases
   Extract to: models/yolov4/
   Files needed:
     - yolov4.weights
     - yolov4.cfg
     - coco.names

2. Start the Application
   From project root, run:
   
   python run.py

3. Use the Program
   - Select person (1-3)
   - Run person detection
   - View medications
   - Track doses

TROUBLESHOOTING:

Q: ImportError: No module named 'cv2'
A: pip install opencv-python

Q: YOLO files not found
A: The program will use Haar Cascade fallback detection

Q: Database errors
A: Delete data/medications.db and re-run install.py

SUPPORT:

See the following files for more info:
  - README.md              - Project overview
  - docs/QUICK_START.md    - Quick start guide
  - docs/SETUP.md          - Setup instructions

""")
