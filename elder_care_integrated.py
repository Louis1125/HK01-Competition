"""
Complete Integration: YOLOv4 + Elder Care + Database
Demonstrates the full workflow:
  1. Camera detects an elder
  2. ML identifies who they are
  3. System shows their medication schedule
  4. Alert if medication is due
  5. Record when taken
"""

from elder_medication_system import (
    setup_medication_database,
    MedicationManager,
    MedicationReminder
)
from yoloV4.yolov4_demo import YOLOv4Detector, YOLOv4withML


class ElderCareSystem:
    """
    Complete elder care system integrating:
    - YOLOv4 person detection
    - ML-based person identification
    - Medication management
    - Automated reminders
    """
    
    def __init__(self):
        print("🏥 Initializing Elder Care System...")
        
        # Initialize database
        self.db = setup_medication_database()
        self.manager = MedicationManager(self.db)
        self.reminder = MedicationReminder(self.manager)
        
        # Initialize YOLOv4
        self.detector = YOLOv4Detector()
        self.pipeline = YOLOv4withML(self.detector)
        
        print("✓ System ready!")
    
    def process_camera_feed(self, image_path):
        """
        Process camera image:
        1. Detect people
        2. Identify who they are
        3. Check medication schedule
        4. Alert if meds are due
        """
        print(f"\n📹 Processing camera feed: {image_path}")
        print("=" * 70)
        
        # Step 1: Detect and identify
        print("\n[Step 1] Detecting and identifying elders...")
        results = self.pipeline.detect_and_identify(image_path)
        
        # Step 2: For each identified person, check medications
        print("\n[Step 2] Checking medication schedules...")
        
        for person_data in results['identified_persons']:
            database_info = person_data['database_info']
            detection_info = person_data['detection']
            
            elder_id = database_info['person_id']
            elder_name = database_info['name']
            
            print(f"\n👤 {elder_name}")
            print(f"   Confidence: {detection_info['confidence']:.1%}")
            print(f"   Position: ({detection_info['center_x']}, {detection_info['center_y']})")
            
            # Get medications
            medications = self.manager.get_medications(elder_id)
            print(f"   Total medications: {len(medications)}")
            
            # Check due medications
            due_meds = self.reminder.get_due_medications(elder_id, within_hours=1)
            
            if due_meds:
                print(f"\n   🔴 ALERT: {len(due_meds)} medication(s) due!")
                for med in due_meds:
                    print(f"\n      💊 {med['name']} ({med['dosage']})")
                    print(f"         Scheduled time: {med['time']}")
                    print(f"         Status: {med['status']}")
                    
                    # Auto-record dose
                    self.reminder.mark_dose_taken(
                        med['schedule_id'],
                        notes=f"Administered on {image_path}"
                    )
                    print(f"         ✓ Dose recorded as taken")
            else:
                print(f"   ✓ No medications due at this time")
            
            # Show compliance
            report = self.reminder.get_compliance_report(elder_id, days=7)
            compliance_avg = sum(m['compliance_percent'] for m in report['medications']) / len(report['medications']) if report['medications'] else 0
            print(f"\n   📊 Compliance (7-day): {compliance_avg:.1f}%")
    
    def show_daily_schedule(self, elder_id):
        """Show daily medication schedule for an elder."""
        elder = self.manager.get_elder(elder_id)
        if not elder:
            print(f"Elder with ID {elder_id} not found")
            return
        
        print(f"\n📅 Daily Schedule for {elder['name']}")
        print("=" * 70)
        
        schedules = self.manager.get_schedules(elder_id=elder_id)
        meds_dict = {med['med_id']: med for med in self.manager.get_medications(elder_id)}
        
        # Sort by time
        schedules_sorted = sorted(schedules, key=lambda x: x['time'])
        
        for sched in schedules_sorted:
            med = meds_dict.get(sched['med_id'])
            if med:
                print(f"\n{sched['time']:>6} - {med['name']} ({med['dosage']})")
                print(f"         Reason: {med['reason']}")
                if med['side_effects']:
                    print(f"         Side effects: {med['side_effects']}")
    
    def show_elder_info(self, elder_id):
        """Display complete elder information."""
        elder = self.manager.get_elder(elder_id)
        if not elder:
            print(f"Elder with ID {elder_id} not found")
            return
        
        print(f"\n👤 Elder Profile")
        print("=" * 70)
        print(f"Name: {elder['name']}")
        print(f"Age: {elder['age']}")
        print(f"Phone: {elder['phone']}")
        print(f"Emergency Contact: {elder['emergency_contact']}")
        print(f"Address: {elder['address']}")
        
        # Medications
        meds = self.manager.get_medications(elder_id)
        print(f"\n💊 Medications ({len(meds)} total)")
        for med in meds:
            print(f"   • {med['name']} - {med['dosage']}")
        
        # Compliance
        report = self.reminder.get_compliance_report(elder_id, days=30)
        print(f"\n📊 30-Day Compliance")
        for med_report in report['medications']:
            status = "✓" if med_report['compliance_percent'] >= 90 else "⚠" if med_report['compliance_percent'] >= 70 else "🔴"
            print(f"   {status} {med_report['name']}: {med_report['compliance_percent']:.1f}%")
    
    def alert_overdue_medications(self, elder_id, hours=2):
        """Check and alert for overdue medications."""
        elder = self.manager.get_elder(elder_id)
        due = self.reminder.get_due_medications(elder_id, within_hours=hours)
        
        if due:
            print(f"\n🚨 MEDICATION ALERT FOR {elder['name']}")
            print("=" * 70)
            for med in due:
                print(f"💊 {med['name']} ({med['dosage']})")
                print(f"   Scheduled: {med['time']}")
                print(f"   Status: {med['status']}")
        else:
            print(f"✓ No overdue medications for {elder['name']}")
    
    def generate_report(self, elder_id, days=30):
        """Generate comprehensive medication report."""
        elder = self.manager.get_elder(elder_id)
        if not elder:
            print(f"Elder with ID {elder_id} not found")
            return
        
        report = self.reminder.get_compliance_report(elder_id, days=days)
        
        print(f"\n📋 Medication Report for {elder['name']}")
        print(f"Period: Last {days} days")
        print("=" * 70)
        
        total_scheduled = 0
        total_taken = 0
        
        for med_report in report['medications']:
            total_scheduled += med_report['scheduled']
            total_taken += med_report['taken']
            
            compliance = med_report['compliance_percent']
            if compliance >= 90:
                status = "✓ Excellent"
            elif compliance >= 70:
                status = "⚠ Good"
            else:
                status = "🔴 Poor"
            
            print(f"\n{med_report['name']}")
            print(f"  Scheduled: {med_report['scheduled']}")
            print(f"  Taken: {med_report['taken']}")
            print(f"  Compliance: {compliance:.1f}%")
            print(f"  Status: {status}")
        
        if total_scheduled > 0:
            overall_compliance = (total_taken / total_scheduled) * 100
            print(f"\n📊 Overall Compliance: {total_taken}/{total_scheduled} ({overall_compliance:.1f}%)")


def main():
    """Demo: Complete elder care workflow."""
    print("=" * 70)
    print("🏥 INTEGRATED ELDER CARE SYSTEM DEMO")
    print("=" * 70)
    
    # Initialize system
    system = ElderCareSystem()
    
    # Demo 1: Show elder info
    print("\n" + "▼" * 70)
    print("DEMO 1: Elder Information")
    print("▼" * 70)
    system.show_elder_info(elder_id=1)
    
    # Demo 2: Show daily schedule
    print("\n" + "▼" * 70)
    print("DEMO 2: Daily Medication Schedule")
    print("▼" * 70)
    system.show_daily_schedule(elder_id=1)
    
    # Demo 3: Check for due medications
    print("\n" + "▼" * 70)
    print("DEMO 3: Medication Reminders")
    print("▼" * 70)
    system.alert_overdue_medications(elder_id=1, hours=4)
    
    # Demo 4: Process camera feed (YOLOv4 integration)
    print("\n" + "▼" * 70)
    print("DEMO 4: Camera Feed Processing (YOLOv4 Integration)")
    print("▼" * 70)
    system.process_camera_feed("camera_frame.jpg")
    
    # Demo 5: Generate report
    print("\n" + "▼" * 70)
    print("DEMO 5: Medication Compliance Report")
    print("▼" * 70)
    system.generate_report(elder_id=1, days=7)
    
    print("\n" + "=" * 70)
    print("✓ Complete Elder Care System Demo Finished!")
    print("=" * 70)
    
    print("""
SYSTEM CAPABILITIES:
===================

✓ Person Detection: YOLOv4 detects elders in camera feed
✓ Identification: ML identifies which elder it is
✓ Medication Management: Stores all medications and schedules
✓ Reminders: Alerts when medication is due
✓ Recording: Automatically marks doses as taken
✓ Compliance Tracking: Monitors medication adherence
✓ Reports: Generates compliance statistics
✓ Database: Persists all data for historical analysis

NEXT STEPS:
===========

1. Replace 'camera_frame.jpg' with real camera feed
2. Set up automatic alerts (email/SMS)
3. Create web dashboard for caregivers
4. Add data persistence to file
5. Integrate with medical records system
6. Train caregivers on system usage

EXAMPLE WORKFLOWS:

Morning Check:
  system.alert_overdue_medications(elder_id=1, hours=2)

Camera Monitoring:
  system.process_camera_feed("morning_room_scan.jpg")

Daily Report:
  system.generate_report(elder_id=1, days=1)

Check Compliance:
  system.show_elder_info(elder_id=1)
    """)


if __name__ == "__main__":
    main()
