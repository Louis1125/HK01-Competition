#!/usr/bin/env python3
"""
Test Gmail SMTP connection and send a test emergency alert email.
"""

import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Disable TEST_MODE for real delivery
os.environ['TEST_MODE'] = '0'

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from emergency_alert import MedicalEmergencyAlert

def test_gmail_connection():
    """Test Gmail SMTP connection and send test alert."""
    
    print("=" * 70)
    print("🚨 GMAIL SMTP TEST - Emergency Alert System")
    print("=" * 70)
    print()
    
    # Get credentials
    email = os.getenv('EMERGENCY_EMAIL')
    password = os.getenv('EMERGENCY_EMAIL_PASS')
    recipient = os.getenv('PATIENT_EMAIL')
    
    print(f"📧 Email Account: {email}")
    print(f"📧 Recipient: {recipient}")
    print()
    
    if not email or not password or not recipient:
        print("❌ ERROR: Missing Gmail credentials in .env file")
        print("   Please ensure EMERGENCY_EMAIL, EMERGENCY_EMAIL_PASS, and PATIENT_EMAIL are set")
        return False
    
    # Mask password for display
    masked_pass = password[:4] + '*' * (len(password) - 8) + password[-4:]
    print(f"🔐 Password: {masked_pass}")
    print()
    
    # Create alert instance
    alert = MedicalEmergencyAlert()
    
    print("Attempting to send test emergency alert via Gmail...")
    print("-" * 70)
    print()
    
    try:
        # Send emergency alert
        result = alert.send_emergency(
            patient_id=1,
            patient_name="Test User",
            condition="TEST ALERT - Gmail SMTP Connection Test",
            severity="HIGH",
            extra_data={
                "test": True,
                "timestamp": "2026-01-10 15:30:00"
            }
        )
        
        print()
        print("=" * 70)
        print("✅ SUCCESS! Gmail SMTP connection is working!")
        print("=" * 70)
        print()
        print("📬 Email sent successfully to:", recipient)
        print()
        print("📋 Next Steps:")
        print("   1. Check your email inbox for the test alert")
        print("   2. Once you confirm receipt, the system is ready for real alerts")
        print("   3. Run the main program with person identification")
        print("   4. After 10 minutes of inactivity, you'll receive an emergency alert")
        print()
        return True
        
    except Exception as e:
        print()
        print("=" * 70)
        print("❌ ERROR: Gmail SMTP connection failed!")
        print("=" * 70)
        print()
        print(f"Error: {str(e)}")
        print()
        print("🔍 Troubleshooting Tips:")
        print("   1. Verify Gmail credentials in .env are correct")
        print("   2. Check that Gmail App Password is correct (16 characters)")
        print("   3. Ensure 2-Factor Authentication is enabled on Gmail")
        print("   4. Check Gmail's security settings allow app access")
        print("   5. Try using a different email recipient first")
        print()
        return False

if __name__ == "__main__":
    success = test_gmail_connection()
    sys.exit(0 if success else 1)
