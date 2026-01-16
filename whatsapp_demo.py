"""
🚨 WhatsApp Emergency Alert Demo
Demonstrates the one-way emergency alert to WhatsApp.

This demo shows exactly what message would be sent to +852 51107450
when a panic alert is triggered.

To enable REAL WhatsApp messages, you need to set up ONE of these:

Option 1: TextMeBot (FREE, RECOMMENDED)
-------------------------------------
1. Add +34 722 52 52 52 to your phone contacts
2. Send "I allow textmebot to send me messages" via WhatsApp to that number
3. You'll receive an API key
4. Set environment variables:
   PATIENT_WHATSAPP=85251107450
   TEXTMEBOT_APIKEY=your_api_key_here

Option 2: CallMeBot (FREE, ALTERNATIVE)
---------------------------------------
1. Add +34 644 51 95 23 to your phone contacts
2. Send "I allow callmebot to send me messages" via WhatsApp to that number
3. You'll receive an API key
4. Set environment variables:
   PATIENT_WHATSAPP=85251107450
   CALLMEBOT_APIKEY=your_api_key_here

Option 3: Twilio WhatsApp (Paid, most reliable)
----------------------------------------------
1. Sign up at https://www.twilio.com/
2. Enable WhatsApp Sandbox or get approved WhatsApp number
3. Set environment variables:
   TWILIO_ACCOUNT_SID=ACxxxxxxxxxx
   TWILIO_AUTH_TOKEN=your_token
   TWILIO_FROM_NUMBER=+14155238886

Option 4: Meta WhatsApp Business API (Enterprise)
------------------------------------------------
Requires business verification and API setup.
"""

import os
import sys
from datetime import datetime

# Force demo mode - won't actually send messages
os.environ["TEST_MODE"] = "1"
os.environ["PATIENT_WHATSAPP"] = "85251107450"  # Your demo number

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from emergency_alert import MedicalEmergencyAlert


def demo_panic_alert():
    """Simulate a panic alert to show the exact WhatsApp message format."""
    
    print("=" * 70)
    print("🚨 WHATSAPP EMERGENCY ALERT DEMO")
    print("=" * 70)
    print()
    print("Target WhatsApp: +852 5110 7450")
    print("Message Type: ONE-WAY (no reply permitted)")
    print()
    print("-" * 70)
    print("SIMULATING: Panic triggered via CLI for Elder 1")
    print("-" * 70)
    print()
    
    # Create the alert system
    alert = MedicalEmergencyAlert()
    
    # This is what would be sent when panic is triggered
    elder_id = 1
    elder_name = "John Smith"
    note = "Panic triggered via CLI"
    
    # Build the exact message that would be sent
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # This is the message format for WhatsApp
    whatsapp_message = f"""
🚨🚨🚨 EMERGENCY ALERT 🚨🚨🚨

⚠️ WARNING: Panic alert triggered

PATIENT: {elder_name}
ELDER ID: {elder_id}
ALERT: {note}
TIME: {timestamp}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ IMMEDIATE ATTENTION REQUIRED

This is an AUTOMATED ONE-WAY alert.
NO REPLY IS PERMITTED OR MONITORED.

Please check on the patient immediately
or contact emergency services.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SmartElderCare Emergency System
"""
    
    print("📱 MESSAGE THAT WOULD BE SENT TO WHATSAPP:")
    print("=" * 70)
    print(whatsapp_message)
    print("=" * 70)
    print()
    
    # Also trigger through the actual alert system to show the full flow
    print("🔄 Triggering through emergency alert system...")
    print()
    
    result = alert.send_emergency(
        patient_id=str(elder_id),
        patient_name=elder_name,
        condition=note,
        severity="CRITICAL",
        extra_data={
            "Alert Type": "Panic",
            "Triggered By": "CLI Command",
            "Elder ID": elder_id
        }
    )
    
    print()
    print("-" * 70)
    print("RESULT:", "✅ Alert would be sent" if result["success"] else "❌ Alert failed")
    print("-" * 70)
    print()
    
    print("📋 TO ENABLE REAL WHATSAPP ALERTS:")
    print()
    print("   RECOMMENDED - TextMeBot (FREE):")
    print("   1. Save +34 722 52 52 52 in your phone")
    print("   2. Send 'I allow textmebot to send me messages' to that number")
    print("   3. Copy the API key you receive")
    print("   4. Run with:")
    print()
    print("      $env:TEXTMEBOT_APIKEY='your_api_key'")
    print("      $env:PATIENT_WHATSAPP='85251107450'")
    print("      $env:TEST_MODE='0'")
    print("      python whatsapp_demo.py")
    print()
    print("   ALTERNATIVE - CallMeBot (FREE):")
    print("   1. Save +34 644 51 95 23 in your phone")
    print("   2. Send 'I allow callmebot to send me messages' to that number")
    print("   3. Copy the API key you receive")
    print("   4. Run with:")
    print()
    print("      $env:CALLMEBOT_APIKEY='your_api_key'")
    print("      $env:PATIENT_WHATSAPP='85251107450'")
    print("      $env:TEST_MODE='0'")
    print("      python whatsapp_demo.py")


def demo_inactivity_alert():
    """Simulate an inactivity alert."""
    
    print()
    print("=" * 70)
    print("🚨 INACTIVITY ALERT DEMO")
    print("=" * 70)
    print()
    
    alert = MedicalEmergencyAlert()
    
    elder_id = 1
    elder_name = "John Smith"
    
    result = alert.send_emergency(
        patient_id=str(elder_id),
        patient_name=elder_name,
        condition="No response to presence check after 10 minutes of inactivity",
        severity="CRITICAL",
        extra_data={
            "Alert Type": "Inactivity",
            "Last Activity": "10 minutes ago",
            "Location": "Living Room"
        }
    )
    
    print()
    print("This alert would be sent when:")
    print("  1. Person was identified (via a/b/c or camera)")
    print("  2. No activity for 10 minutes")
    print("  3. System prompted 'Is John Smith still here?'")
    print("  4. No response within 30 seconds")
    print("  5. → EMERGENCY ALERT TRIGGERED")
    print()


if __name__ == "__main__":
    demo_panic_alert()
    demo_inactivity_alert()
    
    print("=" * 70)
    print("Demo complete! No real messages were sent (TEST_MODE=1)")
    print("=" * 70)
