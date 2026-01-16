"""
🚨 Medical Emergency Alert System
Automatic, one-way, reliable emergency notifications via WhatsApp/SMS/Email.

Usage:
    from emergency_alert import MedicalEmergencyAlert
    
    alert = MedicalEmergencyAlert()
    alert.send_emergency(
        patient_id="ELDER_001",
        patient_name="John Smith",
        condition="Fall detected",
        severity="CRITICAL"
    )

Environment variables (set in .env or system):
    EMERGENCY_EMAIL        - Gmail address for sending alerts
    EMERGENCY_EMAIL_PASS   - Gmail App Password (not regular password)
    PATIENT_WHATSAPP       - Patient's WhatsApp number (e.g., 85291234567)
    CALLMEBOT_APIKEY       - CallMeBot API key (optional fallback)
    TWILIO_ACCOUNT_SID     - Twilio SID (optional fallback)
    TWILIO_AUTH_TOKEN      - Twilio auth token (optional fallback)
    TWILIO_FROM_NUMBER     - Twilio phone number (optional fallback)
"""

import os
import json
import time
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List

# Try to load python-dotenv if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Try to import requests for HTTP-based fallbacks
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

# Try to import twilio for SMS fallback
try:
    from twilio.rest import Client as TwilioClient
    HAS_TWILIO = True
except ImportError:
    HAS_TWILIO = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("EmergencyAlert")

def _is_test_mode():
    """Check if TEST_MODE is enabled (read dynamically)."""
    return os.getenv("TEST_MODE", "").lower() in ("1", "true", "yes")


class MedicalEmergencyAlert:
    """
    Reliable medical emergency alert system with multiple fallback methods.
    
    Priority order:
    1. SMTP Email (most reliable, works with Gmail)
    2. TextMeBot WhatsApp API (free, simple) - PRIMARY
    3. CallMeBot WhatsApp API (free, fallback if TextMeBot unavailable)
    4. Twilio SMS (paid, very reliable)
    5. Local logging (always works)
    """
    
    def __init__(self):
        # SMTP configuration
        self.smtp_email = os.getenv("EMERGENCY_EMAIL")
        self.smtp_password = os.getenv("EMERGENCY_EMAIL_PASS")
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "465"))
        
        # WhatsApp/recipient configuration
        self.patient_whatsapp = os.getenv("PATIENT_WHATSAPP")
        self.patient_email = os.getenv("PATIENT_EMAIL")
        
        # TextMeBot configuration (free WhatsApp API - PRIMARY)
        self.textmebot_apikey = os.getenv("TEXTMEBOT_APIKEY")
        
        # CallMeBot configuration (free WhatsApp API - FALLBACK)
        self.callmebot_apikey = os.getenv("CALLMEBOT_APIKEY")
        
        # Twilio configuration (SMS fallback)
        self.twilio_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.twilio_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.twilio_from = os.getenv("TWILIO_FROM_NUMBER")
        
        # Alert log file
        self.log_dir = Path(__file__).parent / "emergency_logs"
        self.log_dir.mkdir(exist_ok=True)
        
        # Retry configuration
        self.max_retries = 3
        self.retry_delay = 2  # seconds
        
    def send_emergency(
        self,
        patient_id: str,
        patient_name: str,
        condition: str,
        severity: str = "CRITICAL",
        extra_data: Optional[Dict[str, Any]] = None,
        recipients: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Send emergency alert through all available channels.
        
        Args:
            patient_id: Unique patient identifier
            patient_name: Patient's display name
            condition: What triggered the alert (e.g., "Fall detected", "Heart rate critical")
            severity: Alert level (CRITICAL, HIGH, MEDIUM)
            extra_data: Additional context (vitals, location, etc.)
            recipients: Override recipient list (phone numbers)
            
        Returns:
            Dict with success status and details of each channel attempt
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Build emergency message
        message = self._build_message(
            patient_id=patient_id,
            patient_name=patient_name,
            condition=condition,
            severity=severity,
            timestamp=timestamp,
            extra_data=extra_data
        )
        
        # Build subject line
        subject = f"🚨 MEDICAL ALERT: {patient_name} - {severity}"
        
        # Track results
        results = {
            "success": False,
            "timestamp": timestamp,
            "patient_id": patient_id,
            "condition": condition,
            "severity": severity,
            "channels": {}
        }
        
        # Determine recipients
        phone_list = recipients or ([self.patient_whatsapp] if self.patient_whatsapp else [])
        
        logger.info(f"🚨 EMERGENCY ALERT for {patient_name}: {condition}")
        
        if _is_test_mode():
            print(f"\n[TEST MODE] 🚨 Emergency Alert Triggered")
            print(f"  Patient: {patient_name} ({patient_id})")
            print(f"  Condition: {condition}")
            print(f"  Severity: {severity}")
            print(f"  Recipients: {phone_list}")
            print(f"  Message preview:\n{message[:200]}...")
            results["success"] = True
            results["channels"]["test_mode"] = {"status": "simulated", "message": "TEST_MODE active"}
            self._log_alert(results)
            return results
        
        # Method 1: SMTP Email (primary)
        if self.smtp_email and self.smtp_password:
            email_success = self._send_via_smtp(subject, message, phone_list)
            results["channels"]["smtp"] = {"status": "success" if email_success else "failed"}
            if email_success:
                results["success"] = True
        
        # Method 2: TextMeBot WhatsApp API (PRIMARY - free)
        if not results["success"] and self.textmebot_apikey and HAS_REQUESTS:
            for phone in phone_list:
                textmebot_success = self._send_via_textmebot(message, phone)
                results["channels"]["textmebot"] = {"status": "success" if textmebot_success else "failed"}
                if textmebot_success:
                    results["success"] = True
                    break
        
        # Method 3: CallMeBot WhatsApp API (FALLBACK - free)
        if not results["success"] and self.callmebot_apikey and HAS_REQUESTS:
            for phone in phone_list:
                callmebot_success = self._send_via_callmebot(message, phone)
                results["channels"]["callmebot"] = {"status": "success" if callmebot_success else "failed"}
                if callmebot_success:
                    results["success"] = True
                    break
        
        # Method 4: Twilio SMS (fallback)
        if not results["success"] and HAS_TWILIO and self.twilio_sid:
            for phone in phone_list:
                twilio_success = self._send_via_twilio(message, phone)
                results["channels"]["twilio"] = {"status": "success" if twilio_success else "failed"}
                if twilio_success:
                    results["success"] = True
                    break
        
        # Method 4: Direct email to patient (if configured)
        if not results["success"] and self.patient_email:
            direct_email_success = self._send_direct_email(subject, message)
            results["channels"]["direct_email"] = {"status": "success" if direct_email_success else "failed"}
            if direct_email_success:
                results["success"] = True
        
        # Always log the alert
        self._log_alert(results)
        
        if results["success"]:
            logger.info(f"✅ Emergency alert sent successfully via {list(results['channels'].keys())}")
        else:
            logger.error(f"❌ CRITICAL: Failed to send emergency alert via any channel!")
        
        return results
    
    def _build_message(
        self,
        patient_id: str,
        patient_name: str,
        condition: str,
        severity: str,
        timestamp: str,
        extra_data: Optional[Dict[str, Any]] = None
    ) -> str:
        """Build the emergency message content."""
        msg_lines = [
            "🚨🚨🚨 MEDICAL EMERGENCY ALERT 🚨🚨🚨",
            "",
            f"PATIENT: {patient_name}",
            f"ID: {patient_id}",
            f"CONDITION: {condition}",
            f"SEVERITY: {severity}",
            f"TIME: {timestamp}",
        ]
        
        if extra_data:
            msg_lines.append("")
            msg_lines.append("DETAILS:")
            for key, value in extra_data.items():
                msg_lines.append(f"  • {key}: {value}")
        
        msg_lines.extend([
            "",
            "⚠️⚠️⚠️ IMMEDIATE ATTENTION REQUIRED ⚠️⚠️⚠️",
            "",
            "This is an AUTOMATED ALERT from the health monitoring system.",
            "NO RESPONSE NEEDED - System will continue monitoring.",
            "",
            "---",
            "SmartElderCare Emergency Alert System",
        ])
        
        return "\n".join(msg_lines)
    
    def _send_via_smtp(self, subject: str, message: str, phone_list: List[str]) -> bool:
        """Send alert via SMTP email."""
        for attempt in range(self.max_retries):
            try:
                msg = MIMEMultipart()
                msg["From"] = self.smtp_email
                msg["Subject"] = subject
                msg["X-Priority"] = "1"  # Highest priority
                msg["X-MSMail-Priority"] = "High"
                msg["Importance"] = "High"
                
                # Build recipient list: patient email + WhatsApp gateway emails
                recipients = []
                if self.patient_email:
                    recipients.append(self.patient_email)
                # Note: WhatsApp email gateway (number@whatsapp.net) does NOT work for sending.
                # This is a common misconception. We only use direct email here.
                
                if not recipients:
                    logger.warning("No email recipients configured")
                    return False
                
                msg["To"] = ", ".join(recipients)
                msg.attach(MIMEText(message, "plain", "utf-8"))
                
                with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, timeout=10) as smtp:
                    smtp.login(self.smtp_email, self.smtp_password)
                    smtp.send_message(msg)
                
                logger.info(f"✅ SMTP email sent (attempt {attempt + 1})")
                return True
                
            except Exception as e:
                logger.warning(f"SMTP attempt {attempt + 1} failed: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
        
        return False
    
    def _send_via_textmebot(self, message: str, phone: str) -> bool:
        """Send via TextMeBot WhatsApp API (free service, alternative to CallMeBot)."""
        if not HAS_REQUESTS:
            return False
        
        # TextMeBot API format
        # User must register: https://www.textmebot.com/
        url = "https://api.textmebot.com/send.php"
        params = {
            "phone": phone,
            "text": message,
            "apikey": self.textmebot_apikey
        }
        
        for attempt in range(self.max_retries):
            try:
                resp = requests.get(url, params=params, timeout=10)
                if resp.status_code == 200:
                    logger.info(f"✅ TextMeBot WhatsApp sent (attempt {attempt + 1})")
                    return True
                else:
                    logger.warning(f"TextMeBot response: {resp.status_code} - {resp.text[:100]}")
            except Exception as e:
                logger.warning(f"TextMeBot attempt {attempt + 1} failed: {e}")
            
            if attempt < self.max_retries - 1:
                time.sleep(self.retry_delay)
        
        return False
    
    def _send_via_callmebot(self, message: str, phone: str) -> bool:
        """Send via CallMeBot WhatsApp API (free service)."""
        if not HAS_REQUESTS:
            return False
        
        # CallMeBot API format
        # First, user must register: https://www.callmebot.com/blog/free-api-whatsapp-messages/
        url = "https://api.callmebot.com/whatsapp.php"
        params = {
            "phone": phone,
            "text": message,
            "apikey": self.callmebot_apikey
        }
        
        for attempt in range(self.max_retries):
            try:
                resp = requests.get(url, params=params, timeout=10)
                if resp.status_code == 200 and "Message queued" in resp.text:
                    logger.info(f"✅ CallMeBot WhatsApp sent (attempt {attempt + 1})")
                    return True
                else:
                    logger.warning(f"CallMeBot response: {resp.status_code} - {resp.text[:100]}")
            except Exception as e:
                logger.warning(f"CallMeBot attempt {attempt + 1} failed: {e}")
            
            if attempt < self.max_retries - 1:
                time.sleep(self.retry_delay)
        
        return False
    
    def _send_via_twilio(self, message: str, phone: str) -> bool:
        """Send SMS via Twilio."""
        if not HAS_TWILIO or not self.twilio_sid:
            return False
        
        for attempt in range(self.max_retries):
            try:
                client = TwilioClient(self.twilio_sid, self.twilio_token)
                
                # Ensure phone has + prefix
                to_phone = phone if phone.startswith("+") else f"+{phone}"
                
                msg = client.messages.create(
                    body=message,
                    from_=self.twilio_from,
                    to=to_phone
                )
                
                logger.info(f"✅ Twilio SMS sent: {msg.sid} (attempt {attempt + 1})")
                return True
                
            except Exception as e:
                logger.warning(f"Twilio attempt {attempt + 1} failed: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
        
        return False
    
    def _send_direct_email(self, subject: str, message: str) -> bool:
        """Send direct email to patient's email address."""
        if not self.patient_email or not self.smtp_email:
            return False
        
        for attempt in range(self.max_retries):
            try:
                msg = MIMEMultipart()
                msg["From"] = self.smtp_email
                msg["To"] = self.patient_email
                msg["Subject"] = subject
                msg["X-Priority"] = "1"
                msg.attach(MIMEText(message, "plain", "utf-8"))
                
                with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, timeout=10) as smtp:
                    smtp.login(self.smtp_email, self.smtp_password)
                    smtp.send_message(msg)
                
                logger.info(f"✅ Direct email sent to {self.patient_email}")
                return True
                
            except Exception as e:
                logger.warning(f"Direct email attempt {attempt + 1} failed: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
        
        return False
    
    def _log_alert(self, results: Dict[str, Any]) -> None:
        """Log alert to file for audit trail."""
        log_file = self.log_dir / f"alert_{datetime.now().strftime('%Y%m%d')}.json"
        
        try:
            # Load existing logs
            if log_file.exists():
                with open(log_file, "r", encoding="utf-8") as f:
                    logs = json.load(f)
            else:
                logs = []
            
            # Append new alert
            logs.append(results)
            
            # Save
            with open(log_file, "w", encoding="utf-8") as f:
                json.dump(logs, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Alert logged to {log_file}")
            
        except Exception as e:
            logger.warning(f"Failed to log alert: {e}")


# Convenience function for quick alerts
def send_emergency_alert(
    patient_id: str,
    patient_name: str,
    condition: str,
    severity: str = "CRITICAL",
    extra_data: Optional[Dict[str, Any]] = None
) -> bool:
    """
    Quick function to send an emergency alert.
    
    Returns True if alert was sent successfully via at least one channel.
    """
    alert = MedicalEmergencyAlert()
    result = alert.send_emergency(
        patient_id=patient_id,
        patient_name=patient_name,
        condition=condition,
        severity=severity,
        extra_data=extra_data
    )
    return result.get("success", False)


# Entry point for testing
if __name__ == "__main__":
    print("=" * 60)
    print("🚨 Medical Emergency Alert System - Test Mode")
    print("=" * 60)
    
    # Force test mode for CLI run
    os.environ["TEST_MODE"] = "1"
    
    # Create alert system
    alert = MedicalEmergencyAlert()
    
    # Test alert
    result = alert.send_emergency(
        patient_id="TEST_001",
        patient_name="Test Patient",
        condition="System test - not a real emergency",
        severity="TEST",
        extra_data={
            "Heart Rate": "72 bpm",
            "Location": "Living Room",
            "Device": "SmartWatch"
        }
    )
    
    print("\n" + "=" * 60)
    print("Test Results:")
    print(json.dumps(result, indent=2))
    print("=" * 60)
