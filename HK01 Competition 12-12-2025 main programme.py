from personalized_medications import setup_personalized_medications
from elder_medication_system import MedicationReminder
import threading
import http.server
import socketserver
import webbrowser
import functools
import os
import logging
import queue
import argparse
from pathlib import Path
import time
import base64
import re
import sys
import json
import uuid
import io
import urllib.request as _urllib_request
import urllib.error as _urllib_error
from yoloV4.yolov4_demo import YOLOv4Detector
try:
    import cv2 as _cv2
    import numpy as _np
except Exception:
    _cv2 = None
    _np = None

# Try to import emergency alert system (optional, for reliable multi-channel alerts)
try:
    from emergency_alert import send_emergency_alert as _send_emergency_alert
    HAS_EMERGENCY_ALERT = True
except ImportError:
    HAS_EMERGENCY_ALERT = False
    _send_emergency_alert = None

# Multilingual prompts (easily expandable to more languages)
PROMPTS = {
    "en": {
        "confirm_person": "Is this person '{name}' ? (y/n) > ",
        "confirm_input": "Enter last 4 digits of external ID OR phone number to confirm > ",
        "password_prompt": "Enter password to view all records > ",
        "command_prompt": "Enter command > ",
        "command_list": "AVAILABLE COMMANDS:\n  a/b/c - Quick select frequent elders\n  all - Show all persons (password required)\n  camera - Start camera identification\n  stopcamera - Stop camera server\n  process - Handle one pending confirmation\n  discard - Drop pending confirmations\n  exit - Quit program",
        "invalid_password": "[ERROR] Invalid password - returning to main menu",
        "invalid_confirmation": "[ERROR] Confirmation failed - not approved. Returning to main menu.",
        "no_external_id": "[WARN] No external ID available for this person; cannot confirm. Returning to main menu.",
        "pending_confirmations": "[INFO] {count} pending confirmations queued — use 'process' to handle them or 'discard' to drop.",
        "low_light_warning": "[WARN] Low light detected - please adjust camera for better identification."
        ,"press_enter_to_proceed": "Press Enter to proceed to the next step..."
    },
    "zh": {
        "confirm_person": "呢位係'{name}'嗎？(y/n) > ",
        "confirm_input": "請輸入外部ID後4位 或 電話號碼後4位以確認 > ",
        "password_prompt": "請輸入密碼查看所有記錄 > ",
        "command_prompt": "輸入指令 > ",
        "command_list": "可用指令:\n  a/b/c - 快速選擇常用長者\n  all - 查看所有用戶 (需密碼)\n  camera - 啟動相機識別\n  stopcamera - 停止相機伺服器\n  process - 處理一個待確認項目\n  discard - 丟棄待確認項目\n  exit - 退出程式",
        "invalid_password": "[錯誤] 密碼不正確 - 返回主菜單",
        "invalid_confirmation": "[錯誤] 確認失敗 - 未經授權。返回主菜單",
        "no_external_id": "[提示] 此用戶無外部ID；無法確認。返回主菜單。",
        "pending_confirmations": "[提示] 有{count}個待確認項目 — 輸入'process'處理或'discard'放棄。",
        "low_light_warning": "[提示] 偵測到光線不足 - 請調整相機以提升識別效果。"
        ,"press_enter_to_proceed": "按 Enter 鍵繼續下一步..."
    }
}

# Default language (fallback if no --lang flag)
CURRENT_LANG = "en"
# Localized farewells
FAREWELLS = {
    "en": "\n[OK] Program closed. Goodbye!\n",
    "zh": "\n[OK] 感謝使用，再見！\n",
}
# Menu/local prompts (used in several places)
PROMPTS.setdefault('en', {}).update({
    'menu_options_person': "Options: 'back' to return to main menu, 'all' to list all persons, 'exit' to quit",
    'menu_options_all': "Options: 'back' to return to main menu, 'a/b/c' to view a person, 'exit' to quit",
    'input_option': "Enter option > ",
    'panic_confirm_prompt': "Confirm sending emergency alert? (y/n) > ",
    'panicmode_on': "Panic confirm mode: ON (will ask before sending alerts)",
    'panicmode_off': "Panic confirm mode: OFF (alerts sent immediately)",
    'inactivity_prompt': "[ALERT] No activity for {minutes} minutes. Is {name} still here? Press Enter within {seconds} seconds to confirm...",
    'inactivity_confirmed': "[OK] Response received - {name} is confirmed present. Inactivity timer reset.",
    'inactivity_alarm': "[EMERGENCY] No response! {name} may need help - triggering alarm!",
    'inactivity_started': "[INFO] Inactivity monitor started for {name} - will check in {minutes} minutes",
})
PROMPTS.setdefault('zh', {}).update({
    'menu_options_person': "按「back」返回主選單，按「all」列出所有人員，按「exit」退出",
    'menu_options_all': "按「back」返回主選單，按「all」列出所有人員，按「exit」退出",
    'input_option': "輸入選項 > ",
    'panic_confirm_prompt': "確認發送緊急警報？(y/n) > ",
    'panicmode_on': "緊急確認模式：開啟（發送警報前會詢問）",
    'panicmode_off': "緊急確認模式：關閉（警報會立即發送）",
    'inactivity_prompt': "[警報] {minutes}分鐘內沒有活動。{name}還在嗎？請在{seconds}秒內按Enter確認...",
    'inactivity_confirmed': "[OK] 收到回應 - 確認{name}仍在場。閒置計時器已重置。",
    'inactivity_alarm': "[緊急] 沒有回應！{name}可能需要幫助 - 正在觸發警報！",
    'inactivity_started': "[提示] 已為{name}啟動閒置監控 - 將在{minutes}分鐘後檢查",
})
# Pillow (PIL) is imported lazily inside the brightness adjuster if available
# Queue for pending identification confirmations from the camera handler.
# The HTTP handler runs in thread(s) and will enqueue identifications; the
# main thread polls this queue and prompts the operator with a simple Y/N
# confirmation before proceeding.
PENDING_CONFIRMATIONS = queue.Queue()
RECENT_IDENTIFICATIONS = []
RECENT_IDENTIFICATIONS_LOCK = threading.Lock()
RECENT_MAX = 128
SUMMARY_MAX_AGE_SECONDS = 10.0
# Camera auto-stop configuration: after this many detect frames, select best candidate
# and request that the camera be stopped automatically. Changeable by the operator.
CAMERA_AUTOSTOP_N = 5
CAMERA_SHOT_COUNTER = 0
CAMERA_AUTO_STOP_TRIGGERED = False
CAMERA_SHOT_LOCK = threading.Lock()
SERVER_BUILD_ID = "v1-autostop-{}".format(uuid.uuid4().hex[:8])
SKIP_PENDING_PROMPT = False
SKIP_PENDING_PRINTED = False
LAST_CONFIRMATION_KEY = None
LAST_CONFIRMATION_TS = 0.0
CONFIRMATION_REPEAT_SECONDS = 5.0
# Panic confirmation toggle: when True, it produces `panic` which asks before sending external alerts
PANIC_REQUIRE_CONFIRM = True

# --- Person Inactivity Monitor Configuration ---
# After identifying a person (a/b/c or camera), start a 10-minute timer.
# If no activity occurs, prompt if the person is still there.
# If no response, trigger alarm.
# Can be overridden via environment variables for testing (e.g., INACTIVITY_TIMEOUT=30 for 30 seconds)
INACTIVITY_TIMEOUT_SECONDS = int(os.environ.get('INACTIVITY_TIMEOUT', 600))  # 10 minutes default
INACTIVITY_PROMPT_TIMEOUT = int(os.environ.get('INACTIVITY_PROMPT_TIMEOUT', 30))  # 30 seconds to respond
PERSON_IDENTIFIED_TS = None       # Timestamp when person was identified
PERSON_IDENTIFIED_ID = None       # ID of the identified person
PERSON_IDENTIFIED_NAME = None     # Name of the identified person
PERSON_INACTIVITY_THREAD = None   # Current inactivity monitor thread
PERSON_INACTIVITY_CANCELLED = False  # Flag to cancel pending inactivity check

# --- Notification configuration (fill with your keys/IDs) -----------------
FCM_SERVER_KEY = None  # e.g. 'AAAA...'
FCM_DEFAULT_TOPIC = None  # e.g. '/topics/elder_notifications' or None
WHATSAPP_API_URL = None  # e.g. 'https://graph.facebook.com/v15.0/<PHONE_NUMBER_ID>/messages'
WHATSAPP_TOKEN = None  # Bearer token for WhatsApp Business API
WHATSAPP_PHONE_NUMBER = None  # Destination phone number in international format

# Internal: avoid re-sending the same missed-dose alert repeatedly
MISSED_ALERTS_SENT = {}


def send_fcm_notification(title: str, body: str, token: str | None = None, data: dict | None = None) -> bool:
    """Send a simple FCM push. Returns True on success.

    - If `token` is provided, sends to that device. Otherwise uses `FCM_DEFAULT_TOPIC`.
    - Keep this minimal; fill `FCM_SERVER_KEY` in config.
    """
    if not FCM_SERVER_KEY:
        logging.getLogger(__name__).warning("FCM server key not configured; skipping FCM")
        return False
    url = "https://fcm.googleapis.com/fcm/send"
    headers = {"Authorization": "key={}".format(FCM_SERVER_KEY), "Content-Type": "application/json"}
    payload = {"notification": {"title": title, "body": body}}
    if data:
        payload["data"] = data
    if token:
        payload["to"] = token
    elif FCM_DEFAULT_TOPIC:
        payload["to"] = FCM_DEFAULT_TOPIC
    else:
        logging.getLogger(__name__).warning("No FCM recipient (token or topic) configured; skipping")
        return False
    try:
        data = json.dumps(payload).encode('utf-8')
        req = _urllib_request.Request(url, data=data, headers=headers, method='POST')
        with _urllib_request.urlopen(req, timeout=8) as resp:
            code = getattr(resp, 'status', None) or getattr(resp, 'getcode', lambda: None)()
            if code and 200 <= int(code) < 300:
                logging.getLogger(__name__).info("FCM sent: %s -> %s", title, body)
                return True
            else:
                logging.getLogger(__name__).warning("FCM POST returned status %s", code)
                return False
    except _urllib_error.HTTPError as he:
        logging.getLogger(__name__).exception("FCM HTTP error: %s", he)
        return False
    except Exception as exc:
        logging.getLogger(__name__).exception("Failed to send FCM: %s", exc)
        return False


def send_whatsapp_message(message: str, phone: str | None = None) -> bool:
    """Send a WhatsApp message via configured API URL. Keep minimal and generic.
    Returns True on success.
    """
    if not WHATSAPP_API_URL or not WHATSAPP_TOKEN:
        logging.getLogger(__name__).warning("WhatsApp API not configured; skipping")
        return False
    to_phone = phone or WHATSAPP_PHONE_NUMBER
    if not to_phone:
        logging.getLogger(__name__).warning("No WhatsApp destination phone configured; skipping")
        return False
    headers = {"Authorization": "Bearer {}".format(WHATSAPP_TOKEN), "Content-Type": "application/json"}
    payload = {"to": to_phone, "type": "text", "text": {"body": message}}
    try:
        data = json.dumps(payload).encode('utf-8')
        req = _urllib_request.Request(WHATSAPP_API_URL, data=data, headers=headers, method='POST')
        with _urllib_request.urlopen(req, timeout=8) as resp:
            code = getattr(resp, 'status', None) or getattr(resp, 'getcode', lambda: None)()
            if code and 200 <= int(code) < 300:
                logging.getLogger(__name__).info("WhatsApp message sent to %s", to_phone)
                return True
            else:
                logging.getLogger(__name__).warning("WhatsApp POST returned status %s", code)
                return False
    except _urllib_error.HTTPError as he:
        logging.getLogger(__name__).exception("WhatsApp HTTP error: %s", he)
        return False
    except Exception as exc:
        logging.getLogger(__name__).exception("Failed to send WhatsApp message: %s", exc)
        return False


def send_panic_alert(elder_id: int | str | None = None, note: str | None = None) -> bool:
    """Send an emergency alert for `elder_id`.

    - Uses `send_whatsapp_message` and `send_fcm_notification` helpers.
    - If `elder_id` is None, attempts to use `LAST_IDENTIFIED`.
    - Runs synchronously but is usually invoked from a background thread.
    """
    try:
        mgr = globals().get('manager')
        elder = None
        if elder_id is None:
            elder_id = globals().get('LAST_IDENTIFIED')
        if elder_id is not None and mgr is not None:
            try:
                elder = mgr.get_elder(elder_id)
            except Exception:
                try:
                    # Allow passing in a string name
                    elder = mgr.get_elder_by_name(str(elder_id))
                except Exception:
                    elder = None

        name = (elder.get('name') if isinstance(elder, dict) else str(elder_id)) if elder is not None else str(elder_id or 'Unknown')
        contact = None
        if isinstance(elder, dict):
            contact = elder.get('emergency_contact') or elder.get('phone') or elder.get('contact')
        # Compose bilingual message (English + Chinese) including contact phone and timestamp
        note_text = note or 'Panic triggered via CLI'
        # Small translation map for common notes
        zh_map = {
            'Panic triggered via CLI': '由CLI觸發緊急警報'
        }
        note_text_zh = zh_map.get(note_text, note_text)
        eid = elder_id or 'Unknown'
        ts = time.strftime('%Y-%m-%d %H:%M:%S')
        contact_display = contact if contact else 'Unknown'
        en = "WARNING Panic alert triggered for elder={} contact={} time={} note={}".format(eid, contact_display, ts, note_text)
        zh = "警告：緊急警報，長者={}，聯絡電話={}，時間={}，備註={}".format(eid, contact_display, ts, note_text_zh)
        body = en + "\n\n" + zh

        sent_any = False
        
        # Channel 1: Use MedicalEmergencyAlert and attempt BOTH SMTP and WhatsApp concurrently
        if HAS_EMERGENCY_ALERT:
            try:
                from emergency_alert import MedicalEmergencyAlert
                extra_data = {"Note": note} if note else None
                alert_sys = MedicalEmergencyAlert()
                subject = "EMERGENCY: {} - CRITICAL".format(name)

                results = {}

                def _smtp_worker():
                    try:
                        results['smtp'] = bool(alert_sys._send_via_smtp(subject, body, [contact] if contact else []))
                    except Exception:
                        logging.getLogger(__name__).exception("SMTP worker exception")
                        results['smtp'] = False

                def _wa_worker():
                    try:
                        if contact:
                            results['whatsapp'] = bool(alert_sys._send_via_textmebot(body, contact))
                        else:
                            results['whatsapp'] = False
                    except Exception:
                        logging.getLogger(__name__).exception("WhatsApp worker exception")
                        results['whatsapp'] = False

                t_smtp = threading.Thread(target=_smtp_worker, daemon=True)
                t_wa = threading.Thread(target=_wa_worker, daemon=True)
                t_smtp.start()
                t_wa.start()
                # Wait up to 15 seconds for both
                t_smtp.join(15)
                t_wa.join(15)

                smtp_ok = bool(results.get('smtp', False))
                wa_ok = bool(results.get('whatsapp', False))

                if smtp_ok:
                    logging.getLogger(__name__).info("Emergency email (SMTP) sent")
                if wa_ok:
                    logging.getLogger(__name__).info("WhatsApp (TextMeBot) sent")

                emergency_success = smtp_ok or wa_ok
                if emergency_success:
                    sent_any = True
                    logging.getLogger(__name__).info("Emergency alert sent via emergency_alert helpers")
            except Exception:
                logging.getLogger(__name__).exception("Failed to use MedicalEmergencyAlert; falling back")
        
        # Channel 2: Direct WhatsApp API (legacy)
        try:
            if contact:
                send_whatsapp_message(body, phone=contact)
                sent_any = True
        except Exception:
            logging.getLogger(__name__).exception("Failed to send WhatsApp panic message")
        
        # Channel 3: FCM Push Notification (legacy)
        try:
            send_fcm_notification("Emergency Alert", body)
            sent_any = True
        except Exception:
            logging.getLogger(__name__).exception("Failed to send FCM panic notification")

        # Log bilingual warning message
        logging.getLogger(__name__).warning("%s | %s", en, zh)
        return bool(sent_any)
    except Exception:
        logging.getLogger(__name__).exception("Unhandled error while sending panic alert")
        return False


def start_person_inactivity_monitor(person_id, person_name: str):
    """Start or restart the inactivity monitor after identifying a person.
    
    After INACTIVITY_TIMEOUT_SECONDS (default 10 min) with no activity,
    prompts to check if the person is still present. If no response within
    INACTIVITY_PROMPT_TIMEOUT seconds, triggers an emergency alert.
    
    This is called after:
    - Successful a/b/c person selection
    - Camera identification confirmation
    """
    global PERSON_IDENTIFIED_TS, PERSON_IDENTIFIED_ID, PERSON_IDENTIFIED_NAME
    global PERSON_INACTIVITY_THREAD, PERSON_INACTIVITY_CANCELLED
    
    # Cancel any existing inactivity monitor
    PERSON_INACTIVITY_CANCELLED = True
    time.sleep(0.1)  # Brief pause to let existing thread notice cancellation
    PERSON_INACTIVITY_CANCELLED = False
    
    # Record identification
    PERSON_IDENTIFIED_TS = time.time()
    PERSON_IDENTIFIED_ID = person_id
    PERSON_IDENTIFIED_NAME = person_name
    globals()['LAST_IDENTIFIED'] = person_id
    globals()['LAST_INPUT_TS'] = PERSON_IDENTIFIED_TS
    
    logging.getLogger(__name__).info(
        "Person identified: %s (ID: %s) - starting %d-minute inactivity monitor",
        person_name, person_id, INACTIVITY_TIMEOUT_SECONDS // 60
    )
    
    def _person_inactivity_watchdog():
        """Background thread that monitors for inactivity after person identification."""
        global PERSON_INACTIVITY_CANCELLED
        
        try:
            # Import msvcrt for Windows key detection
            try:
                import msvcrt as _msvcrt
                MSVCRT_AVAILABLE = True
            except ImportError:
                _msvcrt = None
                MSVCRT_AVAILABLE = False
            
            # Sleep in small increments to allow cancellation
            sleep_remaining = INACTIVITY_TIMEOUT_SECONDS
            while sleep_remaining > 0 and not PERSON_INACTIVITY_CANCELLED:
                time.sleep(min(5, sleep_remaining))
                sleep_remaining -= 5
                
                # Check if there was any activity since identification
                last_input = globals().get('LAST_INPUT_TS', 0)
                if last_input > PERSON_IDENTIFIED_TS:
                    logging.getLogger(__name__).info("Activity detected since identification; resetting timer")
                    return  # Activity detected, exit quietly
            
            if PERSON_INACTIVITY_CANCELLED:
                return
            
            # No activity for the timeout period - prompt the user
            person_name_display = PERSON_IDENTIFIED_NAME or "the identified person"
            timeout_minutes = INACTIVITY_TIMEOUT_SECONDS // 60 if INACTIVITY_TIMEOUT_SECONDS >= 60 else 1
            
            # Get localized prompt message
            try:
                prompt_template = PROMPTS.get(CURRENT_LANG, PROMPTS.get('en', {})).get('inactivity_prompt')
                if prompt_template:
                    prompt_msg = prompt_template.format(
                        minutes=timeout_minutes,
                        name=person_name_display,
                        seconds=INACTIVITY_PROMPT_TIMEOUT
                    )
                else:
                    prompt_msg = "[ALERT] No activity for {} minutes. Is {} still here? Press Enter within {} seconds to confirm...".format(
                        timeout_minutes, person_name_display, INACTIVITY_PROMPT_TIMEOUT
                    )
            except Exception:
                prompt_msg = "[ALERT] No activity for {} minutes. Is {} still here? Press Enter within {} seconds to confirm...".format(
                    timeout_minutes, person_name_display, INACTIVITY_PROMPT_TIMEOUT
                )
            
            print("\n" + "=" * 70)
            print(prompt_msg)
            print("=" * 70)
            
            responded = False
            
            # Windows: use msvcrt.kbhit
            if MSVCRT_AVAILABLE and _msvcrt is not None:
                end_time = time.time() + INACTIVITY_PROMPT_TIMEOUT
                while time.time() < end_time and not PERSON_INACTIVITY_CANCELLED:
                    try:
                        if _msvcrt.kbhit():
                            try:
                                _ = _msvcrt.getwch()
                            except Exception:
                                pass
                            try:
                                _ = sys.stdin.readline()
                            except Exception:
                                pass
                            responded = True
                            break
                    except Exception:
                        break
                    time.sleep(0.2)
            else:
                # POSIX fallback: select on stdin
                try:
                    import select as _select
                    rlist, _, _ = _select.select([sys.stdin], [], [], INACTIVITY_PROMPT_TIMEOUT)
                    if rlist:
                        try:
                            _ = sys.stdin.readline()
                        except Exception:
                            pass
                        responded = True
                except Exception:
                    responded = False
            
            if PERSON_INACTIVITY_CANCELLED:
                return
            
            if responded:
                # Get localized confirmation message
                try:
                    confirm_template = PROMPTS.get(CURRENT_LANG, PROMPTS.get('en', {})).get('inactivity_confirmed')
                    if confirm_template:
                        confirm_msg = confirm_template.format(name=person_name_display)
                    else:
                        confirm_msg = "[OK] Response received - {} is confirmed present. Inactivity timer reset.".format(person_name_display)
                except Exception:
                    confirm_msg = "[OK] Response received - {} is confirmed present. Inactivity timer reset.".format(person_name_display)
                print(confirm_msg)
                globals()['LAST_INPUT_TS'] = time.time()
                # Restart the monitor
                start_person_inactivity_monitor(PERSON_IDENTIFIED_ID, PERSON_IDENTIFIED_NAME)
                return
            
            # No response - trigger emergency alert!
            try:
                alarm_template = PROMPTS.get(CURRENT_LANG, PROMPTS.get('en', {})).get('inactivity_alarm')
                if alarm_template:
                    alarm_msg = alarm_template.format(name=person_name_display)
                else:
                    alarm_msg = "[EMERGENCY] No response! {} may need help - triggering alarm!".format(person_name_display)
            except Exception:
                alarm_msg = "[EMERGENCY] No response! {} may need help - triggering alarm!".format(person_name_display)
            
            print("\n" + "!" * 70)
            print(alarm_msg)
            print("!" * 70 + "\n")
            
            try:
                threading.Thread(
                    target=send_panic_alert,
                    args=(PERSON_IDENTIFIED_ID, "No response to presence check after {} minutes of inactivity".format(INACTIVITY_TIMEOUT_SECONDS // 60)),
                    daemon=True
                ).start()
            except Exception:
                logging.getLogger(__name__).exception("Failed to dispatch inactivity panic alert")
                
        except Exception:
            logging.getLogger(__name__).exception("Person inactivity watchdog failed")
    
    # Start the watchdog thread
    try:
        PERSON_INACTIVITY_THREAD = threading.Thread(target=_person_inactivity_watchdog, daemon=True)
        PERSON_INACTIVITY_THREAD.start()
        timeout_minutes = INACTIVITY_TIMEOUT_SECONDS // 60 if INACTIVITY_TIMEOUT_SECONDS >= 60 else 1
        try:
            started_template = PROMPTS.get(CURRENT_LANG, PROMPTS.get('en', {})).get('inactivity_started')
            if started_template:
                started_msg = started_template.format(name=person_name, minutes=timeout_minutes)
            else:
                started_msg = "[INFO] Inactivity monitor started for {} - will check in {} minutes".format(person_name, timeout_minutes)
        except Exception:
            started_msg = "[INFO] Inactivity monitor started for {} - will check in {} minutes".format(person_name, timeout_minutes)
        print(started_msg)
    except Exception:
        logging.getLogger(__name__).exception("Could not start person inactivity watchdog")


def reset_inactivity_timer():
    """Call this whenever there is user activity to reset the inactivity timer."""
    globals()['LAST_INPUT_TS'] = time.time()


def _missed_dose_monitor(manager, reminder, check_interval_seconds: int = 300, lookback_hours: int = 2):
    """Background thread that detects missed doses (no recorded `doses_taken` within
    `lookback_hours` after scheduled time) and sends notifications once per schedule/date.
    """
    logging.getLogger(__name__).info("Starting missed-dose monitor (interval=%ds, lookback=%dh)", check_interval_seconds, lookback_hours)
    while True:
        try:
            elders = manager.get_all_elders()
            now = time.time()
            today_str = time.strftime("%Y-%m-%d")
            with manager.locked_cursor() as cursor:
                for elder in elders:
                    elder_id = elder.get('elder_id')
                    # Fetch schedules for this elder that are active today
                    cursor.execute('''
                        SELECT s.schedule_id, s.time_of_day, m.med_name
                        FROM schedules s
                        JOIN medications m ON s.med_id = m.med_id
                        WHERE m.elder_id = ?
                          AND DATE(s.start_date) <= DATE('now')
                          AND DATE(s.end_date) >= DATE('now')
                    ''', (elder_id,))
                    for row in cursor.fetchall():
                        schedule_id, time_str, med_name = row
                        # Build datetime for today at scheduled time
                        try:
                            sched_dt = time.strptime(time_str, "%H:%M")
                            sched_ts = time.mktime((time.localtime().tm_year, time.localtime().tm_mon, time.localtime().tm_mday, sched_dt.tm_hour, sched_dt.tm_min, 0, 0, 0, -1))
                        except Exception:
                            continue
                        # If scheduled time occurred between now-lookback and now (i.e. potentially missed)
                        if sched_ts <= now and sched_ts >= (now - lookback_hours * 3600):
                            # check doses_taken for this schedule today
                            cursor.execute('SELECT COUNT(*) FROM doses_taken WHERE schedule_id = ? AND date = ?', (schedule_id, today_str))
                            cnt = cursor.fetchone()[0]
                            key = (schedule_id, today_str)
                            if cnt == 0 and MISSED_ALERTS_SENT.get(key) is None:
                                # Send notification(s)
                                title = "Missed dose: {}".format(med_name)
                                body = "{} may have missed {} scheduled at {}.".format(elder.get('name'), med_name, time_str)
                                send_fcm_notification(title, body)
                                send_whatsapp_message(body, phone=elder.get('phone'))
                                MISSED_ALERTS_SENT[key] = time.time()
                                logging.getLogger(__name__).warning("Missed dose detected: elder=%s med=%s schedule=%s", elder_id, med_name, schedule_id)
            # cleanup old keys older than 24h
            cutoff = time.time() - 24 * 3600
            for k, ts in list(MISSED_ALERTS_SENT.items()):
                if ts < cutoff:
                    MISSED_ALERTS_SENT.pop(k, None)
        except Exception:
            logging.getLogger(__name__).exception("Error in missed-dose monitor")
        time.sleep(check_interval_seconds)



def _normalize_confidence(value):
    try:
        conf = float(value)
    except Exception:
        return 0.0
    if conf < 0.0:
        return 0.0
    if conf > 1.0:
        if conf <= 100.0:
            conf = conf / 100.0
        else:
            conf = 1.0
    if conf >= 1.0:
        conf = 0.999
    return conf


def summarize_recent_identifications(max_entries=None, max_age=None):
    samples = []
    with RECENT_IDENTIFICATIONS_LOCK:
        if RECENT_IDENTIFICATIONS:
            samples = list(RECENT_IDENTIFICATIONS)
    if not samples:
        return None

    if max_entries is not None:
        samples = samples[-int(max_entries):]

    now_ts = time.time()
    if max_age is not None:
        filtered = []
        for sample in samples:
            ts = sample.get('ts') if isinstance(sample, dict) else None
            if ts is None or now_ts - ts <= max_age:
                filtered.append(sample)
        samples = filtered
    if not samples:
        return None

    stats = {}
    for sample in samples:
        pid = sample.get('person_id') if isinstance(sample, dict) else None
        name = sample.get('name') if isinstance(sample, dict) else None
        label = sample.get('label') if isinstance(sample, dict) else None
        key = pid if pid is not None else (name or label or 'Unknown')
        entry = stats.setdefault(
            key,
            {
                'count': 0,
                'conf_sum': 0.0,
                'name': name or label or 'Unknown',
                'person_id': pid,
                'latest_ts': 0.0,
            },
        )
        entry['count'] += 1
        try:
            entry['conf_sum'] += _normalize_confidence(sample.get('confidence'))
        except Exception:
            pass
        ts = sample.get('ts') if isinstance(sample, dict) else None
        if isinstance(ts, (int, float)):
            entry['latest_ts'] = max(entry['latest_ts'], ts)

    total = sum(v['count'] for v in stats.values())
    if total == 0:
        return None

    best = None
    for data in stats.values():
        avg_conf = data['conf_sum'] / data['count'] if data['count'] else 0.0
        candidate = {
            'person_id': data['person_id'],
            'name': data['name'],
            'count': data['count'],
            'avg_confidence': avg_conf,
            'support': data['count'] / total,
            'total_samples': total,
            'latest_timestamp': data['latest_ts'] or None,
        }
        if best is None:
            best = candidate
            continue
        if candidate['count'] > best['count']:
            best = candidate
            continue
        if candidate['count'] == best['count'] and candidate['avg_confidence'] > best['avg_confidence']:
            best = candidate
            continue
        if (
            candidate['count'] == best['count']
            and abs(candidate['avg_confidence'] - best['avg_confidence']) < 1e-6
            and (candidate['latest_timestamp'] or 0.0) > (best['latest_timestamp'] or 0.0)
        ):
            best = candidate

    return best


def _last4_match(elder: dict | None, code: str) -> bool:
    """Return True if `code` matches last 4 digits of elder's external_id or phone.
    `code` may include non-digit characters; we compare only the trailing 4 digits.
    """
    if not code:
        return False
    try:
        digits = re.sub(r"\D", "", str(code))
    except Exception:
        digits = ''.join([c for c in str(code) if c.isdigit()])
    if len(digits) > 4:
        digits = digits[-4:]
    if elder is None:
        return False
    # external_id
    ext = str(elder.get('external_id') or elder.get('external') or '')
    ext_digits = re.sub(r"\D", "", ext)
    if len(ext_digits) >= 4 and ext_digits[-4:] == digits:
        return True
    # phone (strip non-digits)
    phone = str(elder.get('phone') or '')
    phone_digits = re.sub(r"\D", "", phone)
    if len(phone_digits) >= 4 and phone_digits[-4:] == digits:
        return True
    return False


# Group helpers into a single class to improve readability for readers.
class Application:
    def __init__(self):
        self.fcm_key = FCM_SERVER_KEY
        self.fcm_topic = FCM_DEFAULT_TOPIC
        self.whatsapp_url = WHATSAPP_API_URL
        self.whatsapp_token = WHATSAPP_TOKEN
        self.whatsapp_phone = WHATSAPP_PHONE_NUMBER
        self.missed_alerts = MISSED_ALERTS_SENT

    # Wrap the existing module-level notification behavior so callers use methods
    def send_fcm_notification(self, title: str, body: str, token: str | None = None, data: dict | None = None) -> bool:
        if '_orig_send_fcm_notification' in globals() and globals()['_orig_send_fcm_notification']:
            return globals()['_orig_send_fcm_notification'](title, body, token=token, data=data)
        return False

    def send_whatsapp_message(self, message: str, phone: str | None = None) -> bool:
        # call the backed-up original implementation (set below)
        if '_orig_send_whatsapp_message' in globals() and globals()['_orig_send_whatsapp_message']:
            return globals()['_orig_send_whatsapp_message'](message, phone)
        return False

    def adjust_image_brightness(self, path: str, target_mean: float = 120.0, max_factor: float = 2.0) -> bool:
        # If an original adjust_image_brightness exists, call it; otherwise no-op
        fn = globals().get('_orig_adjust_image_brightness')
        if fn:
            try:
                return fn(path, target_mean, max_factor)
            except Exception:
                return False
        return False

    def last4_match(self, elder: dict | None, code: str) -> bool:
        return globals().get('_orig__last4_match', _last4_match)(elder, code)

    def summarize_recent_identifications(self, max_entries=None, max_age=None):
        return globals().get('_orig_summarize_recent_identifications', summarize_recent_identifications)(max_entries=max_entries, max_age=max_age)


# Create a single application object for easier consumption by readers/tools
# Back up the original helper functions so the class can call them safely
_orig_send_fcm_notification = globals().get('send_fcm_notification')
_orig_send_whatsapp_message = globals().get('send_whatsapp_message')
_orig_adjust_image_brightness = globals().get('adjust_image_brightness')
_orig_summarize_recent_identifications = globals().get('summarize_recent_identifications')
_orig__last4_match = globals().get('_last4_match')

APP = Application()

# Rebind common helper names to methods on APP for consistency (keeps existing API)
send_fcm_notification = APP.send_fcm_notification
send_whatsapp_message = APP.send_whatsapp_message
adjust_image_brightness = APP.adjust_image_brightness
_last4_match = APP.last4_match
summarize_recent_identifications = APP.summarize_recent_identifications


def display_person(person_id, manager, reminder, show_medications=False):
    """Display a person's basic information. Medications and schedules are hidden by default
    for privacy; pass `show_medications=True` to reveal them. If `show_medications` is False,
    the function will prompt the user whether to show medication details."""
    person = manager.get_elder(person_id)

    if person is None:
        print("\n[ERROR] Person {} not found\n".format(person_id))
        return

    # Basic info
    print("\n" + "=" * 80)
    print("PERSON {}: {}".format(person_id, person['name'].upper()))
    print("=" * 80)

    print("\n[BASIC INFO]")
    print("  Name:    {}".format(person['name']))
    print("  Age:     {}".format(person['age']))
    if 'external_id' in person:
        print("  External ID: {}".format(person.get('external_id')))
    print("  Phone:   {}".format(person['phone']))
    print("  Contact: {}".format(person['emergency_contact']))
    print("  Address: {}".format(person['address']))

    # If medications are not requested yet, ask the user if they want to see them
    if not show_medications:
        ans = input("Show medications and schedule for this person? (yes/no) > ").strip().lower()
        if ans in ('y', 'yes'):
            show_medications = True

    if show_medications:
        medications = manager.get_medications(person_id)
        schedules = manager.get_schedules(elder_id=person_id)
        due_meds = reminder.get_due_medications(person_id, within_hours=4)
        compliance = reminder.get_compliance_report(person_id, days=7)

        print("\n[MEDICATIONS] ({}):".format(len(medications)))
        for med in medications:
            print("  - {} ({})".format(med['name'], med['dosage']))
            print("    Reason: {}".format(med['reason']))

        print("\n[SCHEDULE] ({} times/day):".format(len(schedules)))
        for sched in schedules:
            print("  - {}: {}".format(sched['time'], sched['frequency']))

        print("\n[DUE NOW]:")
        if due_meds:
            for med in due_meds:
                print("  - {} at {}".format(med['name'], med['time']))
        else:
            print("  (None)")

        print("\n[7-DAY COMPLIANCE]:")
        for comp in compliance['medications']:
            pct = comp['compliance_percent']
            print("  - {}: {}/{} ({:.1f}%)".format(comp['name'], comp['taken'], comp['scheduled'], pct))

    print("\n" + "=" * 80 + "\n")
    # Show options to the user after displaying the person's information
    while (1):
        try:
            print(PROMPTS[CURRENT_LANG]["menu_options_person"])
        except Exception:
            print(PROMPTS['en']["menu_options_person"])
        choice = input(PROMPTS[CURRENT_LANG].get("input_option", "Enter option > ")).strip().lower()
        if not choice:
            continue
        elif choice in ("back", "b"):
            # Return to the main menu without printing the full dataset
            break
        elif choice == "all":
            display_all(manager)
            break
        elif choice in ("exit", "quit", "q"):
            print(FAREWELLS.get(CURRENT_LANG, FAREWELLS['en']))
            sys.exit(0)
        else:
            print("[ERROR] Unknown option: {}\n".format(choice))

# (Duplicate block removed) The file contains a single `display_all` and `main` implementation further
# down; earlier duplicate copies have been removed to shrink file size.
def display_all(manager):
    """Display all persons in database."""
    all_persons = manager.get_all_elders()
    
    print("\n" + "=" * 80)
    print("ALL PERSONS IN DATABASE")
    print("=" * 80)
    print("\nTotal: {} persons\n".format(len(all_persons)))
    
    for p in all_persons:
        # Do not display external IDs here to protect privacy; show name and age only
        print("  [{}] {} - Age {}".format(p['elder_id'], p['name'], p['age']))
    
    print("\n" + "=" * 80 + "\n")

    # Show options to the user after listing everyone in the database
    while True:
        try:
            print(PROMPTS[CURRENT_LANG]["menu_options_all"])
        except Exception:
            print(PROMPTS['en']["menu_options_all"])
        choice = input(PROMPTS[CURRENT_LANG].get("input_option", "Enter option > ")).strip().lower()
        if not choice:
            continue
        if choice in ("back", "b"):
            break
        if choice in ("a", "b", "c"):
            # Quick-select mapped to the displayed list order: a -> first person, b -> second, c -> third
            idx = ord(choice) - ord('a')
            if idx < 0 or idx >= len(all_persons):
                print("[ERROR] Invalid selection: {}".format(choice))
                continue
            selected = all_persons[idx]
            reminder = globals().get('reminder')
            if reminder is None:
                print("[WARN] Reminder object not available here; returning to menu.")
                break
            display_person(selected.get('elder_id'), manager, reminder)
            break

        if choice.startswith("person "):
            try:
                pid = int(choice.split()[1])
                # The main loop normally provides a `reminder` object. Try to get it from
                # the module globals; if it's not present, warn and return to the menu.
                reminder = globals().get('reminder')
                if reminder is None:
                    print("[WARN] Reminder object not available here; returning to menu.")
                    break
                display_person(pid, manager, reminder)
            except (IndexError, ValueError):
                print("[ERROR] Use: person <id> (e.g., person 1)")
            continue
        if choice in ("exit", "quit", "q"):
            print(FAREWELLS.get(CURRENT_LANG, FAREWELLS['en']))
            sys.exit(0)
        print("[ERROR] Unknown option: {}\n".format(choice))


def main():
    """Main programme - Interactive medication management system."""
    # Parse minimal CLI args (language)
    parser = argparse.ArgumentParser(description="Elder Medication Management System")
    parser.add_argument("--lang", choices=["en", "zh"], default=None, help="Interface language (en/zh)")
    parser.add_argument("--demo", action="store_true", help="Run integrated non-invasive demo sequence and exit")
    parser.add_argument("--panic-demo", action="store_true", help="Run a panic/WhatsApp demo (TEST_MODE) and exit")
    args = parser.parse_args()
    # Set global language
    global CURRENT_LANG
    CURRENT_LANG = args.lang
    # If running a non-interactive demo (panic-demo), default language to English
    if args.panic_demo and CURRENT_LANG is None:
        CURRENT_LANG = 'en'
    # Also handle cases where argparse did not parse (direct argv check)
    if CURRENT_LANG is None and "--panic-demo" in sys.argv:
        CURRENT_LANG = 'en'

    # If no CLI flag provided, offer a startup prompt; default is English
    if CURRENT_LANG is None:
        print("=" * 50)
        print("請選擇語言 / Please select your language (default would be English):")
        print("1. 中文 (Cantonese/Chinese(Traditional))")
        print("2. English (default)")
        print("(Press Enter to accept default)")
        print("=" * 50)
        while True:
            choice = input("Enter 1 or 2 [default 2] > ").strip()
            if choice == "1":
                CURRENT_LANG = "zh"
                break
            if choice == "" or choice == "2":
                CURRENT_LANG = "en"
                break
            print("無效選擇，請輸入 1 或 2 / Invalid choice. Please enter 1 or 2.")

    # Greet user in selected language
    greetings = {"en": "Welcome to SmartElderCare System!", "zh": "歡迎使用智慧長者用藥管理系統！"}
    print("\n{}\n".format(greetings.get(CURRENT_LANG, greetings['en'])))
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    logger = logging.getLogger(__name__)
    db, manager = setup_personalized_medications()
    reminder = MedicationReminder(manager)

    # If user requested a panic demo, run a simulated panic alert and exit
    if args.panic_demo:
        print("Running panic demo (TEST_MODE=1)...")
        os.environ["TEST_MODE"] = "1"
        try:
            # Try to use the panic helper; pass the first elder ID if available
            first_id = None
            try:
                first_id = next(iter(manager.list_elder_ids()))
            except Exception:
                try:
                    # fallback: use 1 if manager provides get_elder
                    first_id = 1
                except Exception:
                    first_id = None

            success = send_panic_alert(first_id, note="Demo panic test")
            print("Panic demo result: {}".format('SUCCESS' if success else 'FAILED'))
        except Exception as e:
            print("Panic demo encountered error: {}".format(e))
        return

    # Track program start and last input time for inactivity detection
    global START_TIME, LAST_INPUT_TS
    START_TIME = time.time()
    LAST_INPUT_TS = START_TIME

    # Cross-platform non-blocking key detection: prefer msvcrt on Windows
    try:
        import msvcrt as _msvcrt  # type: ignore
        MSVCRT_AVAILABLE = True
    except Exception:
        _msvcrt = None
        MSVCRT_AVAILABLE = False

    def _inactivity_watchdog(start_ts, timeout_seconds: int = 600, prompt_timeout: int = 30):
        """If no input has been received since `start_ts` after `timeout_seconds`,
        prompt the operator. If the operator does not respond within
        `prompt_timeout` seconds, dispatch a panic alert in background.
        This runs once (one-shot) after `timeout_seconds` from program start.
        """
        try:
            # Sleep until the first check time
            time.sleep(timeout_seconds)
            # If any input happened since start, abort
            last = globals().get('LAST_INPUT_TS', 0)
            if last and last > start_ts:
                return

            # No input; ask operator if they're still present
            try:
                msg = "[WARN] No user input detected for {} minutes. Are you still there? Press Enter within {} seconds to cancel panic...".format(int(timeout_seconds/60), prompt_timeout)
                print(msg)
            except Exception:
                print('[WARN] No user input detected - responding will cancel panic.')

            responded = False
            # Windows: use msvcrt.kbhit to wait for keypress
            if MSVCRT_AVAILABLE and _msvcrt is not None:
                end = time.time() + prompt_timeout
                while time.time() < end:
                    try:
                        if _msvcrt.kbhit():
                            # consume the key(s) and any following line
                            try:
                                _ = _msvcrt.getwch()
                            except Exception:
                                pass
                            try:
                                # Read the rest of the current line if available
                                _ = sys.stdin.readline()
                            except Exception:
                                pass
                            responded = True
                            break
                    except Exception:
                        break
                    time.sleep(0.2)
            else:
                # POSIX fallback: select on stdin
                try:
                    import select as _select
                    rlist, _, _ = _select.select([sys.stdin], [], [], prompt_timeout)
                    if rlist:
                        try:
                            _ = sys.stdin.readline()
                        except Exception:
                            pass
                        responded = True
                except Exception:
                    # If select unavailable or fails, fall back to no-response
                    responded = False

            if responded:
                print('[OK] User response detected; inactivity panic cancelled.')
                # update last input timestamp so further checks will be aware
                globals()['LAST_INPUT_TS'] = time.time()
                return

            # No response -> dispatch panic alert in background
            try:
                print('[WARN] No response to inactivity prompt; dispatching panic alert.')
                threading.Thread(target=send_panic_alert, args=(None, 'No response to inactivity prompt'), daemon=True).start()
            except Exception:
                logging.getLogger(__name__).exception('Failed to dispatch inactivity panic')
        except Exception:
            logging.getLogger(__name__).exception('Inactivity watchdog failed')

    # Launch the inactivity watchdog as a daemon thread (one-shot)
    try:
        threading.Thread(target=_inactivity_watchdog, args=(START_TIME,), daemon=True).start()
    except Exception:
        logging.getLogger(__name__).exception('Could not start inactivity watchdog thread')

    # If demo flag provided, run a short integrated demo sequence using existing helpers
    if args.demo:
        try:
            def run_inline_demo(manager, reminder):
                print("[DEMO] Running integrated demo sequence...")
                timeline = []
                def rec(ev, details=None):
                    ts = time.strftime('%Y-%m-%d %H:%M:%S')
                    timeline.append({'ts': ts, 'event': ev, 'details': details})
                    print('[DEMO]', ts, ev, '-', details or '')

                rec('demo_start', 'Integrated demo started')
                # Simulate identifications
                now = time.time()
                for i in range(5):
                    s = {'person_id': 1, 'name': 'Demo Elder', 'label': 'Demo Elder', 'confidence': 0.8 - i * 0.05, 'ts': now - (5 - i)}
                    try:
                        with RECENT_IDENTIFICATIONS_LOCK:
                            RECENT_IDENTIFICATIONS.append(s)
                            RECENT_IDENTIFICATIONS[:] = RECENT_IDENTIFICATIONS[-RECENT_MAX:]
                    except Exception:
                        RECENT_IDENTIFICATIONS.append(s)
                    rec('camera_frame', {'frame': i + 1, 'identified': s['name'], 'confidence': s['confidence']})
                    time.sleep(0.12)

                rec('camera_stop', 'Summarizing recent identifications')
                best = summarize_recent_identifications(max_entries=5, max_age=SUMMARY_MAX_AGE_SECONDS)
                rec('identification_summary', best)

                # Simulate medication reminder
                rec('reminder_trigger', 'Demo medication reminder')
                meds = manager.get_medications(1) if hasattr(manager, 'get_medications') else []
                med_name = meds[0]['name'] if meds else 'DemoMed'
                title = 'Reminder: {}'.format(med_name)
                body = '{} is due now.'.format((manager.get_elder(1) or {}).get('name', 'Demo Elder'))
                rec('reminder_send', {'title': title, 'body': body})
                try:
                    send_fcm_notification(title, body)
                    send_whatsapp_message(body, phone=(manager.get_elder(1) or {}).get('phone'))
                except Exception:
                    pass

                # Simulate fall -> panic
                rec('fall_simulation', 'Simulating fall detection')
                try:
                    send_panic_alert(elder_id=1, note='demo: simulated fall from integrated demo')
                    rec('panic_sent', {'result': True})
                except Exception as _e:
                    rec('panic_sent', {'result': False, 'error': str(_e)})

                rec('demo_end', 'Integrated demo finished')
                # save timeline for later use
                try:
                    out = Path(__file__).parent / 'demo_recordings'
                    out.mkdir(exist_ok=True)
                    fname = out / ('inline_demo_{}.json'.format(int(time.time())))
                    with open(fname, 'w', encoding='utf-8') as f:
                        json.dump(timeline, f, indent=2, ensure_ascii=False)
                    print('[DEMO] Timeline saved to {}'.format(str(fname)))
                except Exception:
                    pass

            run_inline_demo(manager, reminder)
        except Exception:
            logging.getLogger(__name__).exception('Integrated demo failed')
        return
    # Print the localized command list
    try:
        print(PROMPTS[CURRENT_LANG]["command_list"])
    except Exception:
        # Fallback to English list if something went wrong
        print(PROMPTS['en']["command_list"])
    # Variables that track the camera HTTP server while it's running
    _httpd = None
    _server_thread = None
    def start_camera_server(port=8000):
        nonlocal _httpd, _server_thread
        if _httpd is not None:
            print("[INFO] Camera server already running on port {}".format(_httpd.server_address[1]))
            return
        root = Path(__file__).parent.resolve()
        # Initialize (or reuse) the detector and optional identifier used by the /detect endpoint
        global DETECTOR, IDENTIFIER
        try:
            DETECTOR
        except NameError:
            try:
                # Try to prepare YOLOv4 config & weights if helper is available
                from yoloV4.yolov4_detector import YOLOv4PersonDetector, setup_yolov4_config, download_yolov4_weights
                try:
                    # Ensure config files (cfg, names) exist; this is small and fast
                    setup_yolov4_config()
                except Exception as _e:
                    print("[YOLOV4] Could not ensure config files: {}".format(_e))
                # If weights are missing, attempt a best-effort download (may be large)
                weights_path = os.path.join(str(Path(__file__).parent.resolve()), 'yoloV4', 'yolov4.weights')
                if not os.path.exists(weights_path):
                    try:
                        print("[YOLOV4] Weights missing, attempting download (this may take several minutes)...")
                        download_yolov4_weights()
                    except Exception as _e:
                        print("[YOLOV4] Could not download weights automatically: {}".format(_e))
                # Instantiate the real detector (it will choose fallback if required)
                DETECTOR = YOLOv4PersonDetector()
            except Exception as _e:
                print("[WARN] Real YOLOv4 detector not available: {}\n[FALLBACK] Using demo/mock detector".format(_e))
                # If the real detector can't be created, fall back to the demo/mock detector
                DETECTOR = YOLOv4Detector()
        # Log which detector implementation was created
        try:
            logging.getLogger(__name__).info("DETECTOR instantiated: %s", type(DETECTOR))
        except Exception:
            pass
        # Try to create a higher-level identifier (an object that can identify persons or medications)
        if 'IDENTIFIER' not in globals() or IDENTIFIER is None:
            try:
                from yoloV4.yolov4_detector import YOLOv4MedicationDetector
                IDENTIFIER = YOLOv4MedicationDetector()
            except Exception:
                try:
                    from yoloV4.yolov4_demo import YOLOv4withML
                    IDENTIFIER = YOLOv4withML(DETECTOR)
                except Exception:
                    IDENTIFIER = None
        # Log which identifier (if any) is being used
        try:
            logging.getLogger(__name__).info("IDENTIFIER instantiated: %s", type(IDENTIFIER) if IDENTIFIER is not None else None)
        except Exception:
            pass
        # Create a tiny favicon if one doesn't exist so the browser won't request a missing file
        try:
            favicon_path = root / "favicon.ico"
            if not favicon_path.exists():
                png_base64 = b'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8Xw8AAoMBgP9sR3sAAAAASUVORK5CYII='
                favicon_path.write_bytes(base64.b64decode(png_base64))
        except Exception as _e:
            print("[WARN] Could not create favicon.ico: {}".format(_e))

        # HTTP handler for the camera UI. It accepts POST /detect with a base64 image payload.
        class CameraRequestHandler(http.server.SimpleHTTPRequestHandler):
            def _set_json_headers(self, code=200):
                self.send_response(code)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()

            def do_OPTIONS(self):
                self.send_response(200)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
                self.send_header('Access-Control-Allow-Headers', 'Content-Type')
                self.end_headers()

            def do_GET(self):
                # Provide a simple status endpoint the camera page can poll
                if self.path.startswith('/status'):
                    try:
                        det_info = None
                        id_info = None
                        yolo_loaded = False
                        use_cascade = False
                        use_simulated = False
                        if 'DETECTOR' in globals() and globals().get('DETECTOR') is not None:
                            D = globals().get('DETECTOR')
                            det_info = str(type(D))
                            yolo_loaded = bool(getattr(D, 'net', None) is not None)
                            use_cascade = bool(getattr(D, 'use_cascade', False))
                            use_simulated = bool(getattr(D, 'use_simulated', False))
                        if 'IDENTIFIER' in globals() and globals().get('IDENTIFIER') is not None:
                            id_info = str(type(globals().get('IDENTIFIER')))
                        payload = {
                            'detector': det_info,
                            'identifier': id_info,
                            'yolo_loaded': yolo_loaded,
                            'use_cascade': use_cascade,
                            'use_simulated': use_simulated
                        }
                        self._set_json_headers(200)
                        self.wfile.write(json.dumps(payload).encode('utf-8'))
                        return
                    except Exception:
                        pass
                # Fallback to normal file serving for other GET paths
                try:
                    return super().do_GET()
                except Exception:
                    try:
                        self.send_response(404)
                        self.end_headers()
                    except Exception:
                        pass

            def do_POST(self):
                try:
                    logging.getLogger(__name__).info("HTTP POST %s from %s", self.path, getattr(self, 'client_address', None))
                    # Support a confirmation endpoint used by the Camera UI
                    if self.path == '/confirm':
                        length = int(self.headers.get('Content-Length', 0))
                        body = self.rfile.read(length)
                        try:
                            payload = json.loads(body.decode('utf-8'))
                        except Exception as e:
                            self._set_json_headers(400)
                            self.wfile.write(json.dumps({'error': 'invalid json', 'details': str(e)}).encode('utf-8'))
                            return
                        confirmed = bool(payload.get('confirmed'))
                        info = payload.get('info') or {}
                        raw_label = ''
                        if isinstance(info, dict):
                            raw_label = info.get('label') or ''
                        elif isinstance(info, str):
                            raw_label = info
                        logging.getLogger(__name__).info("Identification confirmation received: confirmed=%s info=%s", confirmed, raw_label)

                        # Normalize label and strip trailing confidence tokens like ' 86%'
                        name_candidate = raw_label
                        try:
                            if isinstance(name_candidate, str) and name_candidate.startswith('Is this person:'):
                                name_candidate = name_candidate.replace('Is this person:', '').replace('?', '').strip()
                        except Exception:
                            pass
                        import re as _re
                        if isinstance(name_candidate, str):
                            name_candidate = _re.sub(r"\s+\d+%$", '', name_candidate).strip()

                        elder = None
                        if name_candidate:
                            try:
                                elder = manager.get_elder_by_name(name_candidate)
                            except Exception as _e:
                                logging.getLogger(__name__).warning("Name lookup failed: %s", _e)

                        # Enqueue the confirmation (client may have clicked yes or no).
                        entry = {
                            'client_confirmed': confirmed,
                            'elder_id': elder['elder_id'] if elder else None,
                            'label': name_candidate
                        }
                        try:
                            PENDING_CONFIRMATIONS.put(entry)
                        except Exception as _e:
                            logging.getLogger(__name__).exception("Could not enqueue pending confirmation: %s", _e)

                        self._set_json_headers(200)
                        self.wfile.write(json.dumps({'status': 'ok', 'confirmed': confirmed}).encode('utf-8'))
                        return

                    # Support a stop endpoint so the web UI can request the server
                    # to finalize analysis and stop the camera cleanly.
                    if self.path == '/stop':
                        try:
                            globals()['CAMERA_AUTO_STOP_TRIGGERED'] = True
                            logging.getLogger(__name__).info("/stop received: set CAMERA_AUTO_STOP_TRIGGERED=True")
                            candidate = summarize_recent_identifications(
                                max_entries=globals().get('CAMERA_AUTOSTOP_N', 10),
                                max_age=SUMMARY_MAX_AGE_SECONDS,
                            )
                        except Exception:
                            logging.getLogger(__name__).exception("Error summarizing recent identifications during /stop")
                            candidate = None

                        if candidate:
                            person_id = candidate.get('person_id')
                            name = candidate.get('name') or candidate.get('label') or 'Unknown'
                            confidence = candidate.get('avg_confidence', 0.0) or candidate.get('confidence', 0.0)
                            support_pct = (candidate.get('support', 0.0) or 0.0) * 100.0
                            logging.getLogger(__name__).info(
                                "/STOP IDENTIFICATION COMPLETE: %s (ID=%s, SUPPORT=%.0f%%, AVG_CONF=%.1f%%)",
                                name.upper(),
                                person_id,
                                support_pct,
                                confidence * 100.0,
                            )
                            try:
                                msg = PROMPTS.get(CURRENT_LANG, PROMPTS.get('en', {})).get('press_enter_to_proceed')
                                if not msg:
                                    msg = PROMPTS['en'].get('press_enter_to_proceed', 'Press Enter to proceed to the next step...')
                                print(msg)
                            except Exception:
                                print('Press Enter to proceed to the next step...')
                            if person_id:
                                globals()['LAST_IDENTIFIED'] = person_id
                                # Start inactivity monitor for the camera-identified person
                                try:
                                    start_person_inactivity_monitor(person_id, name)
                                except Exception:
                                    logging.getLogger(__name__).exception("Failed to start inactivity monitor for camera ID")
                            globals()['SKIP_PENDING_PROMPT'] = True
                            globals()['SKIP_PENDING_PRINTED'] = False
                        else:
                            logging.getLogger(__name__).info("/stop: no candidate selected")
                        self._set_json_headers(200)
                        self.wfile.write(json.dumps({'status': 'ok', 'auto_stop': True}).encode('utf-8'))
                        return

                    if self.path != '/detect':
                        # For any other POST path not handled above, return a JSON 404
                        try:
                            self._set_json_headers(404)
                            self.wfile.write(json.dumps({'error': 'unsupported path', 'path': self.path}).encode('utf-8'))
                        except Exception:
                            try:
                                self.send_response(404)
                                self.end_headers()
                            except Exception:
                                pass
                        return

                    # Read and parse the JSON request body for /detect
                    length = int(self.headers.get('Content-Length', 0))
                    body = self.rfile.read(length)
                    try:
                        payload = json.loads(body.decode('utf-8'))
                        data_url = payload.get('image')
                    except Exception as e:
                        self._set_json_headers(400)
                        self.wfile.write(json.dumps({'error': 'invalid json', 'details': str(e)}).encode('utf-8'))
                        return

                    if not data_url or not data_url.startswith('data:'):
                        self._set_json_headers(400)
                        self.wfile.write(json.dumps({'error': 'missing image data'}).encode('utf-8'))
                        return

                    # Decode the data URL payload into raw image bytes
                    header, b64 = data_url.split(',', 1)
                    try:
                        img_bytes = base64.b64decode(b64)
                    except Exception as e:
                        self._set_json_headers(400)
                        self.wfile.write(json.dumps({'error': 'bad base64', 'details': str(e)}).encode('utf-8'))
                        return

                    # Save the image bytes to a temporary JPEG file on disk
                    tmp_name = str(root / "frame_{}.jpg".format(uuid.uuid4().hex))
                    try:
                        with open(tmp_name, 'wb') as f:
                            f.write(img_bytes)
                    except Exception as e:
                        self._set_json_headers(500)
                        self.wfile.write(json.dumps({'error': 'could not save file', 'details': str(e)}).encode('utf-8'))
                        return

                    # Adjust brightness if the image is too dark to improve detection
                    def adjust_image_brightness(path: str, target_mean: float = 120.0, max_factor: float = 2.0) -> bool:
                        """Try to increase brightness of image at `path`.

                        Uses OpenCV+NumPy when available; falls back to Pillow when not.
                        This implementation reads raw bytes and decodes them to avoid
                        issues with `np.fromfile` and ensures a NumPy array is passed
                        to OpenCV functions so cv2._InputArray assertions won't fail.
                        """
                        try:
                            if _cv2 is not None and _np is not None:
                                # Read bytes reliably (works with unicode paths)
                                try:
                                    with open(path, 'rb') as _f:
                                        img_bytes = _f.read()
                                except Exception:
                                    return False
                                if not img_bytes:
                                    return False
                                arr = _np.frombuffer(img_bytes, dtype=_np.uint8)
                                img = _cv2.imdecode(arr, _cv2.IMREAD_COLOR)
                                if img is None or not isinstance(img, _np.ndarray):
                                    return False
                                # Ensure image has at least 2 dims
                                if img.ndim < 2:
                                    return False
                                # If image is grayscale (H,W), convert to BGR first
                                if img.ndim == 2:
                                    gray = img
                                else:
                                    try:
                                        gray = _cv2.cvtColor(img, _cv2.COLOR_BGR2GRAY)
                                    except Exception:
                                        # Defensive: convert array to uint8 and retry
                                        try:
                                            img = img.astype(_np.uint8, copy=False)
                                            gray = _cv2.cvtColor(img, _cv2.COLOR_BGR2GRAY)
                                        except Exception:
                                            return False
                                mean = float(_np.mean(gray))
                                if mean <= 0:
                                    return False
                                if mean < target_mean:
                                    factor = min(max_factor, target_mean / mean)
                                    adjusted = _cv2.convertScaleAbs(img, alpha=factor, beta=0)
                                    ok, buf = _cv2.imencode('.jpg', adjusted)
                                    if ok:
                                        with open(path, 'wb') as _f:
                                            _f.write(buf.tobytes())
                                        return True
                                return False
                            else:
                                # Pillow fallback (lazy import)
                                try:
                                    import importlib, importlib.util
                                    if importlib.util.find_spec('PIL') is None:
                                        return False
                                    PIL_Image = importlib.import_module('PIL.Image')
                                    PIL_ImageEnhance = importlib.import_module('PIL.ImageEnhance')
                                except Exception:
                                    return False
                                try:
                                    img = PIL_Image.open(path)
                                    gray = img.convert('L')
                                    if _np is not None:
                                        mean = float(_np.array(gray).mean())
                                    else:
                                        mean = float(sum(gray.getdata()) / (gray.width * gray.height))
                                    if mean <= 0:
                                        return False
                                    if mean < target_mean:
                                        factor = min(max_factor, target_mean / mean)
                                        enhancer = PIL_ImageEnhance.Brightness(img)
                                        adjusted = enhancer.enhance(factor)
                                        adjusted.save(path, format='JPEG')
                                        return True
                                except Exception:
                                    return False
                                return False
                        except Exception:
                            logging.getLogger(__name__).exception('Brightness adjustment failed')
                            return False

                    try:
                        adjust_image_brightness(tmp_name)
                    except Exception:
                        pass

                    # Run the detector. Prefer a method that returns person boxes if available.
                    try:
                        if hasattr(DETECTOR, 'detect_persons_in_image'):
                            try:
                                raw = DETECTOR.detect_persons_in_image(tmp_name)
                            except Exception as _inner_e:
                                # If DETECTOR fails, attempt IDENTIFIER as a fallback
                                logging.getLogger(__name__).warning('DETECTOR failed: %s - trying IDENTIFIER fallback', _inner_e)
                                raw = None
                                if IDENTIFIER is not None and hasattr(IDENTIFIER, 'detect_and_identify'):
                                    try:
                                        id_results = IDENTIFIER.detect_and_identify(tmp_name)
                                        # Map identifier results into the `raw` format expected below
                                        raw = []
                                        if isinstance(id_results, list):
                                            for it in id_results:
                                                # tag fields to match expected shape
                                                raw.append({'class': 'person', 'confidence': it.get('detection_confidence') or it.get('confidence') or 0.0, 'box': [0,0,0,0], 'person_id': it.get('person_id'), 'person_name': it.get('person_name')})
                                        elif isinstance(id_results, dict):
                                            for it in id_results.get('identified_persons', []):
                                                raw.append({'class': 'person', 'confidence': it.get('detection_confidence') or it.get('confidence') or 0.0, 'box': [0,0,0,0], 'person_id': it.get('person_id'), 'person_name': it.get('person_name')})
                                    except Exception:
                                        raw = None

                            # Expect `raw` to be a list of detections like {'class','confidence','box':[x,y,w,h]}
                            objects = []
                            if raw:
                                for item in raw:
                                    box = None
                                    if isinstance(item, dict):
                                        box = item.get('box') or item.get('bbox')
                                    if box and len(box) >= 4:
                                        x, y, w, h = box[0], box[1], box[2], box[3]
                                    else:
                                        x = item.get('x', 0) if isinstance(item, dict) else 0
                                        y = item.get('y', 0) if isinstance(item, dict) else 0
                                        w = item.get('width', 0) if isinstance(item, dict) else 0
                                        h = item.get('height', 0) if isinstance(item, dict) else 0
                                    objects.append({
                                        'class': (item.get('class') if isinstance(item, dict) else 'person') or 'person',
                                        'confidence': float(item.get('confidence', 0) if isinstance(item, dict) else 0),
                                        'x': int(x), 'y': int(y), 'width': int(w), 'height': int(h)
                                    })
                            results = {'image_path': tmp_name, 'objects': objects, 'count': len(objects)}
                        else:
                            # If the detector only provides a generic `detect` method, use that form instead
                            results = DETECTOR.detect(tmp_name)
                            # ensure results contains 'objects' list
                            if 'objects' not in results and isinstance(results, list):
                                results = {'image_path': tmp_name, 'objects': results, 'count': len(results)}
                    except Exception as e:
                        import traceback as _tb
                        tb = _tb.format_exc()
                        logging.getLogger(__name__).exception('Detection error: %s', e)
                        # Also write traceback to a local debug file for inspection
                        try:
                            with open(str(root / 'detect_error.log'), 'a', encoding='utf-8') as _f:
                                _f.write('\n--- DETECT ERROR ---\n')
                                _f.write(tb)
                        except Exception:
                            pass
                        try:
                            self._set_json_headers(500)
                            self.wfile.write(json.dumps({'error': 'detection failed', 'details': str(e), 'traceback': tb}).encode('utf-8'))
                        except Exception:
                            try:
                                self.send_response(500)
                                self.end_headers()
                                try:
                                    self.wfile.write(tb.encode('utf-8'))
                                except Exception:
                                    pass
                            except Exception:
                                pass
                        # cleanup tmp
                        try:
                            os.remove(tmp_name)
                        except Exception:
                            pass
                        return

                    # If an identifier object is available, try to map detected boxes to known persons
                    identified = []
                    summary_payload = None
                    try:
                        if IDENTIFIER is not None and hasattr(IDENTIFIER, 'detect_and_identify'):
                            id_results = IDENTIFIER.detect_and_identify(tmp_name)
                            # YOLOv4withML returns dict with 'identified_persons' or YOLOv4MedicationDetector returns list
                            if isinstance(id_results, dict):
                                identified = id_results.get('identified_persons', [])
                            elif isinstance(id_results, list):
                                identified = id_results
                    except Exception as _e:
                        logging.getLogger(__name__).warning("Identification failed: %s", _e)

                    # If identification data was returned, annotate detection objects with friendly labels
                    if identified:
                        # Build a mapping from person id to a readable label (e.g. "person1 (Name)")
                        mapping = {}
                        for i, item in enumerate(identified, start=1):
                            pid = None
                            person_name = None
                            if isinstance(item, dict):
                                pid = item.get('person_id') or item.get('person_id')
                                person_name = item.get('person_name') or item.get('person_name')
                                if not person_name and 'database_info' in item and isinstance(item['database_info'], dict):
                                    person_name = item['database_info'].get('name')
                            if pid is None:
                                pid = i
                            if person_name:
                                mapping[pid] = "person{} ({})".format(pid, person_name)
                            else:
                                mapping[pid] = "person{}".format(pid)

                        for idx, obj in enumerate(results.get('objects', []), start=1):
                            if obj.get('class') == 'person' or str(obj.get('class')).lower().startswith('person'):
                                label = mapping.get(idx, "person{}".format(idx))
                                obj['class'] = label

                        # Conservative fall-detection hook: if the detector exposes a
                        # `detect_fall` (or `detect_fallen_posture`) method, call it
                        # with the temporary image. If a fall is detected, trigger a
                        # panic alert in a background thread. This is opt-in and
                        # requires the detector implementation to provide the method.
                        try:
                            fallen = False
                            D = globals().get('DETECTOR')
                            if D is not None:
                                if hasattr(D, 'detect_fall') and callable(getattr(D, 'detect_fall')):
                                    try:
                                        fallen = bool(D.detect_fall(tmp_name))
                                    except Exception as _e:
                                        logging.getLogger(__name__).warning('Fall detection failed: %s', _e)
                                elif hasattr(D, 'detect_fallen_posture') and callable(getattr(D, 'detect_fallen_posture')):
                                    try:
                                        fallen = bool(D.detect_fallen_posture(tmp_name))
                                    except Exception as _e:
                                        logging.getLogger(__name__).warning('Fall posture detection failed: %s', _e)
                            if fallen:
                                # Try to determine an elder id for the alert (prefer identified results)
                                elder_for_alert = None
                                try:
                                    if isinstance(identified, list) and len(identified) > 0:
                                        first = identified[0]
                                        if isinstance(first, dict):
                                            elder_for_alert = first.get('person_id') or first.get('elder_id')
                                except Exception:
                                    elder_for_alert = None
                                if not elder_for_alert:
                                    elder_for_alert = globals().get('LAST_IDENTIFIED')
                                try:
                                    threading.Thread(target=send_panic_alert, args=(elder_for_alert, 'Fall detected by camera'), daemon=True).start()
                                    logging.getLogger(__name__).warning('Fall detected; panic alert dispatched for elder=%s', elder_for_alert)
                                except Exception:
                                    logging.getLogger(__name__).exception('Failed to dispatch panic alert for fall')
                        except Exception:
                            logging.getLogger(__name__).exception('Error in fall-detection hook')

                        leading_candidate = None
                        cur = 0
                        try:
                            with RECENT_IDENTIFICATIONS_LOCK:
                                for item in identified:
                                    conf = None
                                    name = None
                                    pid = None
                                    if isinstance(item, dict):
                                        conf = item.get('confidence') or item.get('detection_confidence') or item.get('score')
                                        name = item.get('person_name') or item.get('person') or item.get('name')
                                        pid = item.get('person_id') or item.get('elder_id')
                                    else:
                                        name = str(item)
                                    conf = _normalize_confidence(conf)
                                    RECENT_IDENTIFICATIONS.append({'person_id': pid, 'name': name, 'confidence': conf, 'ts': time.time()})
                                    if len(RECENT_IDENTIFICATIONS) > RECENT_MAX:
                                        RECENT_IDENTIFICATIONS.pop(0)
                        except Exception:
                            pass

                        try:
                            with CAMERA_SHOT_LOCK:
                                globals()['CAMERA_SHOT_COUNTER'] = globals().get('CAMERA_SHOT_COUNTER', 0) + 1
                                cur = globals().get('CAMERA_SHOT_COUNTER', 0)
                            logging.getLogger(__name__).debug("Camera shot %d/%d", cur, globals().get('CAMERA_AUTOSTOP_N', 10))
                        except Exception:
                            cur = 0

                        try:
                            leading_candidate = summarize_recent_identifications(
                                max_entries=globals().get('CAMERA_AUTOSTOP_N', 10),
                                max_age=SUMMARY_MAX_AGE_SECONDS,
                            )
                        except Exception:
                            leading_candidate = None

                        if leading_candidate:
                            summary_payload = dict(leading_candidate)
                            summary_payload['support_percent'] = round(summary_payload.get('support', 0.0) * 100.0, 1)
                            summary_payload['avg_confidence_percent'] = round(summary_payload.get('avg_confidence', 0.0) * 100.0, 1)
                            summary_key = (summary_payload.get('person_id'), summary_payload.get('name'))
                            now_summary = time.time()
                            try:
                                if (
                                    summary_key != globals().get('LAST_CONFIRMATION_KEY')
                                    or (now_summary - globals().get('LAST_CONFIRMATION_TS', 0.0)) >= CONFIRMATION_REPEAT_SECONDS
                                ):
                                    entry = {
                                        'client_confirmed': False,
                                        'elder_id': summary_payload.get('person_id'),
                                        'name': summary_payload.get('name'),
                                        'label': summary_payload.get('name'),
                                        'confidence': summary_payload.get('avg_confidence'),
                                        'count': summary_payload.get('count'),
                                        'support': summary_payload.get('support'),
                                    }
                                    PENDING_CONFIRMATIONS.put_nowait(entry)
                                    globals()['LAST_CONFIRMATION_KEY'] = summary_key
                                    globals()['LAST_CONFIRMATION_TS'] = now_summary
                            except Exception:
                                pass

                            logging.getLogger(__name__).info(
                                "[SUMMARY] IDENTIFICATION COMPLETE: %s -- SUPPORT %.0f%%, AVG_CONF %.1f%% ACROSS %d SAMPLES",
                                (summary_payload.get('name') or 'Unknown').upper(),
                                summary_payload.get('support_percent', 0.0),
                                summary_payload.get('avg_confidence_percent', 0.0),
                                summary_payload.get('total_samples', 0),
                            )
                            try:
                                msg = PROMPTS.get(CURRENT_LANG, PROMPTS.get('en', {})).get('press_enter_to_proceed')
                                if not msg:
                                    msg = PROMPTS['en'].get('press_enter_to_proceed', 'Press Enter to proceed to the next step...')
                                print(msg)
                            except Exception:
                                print('Press Enter to proceed to the next step...')
                        else:
                            summary_payload = None
                            try:
                                first = identified[0]
                                pid = first.get('person_id') if isinstance(first, dict) else None
                                name = first.get('person_name') if isinstance(first, dict) else str(first)
                                entry = {'client_confirmed': False, 'elder_id': pid, 'name': name, 'label': name}
                                PENDING_CONFIRMATIONS.put_nowait(entry)
                            except Exception:
                                pass

                        try:
                            if cur >= globals().get('CAMERA_AUTOSTOP_N', 10) and not globals().get('CAMERA_AUTO_STOP_TRIGGERED'):
                                globals()['CAMERA_AUTO_STOP_TRIGGERED'] = True
                                best = leading_candidate or summarize_recent_identifications(
                                    max_entries=globals().get('CAMERA_AUTOSTOP_N', 10),
                                    max_age=SUMMARY_MAX_AGE_SECONDS,
                                )
                                if best:
                                    person_id = best.get('person_id')
                                    name = best.get('name') or 'Unknown'
                                    confidence = best.get('avg_confidence', 0.0)
                                    support_pct = (best.get('support', 0.0) or 0.0) * 100.0
                                    logging.getLogger(__name__).info(
                                        "AUTO-STOP IDENTIFICATION COMPLETE AFTER %d SHOTS: %s -- SUPPORT %.0f%%, AVG_CONF %.1f%%",
                                        cur,
                                        name.upper(),
                                        support_pct,
                                        confidence * 100.0,
                                    )
                                    try:
                                        msg = PROMPTS.get(CURRENT_LANG, PROMPTS.get('en', {})).get('press_enter_to_proceed')
                                        if not msg:
                                            msg = PROMPTS['en'].get('press_enter_to_proceed', 'Press Enter to proceed to the next step...')
                                        print(msg)
                                    except Exception:
                                        print('Press Enter to proceed to the next step...')
                                    if person_id:
                                        globals()['LAST_IDENTIFIED'] = person_id
                                        # Start inactivity monitor for the auto-stop identified person
                                        try:
                                            start_person_inactivity_monitor(person_id, name)
                                        except Exception:
                                            logging.getLogger(__name__).exception("Failed to start inactivity monitor for auto-stop ID")
                                    globals()['SKIP_PENDING_PROMPT'] = True
                                    globals()['SKIP_PENDING_PRINTED'] = False
                                else:
                                    logging.getLogger(__name__).info("Auto-stop: no candidate selected after %d shots", cur)
                        except Exception:
                            logging.getLogger(__name__).exception("Error selecting candidate during auto-stop")

                    # Remove the temporary file to avoid filling up disk space
                    try:
                        os.remove(tmp_name)
                    except Exception:
                        pass

                    # respond with detections and any identified meta
                    try:
                        logging.getLogger(__name__).info("/detect -> detections=%d identified=%d", len(results.get('objects', [])) if isinstance(results, dict) else 0, len(identified) if identified else 0)
                    except Exception:
                        pass
                    payload = {'detections': results, 'identified': identified}
                    self._set_json_headers(200)
                    self.wfile.write(json.dumps(payload).encode('utf-8'))
                except Exception:
                    logging.getLogger(__name__).exception("Unhandled exception in do_POST handler")
                    import traceback as _tb
                    tb = _tb.format_exc()
                    try:
                        self._set_json_headers(500)
                        self.wfile.write(json.dumps({'error': 'internal server error', 'details': tb}).encode('utf-8'))
                    except Exception:
                        try:
                            self.send_response(500)
                            self.end_headers()
                            try:
                                self.wfile.write(tb.encode('utf-8'))
                            except Exception:
                                pass
                        except Exception:
                            pass

        handler = functools.partial(CameraRequestHandler, directory=str(root))
        try:
            httpd = http.server.ThreadingHTTPServer(("127.0.0.1", port), handler)
        except Exception:
            # If binding to localhost fails, bind to all interfaces as a fallback
            httpd = http.server.ThreadingHTTPServer(("", port), handler)

        def serve():
            # Run the HTTP server loop; allow it to exit silently if the thread is stopped
            try:
                httpd.serve_forever()
            except Exception:
                pass

        t = threading.Thread(target=serve, daemon=True)
        _httpd = httpd
        _server_thread = t
        t.start()
        logging.getLogger(__name__).info("Camera server build: %s", SERVER_BUILD_ID)
        # Give the server a short moment to start before opening the browser
        time.sleep(0.2)
        # Reset camera shot counter and auto-stop trigger for this session
        try:
            globals()['CAMERA_SHOT_COUNTER'] = 0
            globals()['CAMERA_AUTO_STOP_TRIGGERED'] = False
            globals()['SKIP_PENDING_PROMPT'] = False
            globals()['SKIP_PENDING_PRINTED'] = False
        except Exception:
            pass
        url = "http://127.0.0.1:{}/Camera.html?autocamera=1".format(port) #The port no. here is assumed as 8000
        print("[OK] Camera server started at {}".format(url))
        webbrowser.open(url)

    def stop_camera_server():
        nonlocal _httpd, _server_thread
        if _httpd is None:
            print("[INFO] Camera server is not running")
            return
        try:
            # Shutdown the HTTP server in a background thread so the main loop
            httpd_ref = _httpd
            thread_ref = _server_thread

            def _shutdown_worker(h, thr):
                try:
                    h.shutdown()
                except Exception:
                    pass
                try:
                    thr.join(timeout=1.0)
                except Exception:
                    pass
                try:
                    h.server_close()
                except Exception:
                    pass

            shutdown_thread = threading.Thread(target=_shutdown_worker, args=(httpd_ref, thread_ref), daemon=True)
            shutdown_thread.start()
        except Exception as e:
            print("[ERROR] Stopping server (background shutdown failed): {}".format(e))
        # Clear local server references immediately so prompt is responsive
        _httpd = None
        _server_thread = None
        print("[OK] Camera server stopped (shutdown in background)")

        # When the camera is stopped by the operator, pick the highest-confidence
        # recent identification (if any). Do NOT enqueue a pending confirmation
        # automatically — that blocks the main loop waiting for a Y/N. Instead
        # record the result in `LAST_IDENTIFIED` and print an instruction so the
        # operator can confirm later using the `confirm` command. Also set
        # `SKIP_PENDING_PROMPT` to avoid processing any pending confirmations
        # immediately (this prevents the UI from blocking input).
        try:
            best = None
            with RECENT_IDENTIFICATIONS_LOCK:
                if RECENT_IDENTIFICATIONS:
                    best = max(RECENT_IDENTIFICATIONS, key=lambda x: (x.get('confidence', 0.0) or 0.0))
                    # keep the recent buffer available for later inspection but trim it
                    RECENT_IDENTIFICATIONS[:] = RECENT_IDENTIFICATIONS[-RECENT_MAX:]

            if best:
                person_id = best.get('person_id')
                name = best.get('name') or best.get('label') or 'Unknown'
                confidence = best.get('confidence', 0.0)
                print("[INFO] IDENTIFICATION COMPLETE: {} (CONFIDENCE={:.1f}%)".format(name.upper(), confidence*100))
                # Record last identified for later confirmation
                if person_id:
                    globals()['LAST_IDENTIFIED'] = person_id
                else:
                    globals()['LAST_IDENTIFIED'] = None
                # Prevent the main loop from prompting immediately; user may want
                # to continue typing other commands. Provide an instruction instead.
                globals()['SKIP_PENDING_PROMPT'] = True
                globals()['SKIP_PENDING_PRINTED'] = False
                print("[INFO] To view or confirm this identification, use the 'confirm' command or 'process' to handle queued confirmations.")
                try:
                    msg = PROMPTS.get(CURRENT_LANG, PROMPTS.get('en', {})).get('press_enter_to_proceed')
                    if not msg:
                        msg = PROMPTS['en'].get('press_enter_to_proceed', 'Press Enter to proceed to the next step...')
                    print(msg)
                except Exception:
                    print('Press Enter to proceed to the next step...')
            else:
                print("[INFO] No recent identifications to select from.")
        except Exception as _e:
            print("[WARN] Error selecting best recent identification: {}".format(_e))

    while True:
        try:
            # If an auto-stop has been triggered by the camera handler, stop the server
            # from the main thread so we can perform proper cleanup and selection.
            try:
                if globals().get('CAMERA_AUTO_STOP_TRIGGERED') and _httpd is not None:
                    print("[INFO] Camera auto-stop triggered; stopping camera server now.")
                    # clear the trigger early to avoid re-entrancy
                    globals()['CAMERA_AUTO_STOP_TRIGGERED'] = False
                    try:
                        stop_camera_server()
                    except Exception as _e:
                        print("[WARN] Auto-stop failed to stop server cleanly: {}".format(_e))
            except Exception:
                pass
            # Process any pending identification confirmations first, but allow
            # skipping automatic prompts immediately after a stop/auto-stop so
            # the interactive prompt remains responsive. If skipping is active
            # we print a one-time notice and defer processing until the user
            # runs the `process` command.
            if not globals().get('SKIP_PENDING_PROMPT'):
                while not PENDING_CONFIRMATIONS.empty():
                    item = PENDING_CONFIRMATIONS.get_nowait()
                    logging.getLogger(__name__).info("Dequeued pending confirmation: %s", item)
                    elder_id = item.get('elder_id')
                    elder_name = item.get('name') or item.get('label') or 'Unknown'
                    client_confirmed = item.get('client_confirmed', False)
                    while True:
                        prompt = PROMPTS[CURRENT_LANG]["confirm_person"].format(name=elder_name)
                        sys.stdout.write(prompt)
                        sys.stdout.flush()
                        yn = sys.stdin.readline().strip().lower()
                        if yn in ('y', 'n'):
                            break

                    if yn == 'n':
                        # Operator rejected — return to the main menu. Do not stop server here.
                        print("[INFO] Identification rejected by operator - returning to main menu.")
                        continue

                    # Operator accepted the identification
                    if elder_id:
                        display_person(elder_id, manager, reminder)
                    else:
                        print("[WARN] No matching elder record for label: '{}'".format(elder_name))
                        # Optionally we could allow the operator to pick a person here
                        continue
            else:
                # If skipping is active and there are pending items, print a single
                # informative line (avoid spamming by checking SKIP_PENDING_PRINTED)
                if PENDING_CONFIRMATIONS.qsize() > 0 and not globals().get('SKIP_PENDING_PRINTED'):
                    print(PROMPTS[CURRENT_LANG]["pending_confirmations"].format(count=PENDING_CONFIRMATIONS.qsize()))
                    globals()['SKIP_PENDING_PRINTED'] = True

            # Use explicit stdout flush + stdin.readline so the prompt is
            # visible immediately even when other threads log to stdout.
            sys.stdout.write("Enter command > ")
            sys.stdout.flush()
            try:
                cmd = sys.stdin.readline()
            except Exception:
                cmd = ''
            # Record that some input activity occurred (even if empty newline)
            try:
                globals()['LAST_INPUT_TS'] = time.time()
            except Exception:
                pass
            if cmd is None:
                cmd = ''
            cmd = cmd.strip().lower()
                # Ignore accidental pasted shell invocation lines (PowerShell/VSCode may paste them)
                # Example: & "D:/.../.venv/Scripts/python.exe" "d:/.../Second Programme.py"
            if not cmd:
                continue
            # Strip surrounding quotes before doing pattern checks
            cmd_unquoted = cmd.strip('"\'')
            if cmd_unquoted.startswith('& '):
                print("[INFO] Ignoring shell invocation line.")
                continue
            # If the input looks like a path or an executable invocation, treat it as accidental and ignore it
            if re.search(r'(^[A-Za-z]:[\\/])|python\.exe|\.venv|scripts[\\/]|\.py\b|\.exe\b', cmd_unquoted, re.IGNORECASE):
                print("[INFO] Ignoring shell/path-like input.")
                continue
            # Accept 'stop' as an alias for 'stopcamera' for convenience
            if cmd == 'stop':
                cmd = 'stopcamera'

            # Support a quick 'panic' command: `panic` or `panic <elder_id>`
            if cmd.startswith('panic'):
                parts = cmd.split()
                eid = None
                if len(parts) > 1:
                    try:
                        eid = int(parts[1])
                    except Exception:
                        eid = parts[1]
                if not eid:
                    eid = globals().get('LAST_IDENTIFIED')
                if not eid:
                    print('[ERROR] No elder id provided and no recent identification available to use for panic alert.')
                else:
                    # Respect PANIC_REQUIRE_CONFIRM when triggered from CLI
                    try:
                        if globals().get('PANIC_REQUIRE_CONFIRM', True):
                            try:
                                prompt = PROMPTS.get(CURRENT_LANG, PROMPTS.get('en', {})).get('panic_confirm_prompt')
                            except Exception:
                                prompt = "Confirm sending emergency alert? (y/n) > "
                            ans = input(prompt).strip().lower()
                            if ans not in ('y', 'yes'):
                                print('[INFO] Panic alert cancelled by operator.')
                                continue
                        print('[WARN] Sending panic alert for elder: {}'.format(eid))
                        threading.Thread(target=send_panic_alert, args=(eid, 'Panic triggered via CLI'), daemon=True).start()
                        print('[OK] Panic alert dispatched (background).')
                    except Exception:
                        logging.getLogger(__name__).exception('Failed to dispatch panic alert from CLI')
                        print('[ERROR] Failed to dispatch panic alert; check logs.')
                continue

            # CLI toggle for panic confirmation mode: `panicmode on` / `panicmode off`
            if cmd.startswith('panicmode'):
                parts = cmd.split()
                if len(parts) < 2:
                    print("Usage: panicmode on|off")
                    continue
                val = parts[1].strip().lower()
                if val in ('on', '1', 'true', 'yes'):
                    globals()['PANIC_REQUIRE_CONFIRM'] = True
                    print(PROMPTS.get(CURRENT_LANG, PROMPTS.get('en', {})).get('panicmode_on', 'Panic confirm mode: ON'))
                else:
                    globals()['PANIC_REQUIRE_CONFIRM'] = False
                    print(PROMPTS.get(CURRENT_LANG, PROMPTS.get('en', {})).get('panicmode_off', 'Panic confirm mode: OFF'))
                continue

            if cmd == "exit" or cmd == "quit":
                print(FAREWELLS.get(CURRENT_LANG, FAREWELLS['en']))
                break
            # Quick shortcuts: a -> person 1, b -> person 2, c -> person 3
            elif cmd in ("a", "b", "c"):
                shortcut_map = {'a': 1, 'b': 2, 'c': 3}
                person_id = shortcut_map[cmd]
                # Reuse the same last-4-digit confirmation flow used by `person <id>`
                person = manager.get_elder(person_id)
                if person is None:
                    print("[ERROR] Person {} not found".format(person_id))
                    continue
                ext = person.get('external_id') or person.get('external') or ''
                if not ext or len(ext) < 4:
                    print(PROMPTS[CURRENT_LANG]["no_external_id"])
                    continue
                confirm = input(PROMPTS[CURRENT_LANG]["confirm_input"]).strip()
                if _last4_match(person, confirm):
                    display_person(person_id, manager, reminder)
                else:
                    print(PROMPTS[CURRENT_LANG]["invalid_confirmation"]) 
                continue
            # If the user enters an 8-digit code, treat it as an external ID and look up the person
            if re.fullmatch(r"\d{8}", cmd):
                ext = cmd
                elder = manager.get_elder_by_external_id(ext) if hasattr(manager, 'get_elder_by_external_id') else None
                if elder:
                    # Require last-4-digit confirmation to view details (consistent with other paths)
                    if not ext or len(ext) < 4:
                        print("[WARN] External ID is invalid; returning to main menu")
                        continue
                    confirm = input(PROMPTS[CURRENT_LANG]["confirm_input"]).strip()
                    if _last4_match(elder, confirm):
                        # Start inactivity monitor for this person
                        start_person_inactivity_monitor(elder['elder_id'], elder.get('name', 'Unknown'))
                        display_person(elder['elder_id'], manager, reminder)
                    else:
                        print(PROMPTS[CURRENT_LANG]["invalid_confirmation"]) 
                else:
                    print("[ERROR] Unknown ID: {} - returning to main menu".format(ext))
                continue
            # Support the explicit `id <8-digit>` command as an alternative way to open a person
            if cmd.startswith('id '):
                parts = cmd.split()
                if len(parts) >= 2 and re.fullmatch(r"\d{8}", parts[1]):
                    ext = parts[1]
                    elder = manager.get_elder_by_external_id(ext) if hasattr(manager, 'get_elder_by_external_id') else None
                    if elder:
                        # Ask for last-4-digit confirmation before showing details
                        if not ext or len(ext) < 4:
                            print("[WARN] External ID is invalid; returning to main menu")
                            continue
                        confirm = input(PROMPTS[CURRENT_LANG]["confirm_input"]).strip()
                        if _last4_match(elder, confirm):
                            # Start inactivity monitor for this person
                            start_person_inactivity_monitor(elder['elder_id'], elder.get('name', 'Unknown'))
                            display_person(elder['elder_id'], manager, reminder)
                        else:
                            print(PROMPTS[CURRENT_LANG]["invalid_confirmation"]) 
                    else:
                        print("[ERROR] Unknown ID: {} - returning to main menu".format(ext))
                else:
                    print("[ERROR] Use: id <8-digit-ID> (e.g., id 12345678)")
                continue
            elif cmd == "all":
                # Require a password before showing the full dataset to protect privacy
                MED_VIEW_PASSWORD = os.environ.get('MED_VIEW_PASSWORD', '08181125')
                pw = input(PROMPTS[CURRENT_LANG]["password_prompt"]).strip()
                if pw == MED_VIEW_PASSWORD:
                    display_all(manager)
                else:
                    print(PROMPTS[CURRENT_LANG]["invalid_password"])
                continue
            elif cmd == "camera":
                try:
                    # Try to pre-instantiate YOLOv4 detector/identifier so recognition
                    # is available immediately when the camera starts. This makes
                    # failures visible here rather than later in the HTTP handler.
                    try:
                        if globals().get('DETECTOR') is None or globals().get('IDENTIFIER') is None:
                            from yoloV4.yolov4_detector import YOLOv4PersonDetector, YOLOv4MedicationDetector, setup_yolov4_config, download_yolov4_weights
                            # Ensure config files exist and try to download weights if missing
                            try:
                                setup_yolov4_config()
                            except Exception as _e:
                                print("[YOLOV4] setup config failed: {}".format(_e))
                            weights_path = os.path.join(str(Path(__file__).parent.resolve()), 'yoloV4', 'yolov4.weights')
                            if not os.path.exists(weights_path):
                                print('[YOLOV4] Weights appear missing; downloading now (this may take several minutes)...')
                                try:
                                    download_yolov4_weights()
                                except Exception as _e:
                                    print("[YOLOV4] Auto-download failed: {}".format(_e))

                            # create detector and identifier (identifier may create its own detector)
                            globals()['DETECTOR'] = globals().get('DETECTOR') or YOLOv4PersonDetector()
                            globals()['IDENTIFIER'] = globals().get('IDENTIFIER') or YOLOv4MedicationDetector()
                            logging.getLogger(__name__).info("Pre-instantiated DETECTOR=%s IDENTIFIER=%s", type(globals().get('DETECTOR')), type(globals().get('IDENTIFIER')))
                    except Exception as _e:
                        print("[WARN] Could not pre-instantiate YOLOv4 detector/identifier: {}".format(_e))
                    start_camera_server(port=8000)
                except Exception as e:
                    print("[ERROR] Could not start camera server: {}".format(e))
                continue
            elif cmd == "stopcamera":
                try:
                    stop_camera_server()
                except Exception as e:
                    print("[ERROR] Could not stop camera server: {}".format(e))
                continue
            elif cmd == "confirm":
                # Confirm the most recently identified person (non-blocking flow)
                last = globals().get('LAST_IDENTIFIED')
                if not last:
                    print("[INFO] No recent identification available to confirm.")
                else:
                    print("[INFO] Confirming last identified person (id={}).".format(last))
                    try:
                        display_person(last, manager, reminder)
                    except Exception as _e:
                        print("[ERROR] Could not display person {}: {}".format(last, _e))
                continue
            elif cmd == 'fetchyolo':
                # Manual fetch of YOLOv4 config and weights (useful if automatic attempt failed)
                try:
                    from yoloV4.yolov4_detector import setup_yolov4_config, download_yolov4_weights
                    print('[YOLOV4] Ensuring config files...')
                    try:
                        setup_yolov4_config()
                    except Exception as _e:
                        print('[YOLOV4] setup config failed: {}'.format(_e))
                    print('[YOLOV4] Downloading weights (this may take several minutes)...')
                    try:
                        download_yolov4_weights()
                        print('[YOLOV4] Download complete')
                    except Exception as _e:
                        print('[YOLOV4] Download failed: {}'.format(_e))
                except Exception as _e:
                    print('[ERROR] YOLO helpers not available: {}'.format(_e))
                continue
            elif cmd == 'process':
                # Process one pending confirmation (if any) — prompts the operator
                if PENDING_CONFIRMATIONS.empty():
                    print('[INFO] No pending confirmations to process.')
                else:
                    try:
                        item = PENDING_CONFIRMATIONS.get_nowait()
                        logging.getLogger(__name__).info('Processing queued confirmation: %s', item)
                        elder_id = item.get('elder_id')
                        elder_name = item.get('name') or item.get('label') or 'Unknown'
                        while True:
                            prompt = PROMPTS[CURRENT_LANG]["confirm_person"].format(name=elder_name)
                            sys.stdout.write(prompt)
                            sys.stdout.flush()
                            yn = sys.stdin.readline().strip().lower()
                            if yn in ('y', 'n'):
                                break
                        if yn == 'n':
                            print('[INFO] Identification rejected by operator - returning to main menu.')
                        else:
                            if elder_id:
                                display_person(elder_id, manager, reminder)
                            else:
                                print("[WARN] No matching elder record for label: '{}'".format(elder_name))
                    except Exception as _e:
                        print('[ERROR] Could not process pending confirmation: {}'.format(_e))
                continue
            elif cmd == 'discard':
                # Discard all pending confirmations
                count = 0
                while not PENDING_CONFIRMATIONS.empty():
                    try:
                        PENDING_CONFIRMATIONS.get_nowait()
                        count += 1
                    except Exception:
                        break
                print('[INFO] Discarded {} pending confirmations.'.format(count))
                continue
            elif cmd.startswith("showmeds"):
                parts = cmd.split()
                person_id = None
                if len(parts) >= 2 and parts[1].isdigit():
                    person_id = int(parts[1])
                else:
                    person_id = globals().get('LAST_IDENTIFIED')
                if not person_id:
                    print("[ERROR] No person specified and no recent identification available.")
                    continue
                person = manager.get_elder(person_id)
                if person is None:
                    print("[ERROR] Person {} not found".format(person_id))
                    continue
                ext = person.get('external_id') or person.get('external') or ''
                if (not ext or len(re.sub(r"\D", "", str(ext))) < 4) and not person.get('phone'):
                    print(PROMPTS[CURRENT_LANG]["no_external_id"])
                    continue
                confirm = input(PROMPTS[CURRENT_LANG]["confirm_input"]).strip()
                if _last4_match(person, confirm):
                    # Show full information including medications
                    display_person(person_id, manager, reminder, show_medications=True)
                else:
                    print(PROMPTS[CURRENT_LANG]["invalid_confirmation"]) 
                continue
            elif cmd.startswith("person"):
                parts = cmd.split()
                if len(parts) < 2 or not parts[1].isdigit():
                    print("[ERROR] Use: person 1, person 2, person 3\n")
                    continue
                person_id = int(parts[1])
                # Require confirmation via last-4-digits of external ID
                person = manager.get_elder(person_id)
                if person is None:
                    print("[ERROR] Person {} not found".format(person_id))
                    continue
                ext = person.get('external_id') or person.get('external') or ''
                if (not ext or len(re.sub(r"\D", "", str(ext))) < 4) and not person.get('phone'):
                    print(PROMPTS[CURRENT_LANG]["no_external_id"])
                    continue
                confirm = input(PROMPTS[CURRENT_LANG]["confirm_input"]).strip()
                if _last4_match(person, confirm):
                    display_person(person_id, manager, reminder)
                else:
                    print(PROMPTS[CURRENT_LANG]["invalid_confirmation"]) 
                continue
            
            print("[ERROR] Unknown command: {}\n".format(cmd))
        
        except KeyboardInterrupt:
            print(FAREWELLS.get(CURRENT_LANG, FAREWELLS['en']))
            break
        except Exception as e:
            print("[ERROR] {}\n".format(e))

if __name__ == "__main__": #calling the main function
    main()
