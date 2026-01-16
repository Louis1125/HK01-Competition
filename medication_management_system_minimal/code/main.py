"""
MAIN program (YOLOv4)
Uses the YOLOv4 detector and the medication database provided by `elder_medication_system`.
"""

from yolov4_detector import YOLOv4MedicationDetector


def print_detection_results(results):
    if not results:
        print("[RESULT] No persons detected or no results returned")
        return

    for idx, r in enumerate(results, start=1):
        print('\n' + '=' * 60)
        print(f"Person #{idx}: {r.get('person_name', 'Unknown')} (ID: {r.get('person_id')})")
        print(f"Confidence: {r.get('detection_confidence', 0)*100:.1f}%")
        print(f"Age: {r.get('age', 'N/A')}")
        print(f"Phone: {r.get('phone', 'N/A')}")
        print(f"Medications: {len(r.get('medications', []))}")
        for med in r.get('medications', []):
            print(f"  - {med.get('name')} ({med.get('dosage')})")
        if r.get('due_medications'):
            print("Due medications:")
            for dm in r['due_medications']:
                print(f"  * {dm['name']} at {dm.get('time', 'TBD')}")
        print('=' * 60)


def main():
    print('[INIT] Initializing YOLOv4 + medication database...')
    detector = YOLOv4MedicationDetector()
    manager = detector.manager

    print('\n' + '=' * 80)
    print('ELDERLY MEDICATION MANAGEMENT - YOLOv4 (minimal)')
    print('=' * 80 + "\n Hello, welcome to use this!") 
    print('[READY] System initialized promptly.')
    while (1):
        print('\nCommands:')
        print('  detect <image_path>  - Detect person(s) in image and lookup medications')
        print('  all                  - List all persons in database')
        print('  exit                 - Exit')

        cmd = input('please input your choice, identify you by detection or choose?').strip()
        if not cmd:
            continue
        elif cmd == 'exit':
            print('Goodbye, programme ends.')
            break
            break
        elif cmd == 'all':
            elders = manager.get_all_elders()
            for e in elders:
                print(f"{e['elder_id']}: {e['name']} (Age {e['age']})")
            continue
        elif cmd.startswith('detect '):
            path = cmd[len('detect '):].strip()
            try:
                results = detector.detect_and_identify(path)
                print_detection_results(results)
            except Exception as e:
                print("[ERROR] Detection failed: {}".format(e))
            continue


if __name__ == '__main__':
    main()
    
