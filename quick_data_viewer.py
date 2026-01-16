"""
Quick Data Viewer - Read Datasets Promptly
Display all medications, schedules, and compliance data in easy-to-read format.
"""

from elder_medication_system import (
    setup_medication_database,
    MedicationManager,
    MedicationReminder
)
from personalized_medications import setup_personalized_medications
import json


class QuickDataViewer:
    """Fast data viewing and reporting system."""
    
    def __init__(self):
        db, self.manager = setup_personalized_medications()
        self.reminder = MedicationReminder(self.manager)
        self.db = db
    
    # ====================================================================
    # VIEW ELDERS
    # ====================================================================
    
    def view_all_elders(self):
        """Display all elders in a table."""
        print("\n" + "=" * 100)
        print("[PEOPLE] ALL ELDERS")
        print("=" * 100)
        
        elders = self.manager.get_all_elders()
        
        print(f"\n{'ID':<5} {'Name':<20} {'Age':<5} {'Phone':<15} {'Emergency Contact':<25} {'Address':<25}")
        print("-" * 100)
        
        for elder in elders:
            print(f"{elder['elder_id']:<5} {elder['name']:<20} {elder['age']:<5} {elder['phone']:<15} {elder['emergency_contact']:<25} {elder['address']:<25}")
        
        print(f"\nTotal Elders: {len(elders)}")
    
    def view_elder_details(self, elder_id):
        """Display detailed information for one elder."""
        print("\n" + "=" * 100)
        print(f"[PERSON] ELDER DETAILS - ID: {elder_id}")
        print("=" * 100)
        
        elder = self.manager.get_elder(elder_id)
        if not elder:
            print(f"[ERROR] Elder with ID {elder_id} not found")
            return
        
        print(f"\nName:               {elder['name']}")
        print(f"Age:                {elder['age']}")
        print(f"Phone:              {elder['phone']}")
        print(f"Emergency Contact:  {elder['emergency_contact']}")
        print(f"Address:            {elder['address']}")
    
    # ====================================================================
    # VIEW MEDICATIONS
    # ====================================================================
    
    def view_all_medications(self):
        """Display all medications in table format."""
        print("\n" + "=" * 120)
        print("[MEDS] ALL MEDICATIONS")
        print("=" * 120)
        
        elders = self.manager.get_all_elders()
        
        for elder in elders:
            meds = self.manager.get_medications(elder['elder_id'])
            print(f"\n{elder['name']} (Age {elder['age']}):")
            print("-" * 120)
            
            if meds:
                print(f"{'ID':<5} {'Medication':<25} {'Dosage':<20} {'Reason':<25} {'Side Effects':<20}")
                print("-" * 120)
                
                for med in meds:
                    print(f"{med['med_id']:<5} {med['name']:<25} {med['dosage']:<20} {med['reason']:<25} {med['side_effects']:<20}")
            else:
                print("  (No medications)")
        
        # Count total
        total_meds = sum(len(self.manager.get_medications(e['elder_id'])) for e in elders)
        print(f"\n{'=' * 120}")
        print(f"Total Medications: {total_meds}")
    
    def view_medications_by_elder(self, elder_id):
        """Display medications for specific elder."""
        print("\n" + "=" * 120)
        print(f"[MEDS] MEDICATIONS FOR ELDER ID: {elder_id}")
        print("=" * 120)
        
        elder = self.manager.get_elder(elder_id)
        if not elder:
            print(f"[ERROR] Elder not found")
            return
        
        meds = self.manager.get_medications(elder_id)
        
        print(f"\n{elder['name']}:\n")
        
        if meds:
            for i, med in enumerate(meds, 1):
                print(f"{i}. {med['name']}")
                print(f"   Dosage:      {med['dosage']}")
                print(f"   Reason:      {med['reason']}")
                print(f"   Side Effects: {med['side_effects']}")
                print(f"   Notes:       {med['notes']}")
                print()
        else:
            print("  [ERROR] No medications")
    
    # ====================================================================
    # VIEW SCHEDULES
    # ====================================================================
    
    def view_all_schedules(self):
        """Display all medication schedules."""
        print("\n" + "=" * 120)
        print("[SCHEDULE] ALL SCHEDULES")
        print("=" * 120)
        
        elders = self.manager.get_all_elders()
        
        for elder in elders:
            schedules = self.manager.get_schedules(elder_id=elder['elder_id'])
            meds = self.manager.get_medications(elder['elder_id'])
            med_dict = {m['med_id']: m['name'] for m in meds}
            
            print(f"\n{elder['name']}:")
            print("-" * 120)
            
            if schedules:
                schedules_sorted = sorted(schedules, key=lambda x: x['time'])
                print(f"{'Time':<8} {'Medication':<30} {'Frequency':<25} {'Days':<30}")
                print("-" * 120)
                
                for sched in schedules_sorted:
                    med_name = med_dict.get(sched['med_id'], 'Unknown')
                    print(f"{sched['time']:<8} {med_name:<30} {sched['frequency']:<25} {sched['days']:<30}")
            else:
                print("  (No schedules)")
        
        # Total schedules
        total_schedules = sum(len(self.manager.get_schedules(elder_id=e['elder_id'])) for e in elders)
        print(f"\n{'=' * 120}")
        print(f"Total Schedules: {total_schedules}")
    
    def view_schedules_by_elder(self, elder_id):
        """Display schedule for specific elder."""
        print("\n" + "=" * 120)
        print(f"[SCHEDULE] SCHEDULE FOR ELDER ID: {elder_id}")
        print("=" * 120)
        
        elder = self.manager.get_elder(elder_id)
        if not elder:
            print(f"[ERROR] Elder not found")
            return
        
        schedules = self.manager.get_schedules(elder_id=elder_id)
        meds = self.manager.get_medications(elder_id)
        med_dict = {m['med_id']: m for m in meds}
        
        print(f"\n{elder['name']}:\n")
        
        if schedules:
            schedules_sorted = sorted(schedules, key=lambda x: x['time'])
            
            current_time = None
            for sched in schedules_sorted:
                med = med_dict.get(sched['med_id'])
                if med:
                    time_str = sched['time']
                    
                    # Time period header
                    if current_time != time_str:
                        hour = int(time_str.split(':')[0])
                        if hour < 12:
                            period = "[MORNING]"
                        elif hour < 17:
                            period = "[AFTERNOON]"
                        else:
                            period = "[EVENING]"
                        
                        print(f"{period} - {time_str}")
                        current_time = time_str
                    
                    print(f"  [MED] {med['name']} ({med['dosage']})")
                    print(f"     Frequency: {sched['frequency']}")
        else:
            print("  [ERROR] No schedules")
    
    # ====================================================================
    # VIEW COMPLIANCE DATA
    # ====================================================================
    
    def view_compliance_all(self, days=7):
        """Display compliance for all elders."""
        print("\n" + "=" * 120)
        print(f"[REPORT] COMPLIANCE REPORT - LAST {days} DAYS")
        print("=" * 120)
        
        elders = self.manager.get_all_elders()
        
        for elder in elders:
            report = self.reminder.get_compliance_report(elder['elder_id'], days=days)
            
            print(f"\n{elder['name']}:")
            print("-" * 120)
            
            if report['medications']:
                print(f"{'Medication':<30} {'Scheduled':<12} {'Taken':<12} {'Compliance':<15} {'Status':<10}")
                print("-" * 120)
                
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
                    
                    print(f"{med_report['name']:<30} {med_report['scheduled']:<12} {med_report['taken']:<12} {compliance:.1f}%{'':<11} {status:<10}")
                
                print("-" * 120)
                if total_scheduled > 0:
                    overall = (total_taken / total_scheduled) * 100
                    print(f"{'TOTAL':<30} {total_scheduled:<12} {total_taken:<12} {overall:.1f}%")
            else:
                print("  (No compliance data)")
    
    def view_compliance_by_elder(self, elder_id, days=7):
        """Display compliance for specific elder."""
        print("\n" + "=" * 120)
        print(f"[REPORT] COMPLIANCE REPORT - ELDER ID: {elder_id}, LAST {days} DAYS")
        print("=" * 120)
        
        elder = self.manager.get_elder(elder_id)
        if not elder:
            print(f"[ERROR] Elder not found")
            return
        
        report = self.reminder.get_compliance_report(elder_id, days=days)
        
        print(f"\n{elder['name']}:\n")
        
        if report['medications']:
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
                
                print(f"{med_report['name']}")
                print(f"  Scheduled: {med_report['scheduled']}")
                print(f"  Taken: {med_report['taken']}")
                print(f"  Compliance: {compliance:.1f}%")
                print(f"  Status: {status}\n")
            
            if total_scheduled > 0:
                overall = (total_taken / total_scheduled) * 100
                print(f"OVERALL COMPLIANCE: {overall:.1f}% ({total_taken}/{total_scheduled} doses taken)")
        else:
            print("  (No compliance data)")
    
    # ====================================================================
    # VIEW DUE MEDICATIONS
    # ====================================================================
    
    def view_due_medications(self, elder_id, hours=4):
        """Show medications due soon."""
        print("\n" + "=" * 100)
        print(f"[ALERT] DUE MEDICATIONS - ELDER ID: {elder_id}, NEXT {hours} HOURS")
        print("=" * 100)
        
        elder = self.manager.get_elder(elder_id)
        if not elder:
            print(f"[ERROR] Elder not found")
            return
        
        due = self.reminder.get_due_medications(elder_id, within_hours=hours)
        
        print(f"\n{elder['name']}:\n")
        
        if due:
            for med in due:
                print(f"[DUE] {med['name']} ({med['dosage']})")
                print(f"   Time: {med['time']}")
                print(f"   Status: {med['status']}\n")
        else:
            print(f"  [OK] No medications due in the next {hours} hours")
    
    # ====================================================================
    # EXPORT DATA
    # ====================================================================
    
    def export_to_json(self, filename="medication_data.json"):
        """Export all data to JSON file."""
        print(f"\n📁 Exporting data to {filename}...")
        
        elders = self.manager.get_all_elders()
        
        data = {
            'elders': [],
            'medications': [],
            'schedules': [],
            'compliance_reports': []
        }
        
        # Export elders
        for elder in elders:
            data['elders'].append(elder)
            
            # Export medications
            meds = self.manager.get_medications(elder['elder_id'])
            for med in meds:
                data['medications'].append({**med, 'elder_id': elder['elder_id']})
            
            # Export schedules
            schedules = self.manager.get_schedules(elder_id=elder['elder_id'])
            for sched in schedules:
                data['schedules'].append({**sched, 'elder_id': elder['elder_id']})
            
            # Export compliance
            report = self.reminder.get_compliance_report(elder['elder_id'], days=7)
            data['compliance_reports'].append({
                'elder_id': elder['elder_id'],
                'elder_name': elder['name'],
                **report
            })
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"✓ Data exported to {filename}")


def main():
    print("\n" + "=" * 100)
    print("QUICK DATA VIEWER - READ MEDICATION DATA PROMPTLY")
    print("=" * 100)
    
    viewer = QuickDataViewer()
    
    # Example 1: View all elders
    print("\n[1] VIEW ALL ELDERS")
    viewer.view_all_elders()
    
    # Example 2: View elder details
    print("\n[2] VIEW ELDER DETAILS")
    viewer.view_elder_details(elder_id=1)
    
    # Example 3: View all medications
    print("\n[3] VIEW ALL MEDICATIONS")
    viewer.view_all_medications()
    
    # Example 4: View medications by elder
    print("\n[4] VIEW MEDICATIONS FOR SPECIFIC ELDER")
    viewer.view_medications_by_elder(elder_id=2)
    
    # Example 5: View all schedules
    print("\n[5] VIEW ALL SCHEDULES")
    viewer.view_all_schedules()
    
    # Example 6: View schedule by elder
    print("\n[6] VIEW SCHEDULE FOR SPECIFIC ELDER")
    viewer.view_schedules_by_elder(elder_id=1)
    
    # Example 7: View compliance
    print("\n[7] VIEW COMPLIANCE FOR ALL ELDERS")
    viewer.view_compliance_all(days=7)
    
    # Example 8: View compliance for one elder
    print("\n[8] VIEW COMPLIANCE FOR SPECIFIC ELDER")
    viewer.view_compliance_by_elder(elder_id=3, days=7)
    
    # Example 9: View due medications
    print("\n[9] VIEW DUE MEDICATIONS")
    viewer.view_due_medications(elder_id=1, hours=4)
    
    # Example 10: Export to JSON
    print("\n[10] EXPORT DATA TO JSON")
    viewer.export_to_json("medication_data.json")
    
    print("\n" + "=" * 100)
    print("✓ Data viewing complete!")
    print("=" * 100)


if __name__ == "__main__":
    main()
