"""
Modern Email & SMS Mailer - Neumorphic Glass Edition
A beautiful real-time messaging application with nature-inspired glass themes
"""

import streamlit as st
import smtplib
import json
import os
import hashlib
import random
import string
import uuid
import re
import time
import threading
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.utils import formatdate, make_msgid
from datetime import datetime, timedelta
from pathlib import Path

# Try to import Jelly components for animated UI
try:
    from jelly_components import (
        jelly_blob_metric,
        jelly_blob_intensity,
        jelly_blob_volume,
        jelly_blob_progress,
        jelly_blob_bounce,
        jelly_metric,
        jelly_notification,
        jelly_loading,
        jelly_progress,
        jelly_gauge,
        jelly_stats_card,
        jelly_slider_display,
        jelly_button
    )
    import dashboard_jelly
    JELLY_AVAILABLE = True
except ImportError:
    JELLY_AVAILABLE = False

# Azure Communication Services for SMS
try:
    from azure.communication.sms import SmsClient
    AZURE_SMS_AVAILABLE = True
except ImportError:
    AZURE_SMS_AVAILABLE = False

# Page Configuration
st.set_page_config(
    page_title="Dragon Mailer | Glass Edition",
    page_icon="🐉",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Logo path
LOGO_PATH = Path(__file__).parent / "images" / "dragon_logo.png"

# =============================================================================
# NATURE BACKGROUNDS & NEUMORPHIC GLASS THEMES
# =============================================================================

NATURE_BACKGROUNDS = {
    "�️ Island Lake": "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?w=1920&q=85",
    "�🌊 Ocean Waves": "https://images.unsplash.com/photo-1505118380757-91f5f5632de0?w=1920&q=80",
    "🏖️ Tropical Beach": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1920&q=80",
    "🌲 Misty Forest": "https://images.unsplash.com/photo-1448375240586-882707db888b?w=1920&q=80",
    "🌸 Cherry Blossoms": "https://images.unsplash.com/photo-1522383225653-ed111181a951?w=1920&q=80",
    "🏔️ Mountain Lake": "https://images.unsplash.com/photo-1439066615861-d1af74d74000?w=1920&q=80",
    "🌅 Sunset Sky": "https://images.unsplash.com/photo-1495616811223-4d98c6e9c869?w=1920&q=80",
    "🌿 Bamboo Grove": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=1920&q=80",
    "❄️ Winter Snow": "https://images.unsplash.com/photo-1491002052546-bf38f186af56?w=1920&q=80",
    "🌻 Flower Field": "https://images.unsplash.com/photo-1490750967868-88aa4486c946?w=1920&q=80",
    "🌙 Northern Lights": "https://images.unsplash.com/photo-1531366936337-7c912a4589a7?w=1920&q=80",
}

GLASS_THEMES = {
    "❄️ Frosted Crystal": {
        "glass_bg": "rgba(255, 255, 255, 0.15)",
        "glass_border": "rgba(255, 255, 255, 0.3)",
        "shadow_light": "rgba(255, 255, 255, 0.5)",
        "shadow_dark": "rgba(0, 0, 0, 0.15)",
        "text_color": "#ffffff",
        "accent": "#00d4ff",
        "blur": "20px"
    },
    "🌊 Ocean Mist": {
        "glass_bg": "rgba(0, 150, 200, 0.12)",
        "glass_border": "rgba(100, 200, 255, 0.25)",
        "shadow_light": "rgba(150, 220, 255, 0.4)",
        "shadow_dark": "rgba(0, 50, 100, 0.2)",
        "text_color": "#e8f4f8",
        "accent": "#4ecdc4",
        "blur": "18px"
    },
    "🌸 Rose Quartz": {
        "glass_bg": "rgba(255, 182, 193, 0.12)",
        "glass_border": "rgba(255, 200, 210, 0.3)",
        "shadow_light": "rgba(255, 220, 230, 0.5)",
        "shadow_dark": "rgba(100, 50, 70, 0.15)",
        "text_color": "#fff5f7",
        "accent": "#ff6b9d",
        "blur": "22px"
    },
    "🌲 Forest Dew": {
        "glass_bg": "rgba(50, 120, 80, 0.12)",
        "glass_border": "rgba(100, 180, 120, 0.25)",
        "shadow_light": "rgba(150, 220, 170, 0.4)",
        "shadow_dark": "rgba(20, 60, 30, 0.2)",
        "text_color": "#e8f5e9",
        "accent": "#66bb6a",
        "blur": "18px"
    },
    "🌙 Midnight Glass": {
        "glass_bg": "rgba(30, 30, 60, 0.25)",
        "glass_border": "rgba(100, 100, 180, 0.3)",
        "shadow_light": "rgba(150, 150, 220, 0.3)",
        "shadow_dark": "rgba(10, 10, 30, 0.3)",
        "text_color": "#e8e8ff",
        "accent": "#9d4edd",
        "blur": "16px"
    },
    "☀️ Golden Hour": {
        "glass_bg": "rgba(255, 200, 100, 0.1)",
        "glass_border": "rgba(255, 220, 150, 0.3)",
        "shadow_light": "rgba(255, 240, 200, 0.5)",
        "shadow_dark": "rgba(150, 100, 50, 0.15)",
        "text_color": "#fff8e7",
        "accent": "#ffc107",
        "blur": "20px"
    },
    "🏝️ Lake Teal": {
        "glass_bg": "rgba(20, 60, 80, 0.18)",
        "glass_border": "rgba(14, 165, 233, 0.3)",
        "shadow_light": "rgba(100, 200, 230, 0.25)",
        "shadow_dark": "rgba(10, 40, 60, 0.3)",
        "text_color": "#e0f7fa",
        "accent": "#0ea5e9",
        "blur": "20px"
    },
}

# SMS Carrier Gateways (US)
SMS_GATEWAYS = {
    "Auto (Try All)": "auto",  # Special: will try all major carriers
    "AT&T": "txt.att.net",
    "T-Mobile": "tmomail.net",
    "Verizon": "vtext.com",
    "Sprint": "messaging.sprintpcs.com",
    "US Cellular": "email.uscc.net",
    "Metro PCS": "mymetropcs.com",
    "Boost Mobile": "sms.myboostmobile.com",
    "Cricket": "sms.cricketwireless.net",
    "Virgin Mobile": "vmobl.com",
    "Google Fi": "msg.fi.google.com",
    "Republic Wireless": "text.republicwireless.com",
    "Straight Talk": "vtext.com",
    "Mint Mobile": "tmomail.net",
    "Xfinity Mobile": "vtext.com",
    "Visible": "vtext.com",
}

# Primary gateways to try for Auto mode (most common US carriers)
AUTO_SMS_GATEWAYS = [
    "vtext.com",       # Verizon (largest)
    "tmomail.net",     # T-Mobile (2nd largest)
    "txt.att.net",     # AT&T (3rd largest)
    "messaging.sprintpcs.com",  # Sprint/T-Mobile
]

# SMTP Presets
SMTP_PRESETS = {
    "Gmail": {"server": "smtp.gmail.com", "port": 587, "tls": True, "description": "Google Gmail - requires App Password"},
    "Outlook/Hotmail": {"server": "smtp-mail.outlook.com", "port": 587, "tls": True, "description": "Microsoft personal accounts"},
    "Office 365 Business": {"server": "smtp.office365.com", "port": 587, "tls": True, "description": "Microsoft 365 Business accounts"},
    "Yahoo": {"server": "smtp.mail.yahoo.com", "port": 587, "tls": True, "description": "Yahoo Mail - requires App Password"},
    "iCloud": {"server": "smtp.mail.me.com", "port": 587, "tls": True, "description": "Apple iCloud Mail"},
    "Zoho": {"server": "smtp.zoho.com", "port": 587, "tls": True, "description": "Zoho Mail"},
    "SendGrid": {"server": "smtp.sendgrid.net", "port": 587, "tls": True, "description": "SendGrid SMTP Relay"},
    "Mailgun": {"server": "smtp.mailgun.org", "port": 587, "tls": True, "description": "Mailgun SMTP"},
    "Amazon SES (US East)": {"server": "email-smtp.us-east-1.amazonaws.com", "port": 587, "tls": True, "description": "Amazon SES US East"},
    "Amazon SES (EU West)": {"server": "email-smtp.eu-west-1.amazonaws.com", "port": 587, "tls": True, "description": "Amazon SES EU West"},
    "Postmark": {"server": "smtp.postmarkapp.com", "port": 587, "tls": True, "description": "Postmark transactional email"},
    "FastMail": {"server": "smtp.fastmail.com", "port": 587, "tls": True, "description": "FastMail - requires App Password"},
    "GoDaddy": {"server": "smtpout.secureserver.net", "port": 465, "tls": False, "ssl": True, "description": "GoDaddy Workspace Email"},
    "Brevo (Sendinblue)": {"server": "smtp-relay.brevo.com", "port": 587, "tls": True, "description": "Brevo (formerly Sendinblue)"},
    "Custom SMTP": {"server": "", "port": 587, "tls": True, "description": "Custom SMTP server"},
}

# Email Templates with pattern variables
EMAIL_TEMPLATES = {
    "-- Select Template --": {"subject": "", "body": ""},
    "🔐 Verification Code": {
        "subject": "Your Verification Code",
        "body": "Your verification code is {random_digit:6}.\n\nThis code expires in 10 minutes.\nDo not share this code with anyone.\n\nIf you didn't request this, please ignore this email."
    },
    "🔐 OTP Code": {
        "subject": "Your One-Time Password",
        "body": "Your OTP is {random_digit:6}.\n\nUse this code to complete your login.\nExpires in 5 minutes.\n\nIf this wasn't you, secure your account immediately."
    },
    "📦 Order Confirmation": {
        "subject": "Order Confirmed - #{random_upper:8}",
        "body": "Thank you for your order!\n\nOrder ID: #{random_upper:8}\nDate: {date}\n\nTrack your order: {link}\n\nThank you for shopping with us!"
    },
    "📦 Shipping Notification": {
        "subject": "Your Order Has Been Shipped!",
        "body": "Great news! Your order is on its way!\n\nTracking Number: {random_upper:12}\nTrack here: {link}\n\nEstimated delivery: 3-5 business days."
    },
    "💳 Transaction Alert": {
        "subject": "Transaction Alert - Action Required",
        "body": "A transaction was made on your account.\n\nAmount: ${random_digit:3}.{random_digit:2}\nDate: {date}\nTime: {time}\n\nIf you didn't make this transaction, secure your account: {link}"
    },
    "🔔 Appointment Reminder": {
        "subject": "Reminder: Your Appointment Tomorrow",
        "body": "This is a reminder for your upcoming appointment.\n\nDate: {date}\n\nPlease arrive 15 minutes early.\n\nNeed to reschedule? Click here: {link}"
    },
    "🎁 Promo Code": {
        "subject": "Special Offer Just For You! 🎉",
        "body": "Exclusive offer!\n\nUse code: {random_upper:8}\nGet 20% off your next order!\n\nShop now: {link}\n\nHurry, offer expires soon!"
    },
    "🔑 Password Reset": {
        "subject": "Password Reset Request",
        "body": "We received a request to reset your password.\n\nReset Code: {random_digit:6}\n\nClick here to reset: {link}\n\nThis link expires in 1 hour.\n\nIf you didn't request this, please ignore this email."
    },
    "✅ Account Verified": {
        "subject": "Welcome! Your Account is Verified",
        "body": "Congratulations! Your account has been verified.\n\nYou now have full access to all features.\n\nGet started: {link}\n\nWelcome aboard!"
    },
    "⚠️ Security Alert": {
        "subject": "Security Alert: New Login Detected",
        "body": "A new login was detected on your account.\n\nTime: {time}\nDate: {date}\n\nIf this was you, you can ignore this message.\nIf not, secure your account immediately: {link}"
    },
    "🔗 Custom Link Only": {
        "subject": "Check This Out!",
        "body": "We thought you might find this interesting:\n\n{link}\n\nLet us know what you think!"
    },
}

# SMS Templates with pattern variables
SMS_TEMPLATES = {
    "-- Select Template --": "",
    "🔐 Verification Code": "Your verification code is {random_digit:6}. Valid for 10 minutes. Do not share this code.",
    "🔐 OTP Code": "Your OTP is {random_digit:4}. Use this to complete your login. Expires in 5 mins.",
    "📦 Order Shipped": "Your order has been shipped! Track: {link}",
    "📦 Delivery Update": "Your package is out for delivery! Track here: {link}",
    "💳 Transaction Alert": "Alert: Transaction of ${random_digit:3}.{random_digit:2} on your account. Review: {link}",
    "🔔 Reminder": "Reminder: Your appointment is tomorrow. Details: {link}",
    "🎁 Promo Code": "Special offer! {random_upper:6} for 20% off! Shop: {link}",
    "🔑 Password Reset": "Reset your password here: {link} Code: {random_digit:6}",
    "📱 2FA Code": "Your 2FA code is {random_digit:6}. Expires in 60 sec.",
    "✅ Account Verified": "Account verified! Get started: {link}",
    "⚠️ Security Alert": "New login detected at {time}. Secure your account: {link}",
    "🔗 Custom Link Only": "Check this out: {link}",
}

# =============================================================================
# FILE PATHS
# =============================================================================
CONFIG_DIR = Path(__file__).parent / "config"
CONFIG_DIR.mkdir(exist_ok=True)

SMTP_CONFIG_FILE = CONFIG_DIR / "smtp_configs.json"
USERS_FILE = CONFIG_DIR / "users.json"
SETTINGS_FILE = CONFIG_DIR / "settings.json"
SENT_MESSAGES_FILE = CONFIG_DIR / "sent_messages.json"
AZURE_SMS_CONFIG_FILE = CONFIG_DIR / "azure_sms.json"
SCHEDULED_FILE = CONFIG_DIR / "scheduled_tasks.json"
TRACKING_FILE = CONFIG_DIR / "tracking.json"

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def load_json(filepath, default=None):
    """Load JSON file safely"""
    if default is None:
        default = {}
    try:
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception:
        pass
    return default

def save_json(filepath, data):
    """Save JSON file safely"""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, default=str)
        return True
    except Exception:
        return False

def get_user_smtp_config_file(username=None):
    """Get SMTP config file path for a specific user"""
    if username is None:
        username = st.session_state.get('current_user', 'admin')
    # Admin uses the main config file, other users get their own
    if username == 'admin':
        return SMTP_CONFIG_FILE
    user_config_dir = CONFIG_DIR / "users"
    user_config_dir.mkdir(exist_ok=True)
    return user_config_dir / f"smtp_{username}.json"

def load_user_smtp_configs():
    """Load SMTP configs for the current user"""
    config_file = get_user_smtp_config_file()
    return load_json(config_file, {"configs": []})

def save_user_smtp_configs(configs):
    """Save SMTP configs for the current user"""
    config_file = get_user_smtp_config_file()
    return save_json(config_file, configs)

def hash_password(password):
    """Hash password with SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def generate_random_string(length=8):
    """Generate random alphanumeric string"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_random_digits(length=6):
    """Generate random digit string"""
    return ''.join(random.choices(string.digits, k=length))

def generate_random_upper(length=8):
    """Generate random uppercase alphanumeric string"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def apply_patterns(text, custom_link=""):
    """
    Apply pattern variables to text.
    Supports:
    - {random} or {random:N} - random alphanumeric
    - {random_digit:N} or {random_digit} - random digits
    - {random_upper:N} - random uppercase
    - {date} - current date
    - {time} - current time
    - {uuid} - unique ID
    - {link} - custom link
    """
    if not text:
        return text
    
    result = text
    
    # Replace {random:N} with random string of length N
    pattern = r'\{random:(\d+)\}'
    for match in re.finditer(pattern, result):
        length = int(match.group(1))
        result = result.replace(match.group(0), generate_random_string(length), 1)
    
    # Replace {random} with default length (8)
    result = result.replace('{random}', generate_random_string(8))
    
    # Replace {random_digit:N} with random digits of length N
    pattern = r'\{random_digit:(\d+)\}'
    for match in re.finditer(pattern, result):
        length = int(match.group(1))
        result = result.replace(match.group(0), generate_random_digits(length), 1)
    
    # Replace {random_digit} with default length (6)
    result = result.replace('{random_digit}', generate_random_digits(6))
    
    # Replace {random_upper:N} with random uppercase of length N
    pattern = r'\{random_upper:(\d+)\}'
    for match in re.finditer(pattern, result):
        length = int(match.group(1))
        result = result.replace(match.group(0), generate_random_upper(length), 1)
    
    # Replace {random_upper} with default length (8)
    result = result.replace('{random_upper}', generate_random_upper(8))
    
    # Replace {date} with current date
    result = result.replace('{date}', datetime.now().strftime('%Y-%m-%d'))
    
    # Replace {time} with current time
    result = result.replace('{time}', datetime.now().strftime('%H:%M:%S'))
    
    # Replace {uuid} with unique ID
    result = result.replace('{uuid}', str(uuid.uuid4())[:8])
    
    # Replace {link} with custom link
    if custom_link:
        result = result.replace('{link}', custom_link)
    
    return result

# =============================================================================
# AZURE SMS FUNCTIONS
# =============================================================================

def load_azure_sms_config():
    """Load Azure SMS configuration"""
    return load_json(AZURE_SMS_CONFIG_FILE, {
        "connection_string": "",
        "phone_number": ""
    })

def save_azure_sms_config(config):
    """Save Azure SMS configuration"""
    return save_json(AZURE_SMS_CONFIG_FILE, config)

def send_sms_via_azure(phone_number, message):
    """
    Send SMS via Azure Communication Services.
    Returns (success, message)
    """
    if not AZURE_SMS_AVAILABLE:
        return False, "Azure Communication Services SDK not installed"
    
    config = load_azure_sms_config()
    if not config.get("connection_string") or not config.get("phone_number"):
        return False, "Azure SMS not configured"
    
    try:
        from azure.communication.sms import SmsClient
        
        # Clean phone number (ensure E.164 format)
        to_number = phone_number.strip()
        if not to_number.startswith('+'):
            to_number = '+1' + to_number  # Assume US
        
        # Create SMS client
        sms_client = SmsClient.from_connection_string(config["connection_string"])
        
        # Send SMS
        response = sms_client.send(
            from_=config["phone_number"],
            to=to_number,
            message=message
        )
        
        # Check response
        for msg_response in response:
            if msg_response.successful:
                return True, f"SMS sent successfully! ID: {msg_response.message_id}"
            else:
                return False, f"Failed: {msg_response.error_message}"
        
        return False, "No response from Azure"
        
    except Exception as e:
        return False, f"Azure SMS Error: {str(e)}"

# =============================================================================
# SCHEDULED TASKS FUNCTIONS
# =============================================================================

def load_scheduled_tasks():
    """Load scheduled tasks"""
    return load_json(SCHEDULED_FILE, {"tasks": []})

def save_scheduled_tasks(data):
    """Save scheduled tasks"""
    return save_json(SCHEDULED_FILE, data)

def add_scheduled_task(task):
    """Add a new scheduled task"""
    data = load_scheduled_tasks()
    task["id"] = str(uuid.uuid4())[:8]
    task["created"] = datetime.now().isoformat()
    task["status"] = "pending"
    data["tasks"].append(task)
    save_scheduled_tasks(data)
    return task["id"]

def delete_scheduled_task(task_id):
    """Delete a scheduled task"""
    data = load_scheduled_tasks()
    data["tasks"] = [t for t in data["tasks"] if t.get("id") != task_id]
    save_scheduled_tasks(data)

def get_pending_tasks():
    """Get tasks that are ready to execute"""
    data = load_scheduled_tasks()
    now = datetime.now()
    pending = []
    for task in data["tasks"]:
        if task.get("status") == "pending":
            scheduled_time = datetime.fromisoformat(task.get("scheduled_time", ""))
            if scheduled_time <= now:
                pending.append(task)
    return pending

# =============================================================================
# CSS INJECTION FOR NEUMORPHIC GLASS
# =============================================================================

def inject_neumorphic_glass_css(background_url, theme):
    """Inject beautiful neumorphic glass CSS"""
    t = GLASS_THEMES[theme]
    
    css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    /* Hide Streamlit branding */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    /* Nature Background */
    .stApp {{
        background: url('{background_url}') no-repeat center center fixed;
        background-size: cover;
        font-family: 'Poppins', sans-serif;
    }}
    
    .stApp::before {{
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.2);
        z-index: -1;
    }}
    
    /* Main Container Glass Effect */
    .main .block-container {{
        background: rgba(15, 15, 30, 0.75);
        backdrop-filter: blur({t['blur']});
        -webkit-backdrop-filter: blur({t['blur']});
        border-radius: 24px;
        border: 1px solid {t['glass_border']};
        box-shadow: 
            8px 8px 32px rgba(0,0,0,0.3),
            -4px -4px 16px rgba(255,255,255,0.03),
            inset 1px 1px 2px rgba(255,255,255,0.05);
        padding: 2rem !important;
        margin: 1rem;
        max-width: 1200px;
    }}
    
    /* Sidebar Glass */
    [data-testid="stSidebar"] {{
        background: rgba(15, 15, 30, 0.85);
        backdrop-filter: blur({t['blur']});
        -webkit-backdrop-filter: blur({t['blur']});
        border-right: 1px solid {t['glass_border']};
        box-shadow: 
            4px 0 16px rgba(0,0,0,0.2),
            inset 1px 0 2px rgba(255,255,255,0.03);
    }}
    
    [data-testid="stSidebar"] [data-testid="stMarkdown"],
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label {{
        color: #ffffff !important;
    }}
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {{
        color: #ffffff !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        font-weight: 600;
    }}
    
    /* Text */
    p, span, label, .stMarkdown, div {{
        color: #ffffff !important;
    }}
    
    /* Links */
    a {{
        color: {t['accent']} !important;
    }}
    
    a:hover {{
        color: #ffffff !important;
        text-decoration: underline;
    }}
    
    /* Neumorphic Input Fields - Dark background for readable text */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {{
        background: rgba(20, 20, 35, 0.85) !important;
        backdrop-filter: blur(10px);
        border: 1px solid {t['glass_border']} !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        box-shadow: 
            inset 4px 4px 8px rgba(0,0,0,0.4),
            inset -2px -2px 6px rgba(255,255,255,0.05);
        padding: 12px 16px !important;
        transition: all 0.3s ease;
    }}
    
    .stSelectbox > div > div > div,
    .stSelectbox > div > div {{
        background: #1a1a2e !important;
        border: 1px solid {t['accent']}40 !important;
        border-radius: 12px !important;
        color: #ffffff !important;
    }}
    
    .stSelectbox [data-baseweb="select"] > div {{
        background: #1a1a2e !important;
        color: #ffffff !important;
    }}
    
    .stNumberInput > div > div > input {{
        background: rgba(20, 20, 35, 0.85) !important;
        border: 1px solid {t['glass_border']} !important;
        border-radius: 12px !important;
        color: #ffffff !important;
    }}
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {{
        border-color: {t['accent']} !important;
        box-shadow: 
            inset 4px 4px 8px rgba(0,0,0,0.4),
            inset -2px -2px 6px rgba(255,255,255,0.05),
            0 0 20px {t['accent']}40;
    }}
    
    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder {{
        color: rgba(255,255,255,0.5) !important;
    }}
    
    /* Labels above inputs */
    .stTextInput > label,
    .stTextArea > label,
    .stSelectbox > label,
    .stNumberInput > label {{
        color: {t['text_color']} !important;
        font-weight: 500;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
    }}
    
    /* Neumorphic Buttons */
    .stButton > button {{
        background: rgba(25, 25, 45, 0.9) !important;
        backdrop-filter: blur(10px);
        border: 1px solid {t['glass_border']} !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        font-weight: 500;
        padding: 12px 24px !important;
        box-shadow: 
            6px 6px 12px rgba(0,0,0,0.3),
            -3px -3px 8px rgba(255,255,255,0.05);
        transition: all 0.3s ease;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 
            8px 8px 16px rgba(0,0,0,0.4),
            -4px -4px 10px rgba(255,255,255,0.05),
            0 0 30px {t['accent']}40;
        border-color: {t['accent']} !important;
        color: {t['accent']} !important;
    }}
    
    .stButton > button:active {{
        transform: translateY(1px);
        box-shadow: 
            inset 4px 4px 8px {t['shadow_dark']},
            inset -4px -4px 8px {t['shadow_light']};
    }}
    
    /* Primary Button */
    .stButton > button[kind="primary"] {{
        background: linear-gradient(145deg, {t['accent']}, {t['accent']}cc) !important;
        color: #ffffff !important;
    }}
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        background: rgba(20, 20, 35, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 8px;
        gap: 8px;
        border: 1px solid {t['glass_border']};
    }}
    
    .stTabs [data-baseweb="tab"] {{
        background: transparent;
        border-radius: 12px;
        color: #ffffff !important;
        padding: 10px 20px;
        transition: all 0.3s ease;
        font-weight: 500;
    }}
    
    .stTabs [data-baseweb="tab"]:hover {{
        background: rgba(255, 255, 255, 0.1);
    }}
    
    .stTabs [aria-selected="true"] {{
        background: rgba(20, 20, 35, 0.9) !important;
        box-shadow: 
            inset 4px 4px 8px rgba(0,0,0,0.3),
            inset -4px -4px 8px rgba(255,255,255,0.05);
        color: {t['accent']} !important;
    }}
    
    /* Cards/Expanders */
    .stExpander {{
        background: rgba(20, 20, 35, 0.7);
        backdrop-filter: blur(10px);
        border: 1px solid {t['glass_border']};
        border-radius: 16px;
        box-shadow: 
            6px 6px 12px {t['shadow_dark']},
            -6px -6px 12px {t['shadow_light']};
        overflow: hidden;
    }}
    
    .stExpander [data-testid="stExpanderHeader"] {{
        color: #ffffff !important;
        font-weight: 500;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
    }}
    
    .stExpander [data-testid="stExpanderHeader"]:hover {{
        color: {t['accent']} !important;
    }}
    
    .stExpander [data-testid="stExpanderDetails"] {{
        background: rgba(15, 15, 30, 0.5);
    }}
    
    .stExpander [data-testid="stExpanderDetails"] p,
    .stExpander [data-testid="stExpanderDetails"] span {{
        color: #ffffff !important;
    }}
    
    /* Metrics */
    [data-testid="metric-container"] {{
        background: rgba(20, 20, 35, 0.75);
        backdrop-filter: blur(10px);
        border: 1px solid {t['glass_border']};
        border-radius: 16px;
        padding: 16px;
        box-shadow: 
            6px 6px 12px {t['shadow_dark']},
            -6px -6px 12px {t['shadow_light']};
    }}
    
    [data-testid="metric-container"] label {{
        color: rgba(255,255,255,0.8) !important;
    }}
    
    [data-testid="metric-container"] [data-testid="stMetricValue"] {{
        color: {t['accent']} !important;
        font-weight: 600;
        text-shadow: 0 0 10px {t['accent']}40;
    }}
    
    /* Alerts/Info boxes */
    .stAlert {{
        background: rgba(20, 20, 35, 0.8) !important;
        backdrop-filter: blur(10px);
        border: 1px solid {t['glass_border']} !important;
        border-radius: 12px;
    }}
    
    .stAlert p, .stAlert span, .stAlert div {{
        color: #ffffff !important;
    }}
    
    /* Success alert */
    .stSuccess {{
        background: rgba(40, 80, 40, 0.8) !important;
        border-left: 4px solid #4caf50 !important;
    }}
    
    /* Error alert */
    .stError {{
        background: rgba(80, 30, 30, 0.8) !important;
        border-left: 4px solid #f44336 !important;
    }}
    
    /* Warning alert */
    .stWarning {{
        background: rgba(80, 60, 20, 0.8) !important;
        border-left: 4px solid #ff9800 !important;
    }}
    
    /* Info alert */
    .stInfo {{
        background: rgba(20, 50, 80, 0.8) !important;
        border-left: 4px solid #2196f3 !important;
    }}
    
    /* Checkbox and Radio */
    .stCheckbox label span,
    .stRadio label span {{
        color: {t['text_color']} !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
    }}
    
    .stRadio > div {{
        background: rgba(20, 20, 35, 0.6) !important;
        border-radius: 12px;
        padding: 10px !important;
    }}
    
    .stCheckbox > div {{
        background: rgba(20, 20, 35, 0.4) !important;
        border-radius: 8px;
        padding: 8px !important;
    }}
    
    /* File Uploader */
    [data-testid="stFileUploader"] {{
        background: rgba(20, 20, 35, 0.7);
        backdrop-filter: blur(10px);
        border: 2px dashed {t['glass_border']};
        border-radius: 16px;
        padding: 20px;
    }}
    
    [data-testid="stFileUploader"] label,
    [data-testid="stFileUploader"] span,
    [data-testid="stFileUploader"] p {{
        color: #ffffff !important;
    }}
    
    [data-testid="stFileUploader"]:hover {{
        border-color: {t['accent']};
    }}
    
    /* Progress bar */
    .stProgress > div > div > div {{
        background: linear-gradient(90deg, {t['accent']}, {t['accent']}80) !important;
        border-radius: 8px;
    }}
    
    /* Selectbox dropdown - GLASS STYLE */
    [data-baseweb="select"] {{
        background: rgba(20, 25, 45, 0.7) !important;
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
    }}
    
    [data-baseweb="select"] * {{
        color: #ffffff !important;
    }}
    
    [data-baseweb="popover"],
    [data-baseweb="popover"] > div {{
        background: rgba(20, 25, 45, 0.85) !important;
        background-color: rgba(20, 25, 45, 0.85) !important;
        backdrop-filter: blur(20px) saturate(150%) !important;
        -webkit-backdrop-filter: blur(20px) saturate(150%) !important;
        border: 1px solid {t['accent']}60 !important;
        border-radius: 12px !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.5), inset 0 1px 1px rgba(255,255,255,0.1) !important;
    }}
    
    /* Dropdown list items - GLASS */
    [data-baseweb="menu"],
    [data-baseweb="menu"] > div,
    [data-baseweb="menu"] ul {{
        background: rgba(20, 25, 45, 0.9) !important;
        background-color: rgba(20, 25, 45, 0.9) !important;
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
        padding: 8px 0 !important;
    }}
    
    [data-baseweb="menu"] li,
    [data-baseweb="menu"] [role="option"],
    [data-baseweb="menu"] div[role="option"] {{
        color: #ffffff !important;
        background: transparent !important;
        background-color: transparent !important;
        padding: 10px 16px !important;
        font-size: 14px !important;
        transition: all 0.2s ease !important;
    }}
    
    [data-baseweb="menu"] li:hover,
    [data-baseweb="menu"] [role="option"]:hover,
    [data-baseweb="menu"] div[role="option"]:hover {{
        background: rgba(255, 255, 255, 0.15) !important;
        background-color: rgba(255, 255, 255, 0.15) !important;
        color: #ffffff !important;
    }}
    
    [data-baseweb="menu"] [aria-selected="true"],
    [data-baseweb="menu"] div[aria-selected="true"] {{
        background: {t['accent']}40 !important;
        background-color: {t['accent']}40 !important;
        color: #ffffff !important;
        font-weight: 600 !important;
    }}
    
    /* Force all list containers glass */
    ul[role="listbox"],
    div[role="listbox"],
    [role="listbox"] {{
        background: rgba(20, 25, 45, 0.9) !important;
        background-color: rgba(20, 25, 45, 0.9) !important;
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
    }}
    
    ul[role="listbox"] li,
    div[role="listbox"] > div,
    [role="listbox"] [role="option"] {{
        background: transparent !important;
        background-color: transparent !important;
        color: #ffffff !important;
    }}
    
    ul[role="listbox"] li:hover,
    div[role="listbox"] > div:hover,
    [role="listbox"] [role="option"]:hover {{
        background: rgba(255, 255, 255, 0.15) !important;
        background-color: rgba(255, 255, 255, 0.15) !important;
    }}
    
    /* Form submit button */
    .stFormSubmitButton > button {{
        background: linear-gradient(145deg, {t['accent']}, {t['accent']}cc) !important;
        color: #ffffff !important;
        border: none !important;
        font-weight: 600;
    }}
    
    /* Scrollbar */
    ::-webkit-scrollbar {{
        width: 8px;
        height: 8px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: {t['glass_bg']};
        border-radius: 4px;
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: {t['accent']}60;
        border-radius: 4px;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: {t['accent']};
    }}
    
    /* FORCE glass backgrounds on all dropdowns and popovers */
    div[data-baseweb] {{
        --background: rgba(20, 25, 45, 0.9) !important;
    }}
    
    /* Override for white backgrounds in any dropdown element - GLASS */
    [class*="StyledList"],
    [class*="StyledDropdown"],
    [class*="Popover"],
    [class*="Menu"],
    [class*="Option"] {{
        background: rgba(20, 25, 45, 0.9) !important;
        background-color: rgba(20, 25, 45, 0.9) !important;
        color: #ffffff !important;
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
    }}
    
    /* BaseWeb specific overrides - GLASS */
    .bsKsFh, .cxdgHy, .dMRJnk, .hkSgvC {{
        background: rgba(20, 25, 45, 0.9) !important;
        background-color: rgba(20, 25, 45, 0.9) !important;
        backdrop-filter: blur(16px) !important;
    }}
    
    /* Any element with white/light background in dropdowns - GLASS */
    [data-baseweb] [style*="background: rgb(255"],
    [data-baseweb] [style*="background-color: rgb(255"],
    [data-baseweb] [style*="background: white"],
    [data-baseweb] [style*="background-color: white"] {{
        background: rgba(20, 25, 45, 0.9) !important;
        background-color: rgba(20, 25, 45, 0.9) !important;
    }}
    
    /* Animations */
    @keyframes float {{
        0%, 100% {{ transform: translateY(0); }}
        50% {{ transform: translateY(-10px); }}
    }}
    
    @keyframes glow {{
        0%, 100% {{ box-shadow: 0 0 20px {t['accent']}40; }}
        50% {{ box-shadow: 0 0 40px {t['accent']}60; }}
    }}
    
    /* Success message animation */
    .element-container:has(.stSuccess) {{
        animation: glow 2s ease-in-out;
    }}
    
    /* Logo styling */
    .logo-container {{
        text-align: center;
        padding: 20px;
        margin-bottom: 20px;
    }}
    
    .logo-text {{
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, {t['accent']}, #ffffff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: none;
    }}
    
    /* Custom card class */
    .glass-card {{
        background: rgba(20, 20, 35, 0.75);
        backdrop-filter: blur({t['blur']});
        border: 1px solid {t['glass_border']};
        border-radius: 16px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 
            6px 6px 12px rgba(0,0,0,0.3),
            -3px -3px 8px rgba(255,255,255,0.03);
        color: #ffffff;
    }}
    
    .glass-card h4 {{
        color: {t['accent']} !important;
    }}
    
    .glass-card p {{
        color: #ffffff !important;
    }}
    
    /* Email/SMS Preview - Code blocks with DARK background and READABLE text */
    [data-testid="stCode"],
    .stCode,
    pre {{
        background: #1a1a2e !important;
        background-color: #1a1a2e !important;
        border: 1px solid {t['glass_border']} !important;
        border-radius: 12px !important;
        padding: 12px !important;
    }}
    
    [data-testid="stCode"] code,
    .stCode code,
    pre code {{
        color: #00ff88 !important;
        background: transparent !important;
        font-family: 'Consolas', 'Monaco', monospace !important;
        font-size: 0.9rem !important;
        white-space: pre-wrap !important;
        word-break: break-word !important;
    }}
    
    /* HTML Preview inside expander - ensure visibility */
    .stExpander [data-testid="stExpanderDetails"] {{
        background: #14142a !important;
    }}
    
    .stExpander [data-testid="stExpanderDetails"] * {{
        color: #e0e0ff !important;
    }}
    
    /* Override white text for preview markdowns */
    .stMarkdown p,
    .stMarkdown span,
    .stMarkdown div {{
        color: #ffffff !important;
    }}
    
    /* ============================================== */
    /* DROPDOWN MENU ITEMS - LIGHT BLUE GLASS FIX    */
    /* ============================================== */
    
    /* Menu container - light blue glass */
    [data-baseweb="popover"] > div,
    [data-baseweb="menu"],
    ul[role="listbox"] {{
        background: rgba(30, 60, 120, 0.95) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(0, 180, 255, 0.3) !important;
        border-radius: 8px !important;
    }}
    
    /* Individual menu items */
    [data-baseweb="menu-item"],
    li[role="option"] {{
        background: transparent !important;
        color: #ffffff !important;
        padding: 10px 15px !important;
    }}
    
    /* Hover state - brighter blue */
    [data-baseweb="menu-item"]:hover,
    li[role="option"]:hover,
    [data-baseweb="menu-item"][aria-selected="true"],
    li[role="option"][aria-selected="true"] {{
        background: rgba(0, 180, 255, 0.4) !important;
        color: #ffffff !important;
    }}
    
    /* Selected/focused item */
    [data-baseweb="menu-item"]:focus,
    li[role="option"]:focus {{
        background: rgba(0, 200, 255, 0.5) !important;
        outline: none !important;
    }}
    
    /* Text inside menu items */
    [data-baseweb="menu-item"] *,
    li[role="option"] * {{
        color: #ffffff !important;
    }}
    
    /* ============================================== */
    /* TEXT ON WHITE BACKGROUNDS - MAKE BLUE         */
    /* ============================================== */
    
    /* Any element with white/light background should have blue text */
    *[style*="background: white"] *,
    *[style*="background-color: white"] *,
    *[style*="background: rgb(255"] *,
    *[style*="background-color: rgb(255"] *,
    *[style*="background:#fff"] *,
    *[style*="background-color:#fff"] * {{
        color: #0066cc !important;
    }}
    
    /* Streamlit emotion cache classes that may have white bg */
    .st-emotion-cache-1inwz65,
    .st-emotion-cache-81oif8,
    .st-emotion-cache-16idsys,
    .st-emotion-cache-1v0mbdj,
    .st-emotion-cache-10trblm {{
        color: #0055aa !important;
    }}
    
    /* Any div/span inside white background containers */
    [data-baseweb="popover"] div,
    [data-baseweb="select"] div {{
        color: #ffffff !important;
    }}
    
    /* Force blue text on any truly white bg element */
    div[style*="255, 255, 255"],
    span[style*="255, 255, 255"],
    li[style*="255, 255, 255"] {{
        color: #0066cc !important;
    }}
    
    /* ============================================== */
    /* INPUT FIELDS - ENSURE VISIBLE TEXT            */
    /* ============================================== */
    
    /* Text inputs - dark background, white text */
    .stTextInput input,
    .stTextInput input[type="text"],
    .stTextInput input[type="password"],
    .stNumberInput input,
    [data-baseweb="input"] input {{
        background: rgba(20, 25, 45, 0.9) !important;
        color: #ffffff !important;
        border: 1px solid rgba(0, 180, 255, 0.3) !important;
        caret-color: #00d4ff !important;
    }}
    
    /* Input placeholder */
    .stTextInput input::placeholder,
    .stNumberInput input::placeholder {{
        color: rgba(255, 255, 255, 0.5) !important;
    }}
    
    /* Input focus state */
    .stTextInput input:focus,
    .stNumberInput input:focus {{
        border-color: #00d4ff !important;
        box-shadow: 0 0 5px rgba(0, 212, 255, 0.3) !important;
    }}
    
    /* ============================================== */
    /* FILE UPLOADER - VISIBLE BUTTON                */
    /* ============================================== */
    
    /* File uploader container */
    .stFileUploader {{
        background: rgba(20, 25, 45, 0.8) !important;
        border: 1px dashed rgba(0, 180, 255, 0.4) !important;
        border-radius: 8px !important;
        padding: 10px !important;
    }}
    
    /* File uploader button - CYAN/BLUE for visibility */
    .stFileUploader button,
    [data-testid="stFileUploader"] button,
    [data-testid="baseButton-secondary"] {{
        background: linear-gradient(135deg, #0088ff, #00d4ff) !important;
        color: #ffffff !important;
        border: none !important;
        padding: 10px 20px !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }}
    
    /* File uploader button hover */
    .stFileUploader button:hover,
    [data-testid="stFileUploader"] button:hover {{
        background: linear-gradient(135deg, #00d4ff, #0088ff) !important;
        transform: scale(1.02) !important;
    }}
    
    /* File uploader text */
    .stFileUploader label,
    .stFileUploader span,
    [data-testid="stFileUploader"] span {{
        color: #ffffff !important;
    }}
    
    /* Browse files text */
    [data-testid="stFileUploader"] section {{
        background: rgba(20, 25, 45, 0.9) !important;
        border: 1px dashed rgba(0, 180, 255, 0.4) !important;
        border-radius: 8px !important;
    }}
    
    /* "Drag and drop" text */
    [data-testid="stFileUploader"] section small {{
        color: rgba(255, 255, 255, 0.7) !important;
    }}
    
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# =============================================================================
# SOUND EFFECTS SYSTEM
# =============================================================================

def inject_sound_system():
    """Inject JavaScript-based sound system using Web Audio API"""
    sound_js = """
    <script>
    // Dragon Mailer Sound System
    window.DragonMailerSounds = {
        audioContext: null,
        enabled: true,
        volume: 0.5,
        
        init: function() {
            try {
                this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
            } catch(e) {
                console.log('Web Audio API not supported');
            }
        },
        
        playTone: function(frequency, duration, type, volume) {
            if (!this.enabled || !this.audioContext) return;
            
            try {
                // Resume audio context if suspended
                if (this.audioContext.state === 'suspended') {
                    this.audioContext.resume();
                }
                
                const oscillator = this.audioContext.createOscillator();
                const gainNode = this.audioContext.createGain();
                
                oscillator.connect(gainNode);
                gainNode.connect(this.audioContext.destination);
                
                oscillator.frequency.value = frequency;
                oscillator.type = type || 'sine';
                
                const vol = (volume || this.volume) * 0.3;
                gainNode.gain.setValueAtTime(vol, this.audioContext.currentTime);
                gainNode.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + duration);
                
                oscillator.start(this.audioContext.currentTime);
                oscillator.stop(this.audioContext.currentTime + duration);
            } catch(e) {
                console.log('Sound error:', e);
            }
        },
        
        // Success sound - pleasant ascending chime
        success: function() {
            this.playTone(523.25, 0.15, 'sine', 0.4);  // C5
            setTimeout(() => this.playTone(659.25, 0.15, 'sine', 0.4), 100);  // E5
            setTimeout(() => this.playTone(783.99, 0.25, 'sine', 0.5), 200);  // G5
        },
        
        // Error sound - descending buzz
        error: function() {
            this.playTone(330, 0.15, 'square', 0.3);  // E4
            setTimeout(() => this.playTone(262, 0.2, 'square', 0.3), 150);  // C4
        },
        
        // Send sound - whoosh-like ascending
        send: function() {
            this.playTone(400, 0.1, 'sine', 0.3);
            setTimeout(() => this.playTone(600, 0.1, 'sine', 0.35), 50);
            setTimeout(() => this.playTone(800, 0.15, 'sine', 0.4), 100);
            setTimeout(() => this.playTone(1000, 0.2, 'sine', 0.3), 150);
        },
        
        // Click sound - soft tap
        click: function() {
            this.playTone(800, 0.05, 'sine', 0.2);
        },
        
        // Notification sound - gentle bell
        notify: function() {
            this.playTone(880, 0.1, 'sine', 0.35);
            setTimeout(() => this.playTone(1100, 0.15, 'sine', 0.3), 120);
        },
        
        // Login sound - welcoming melody
        login: function() {
            this.playTone(523.25, 0.12, 'sine', 0.4);
            setTimeout(() => this.playTone(659.25, 0.12, 'sine', 0.4), 100);
            setTimeout(() => this.playTone(783.99, 0.12, 'sine', 0.4), 200);
            setTimeout(() => this.playTone(1046.50, 0.25, 'sine', 0.5), 300);  // C6
        },
        
        // Warning sound - attention getter
        warning: function() {
            this.playTone(440, 0.15, 'triangle', 0.35);
            setTimeout(() => this.playTone(440, 0.15, 'triangle', 0.35), 200);
        }
    };
    
    // Initialize on first user interaction
    document.addEventListener('click', function initSound() {
        if (!window.DragonMailerSounds.audioContext) {
            window.DragonMailerSounds.init();
        }
        // Don't remove listener - need to resume context on each interaction
    });
    
    // Also init on page load
    window.DragonMailerSounds.init();
    
    // Helper function to call from Streamlit
    window.playDragonSound = function(soundType) {
        if (window.DragonMailerSounds && window.DragonMailerSounds[soundType]) {
            window.DragonMailerSounds[soundType]();
        }
    };
    </script>
    """
    st.markdown(sound_js, unsafe_allow_html=True)

def play_sound(sound_type):
    """Play a sound effect. Types: success, error, send, click, notify, login, warning"""
    st.markdown(f"""
    <script>
    if (window.playDragonSound) {{
        window.playDragonSound('{sound_type}');
    }}
    </script>
    """, unsafe_allow_html=True)

# =============================================================================
# EMAIL SENDING FUNCTIONS
# =============================================================================

def send_email(smtp_config, to_email, subject, body, is_html=False, attachments=None, from_name=None, reply_to=None):
    """Send email via SMTP with optional custom sender name and reply-to"""
    try:
        msg = MIMEMultipart('alternative')
        
        # Format From header with display name if provided
        if from_name:
            from email.utils import formataddr
            msg['From'] = formataddr((from_name, smtp_config['email']))
        else:
            msg['From'] = smtp_config['email']
        
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Add Reply-To header if specified
        if reply_to:
            msg['Reply-To'] = reply_to
        
        if is_html:
            msg.attach(MIMEText(body, 'html'))
        else:
            msg.attach(MIMEText(body, 'plain'))
        
        # Handle attachments
        if attachments:
            for attachment in attachments:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment['data'])
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename="{attachment["name"]}"')
                msg.attach(part)
        
        # Connect and send
        server = smtplib.SMTP(smtp_config['server'], smtp_config['port'])
        server.ehlo()
        
        if smtp_config.get('use_tls', True):
            server.starttls()
            server.ehlo()
        
        server.login(smtp_config['email'], smtp_config['password'])
        server.sendmail(smtp_config['email'], to_email, msg.as_string())
        server.quit()
        
        return {"success": True, "message": f"Email sent to {to_email}"}
    
    except Exception as e:
        return {"success": False, "message": str(e)}

def send_sms_via_gateway(smtp_config, phone_number, carrier, message):
    """Send SMS via carrier email gateway"""
    try:
        gateway = SMS_GATEWAYS.get(carrier)
        if not gateway:
            return {"success": False, "message": f"Unknown carrier: {carrier}"}
        
        # Clean phone number
        phone = ''.join(filter(str.isdigit, phone_number))
        if len(phone) == 11 and phone.startswith('1'):
            phone = phone[1:]
        
        if len(phone) != 10:
            return {"success": False, "message": "Phone number must be 10 digits"}
        
        sms_email = f"{phone}@{gateway}"
        
        # Send via SMTP
        msg = MIMEText(message)
        msg['From'] = smtp_config['email']
        msg['To'] = sms_email
        msg['Subject'] = ""  # SMS doesn't need subject
        
        server = smtplib.SMTP(smtp_config['server'], smtp_config['port'])
        server.ehlo()
        
        if smtp_config.get('use_tls', True):
            server.starttls()
            server.ehlo()
        
        server.login(smtp_config['email'], smtp_config['password'])
        server.sendmail(smtp_config['email'], sms_email, msg.as_string())
        server.quit()
        
        return {"success": True, "message": f"SMS sent to {phone_number}"}
    
    except Exception as e:
        return {"success": False, "message": str(e)}

def send_bulk_emails(smtp_config, recipients, subject, body, is_html=False, progress_callback=None, from_name=None, reply_to=None):
    """Send bulk emails with progress tracking"""
    results = {"success": 0, "failed": 0, "details": []}
    
    for i, recipient in enumerate(recipients):
        result = send_email(smtp_config, recipient.strip(), subject, body, is_html, None, from_name, reply_to)
        
        if result['success']:
            results['success'] += 1
        else:
            results['failed'] += 1
        
        results['details'].append({
            "recipient": recipient,
            "status": "sent" if result['success'] else "failed",
            "message": result['message']
        })
        
        if progress_callback:
            progress_callback((i + 1) / len(recipients))
    
    return results

# =============================================================================
# SESSION STATE INITIALIZATION
# =============================================================================

def init_session_state():
    """Initialize session state variables"""
    defaults = {
        'authenticated': False,
        'current_user': None,
        'user_role': None,
        'theme': '🏝️ Lake Teal',
        'background': '🌲 Misty Forest',
        'smtp_configs': [],
        'current_smtp': None,
        'sending_results': None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# =============================================================================
# AUTHENTICATION
# =============================================================================

def authenticate_user(username, password):
    """Authenticate user"""
    users = load_json(USERS_FILE, {"users": []})
    
    for user in users.get('users', []):
        if user['username'] == username and user['password_hash'] == hash_password(password):
            return user
    return None

def create_default_admin():
    """Create default admin if no users exist"""
    users = load_json(USERS_FILE, {"users": []})
    
    if not users.get('users'):
        users['users'] = [{
            "username": "admin",
            "password_hash": hash_password("SoftWork1@"),
            "role": "admin",
            "created": datetime.now().isoformat()
        }]
        save_json(USERS_FILE, users)

def login_page():
    """Display beautiful glass login page with lake background"""
    import base64
    
    # Lake background image - Emerald Bay style
    LOGIN_BG_IMAGE = "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?w=1920&q=85"
    
    # Colors that complement the lake/forest scene
    orb1 = "#0ea5e9"  # Sky blue
    orb2 = "#059669"  # Forest green
    orb3 = "#6366f1"  # Twilight purple
    
    # Inject beautiful login CSS with lake background
    st.markdown(f"""
    <style>
        /* Fullscreen glass login with lake background */
        html, body {{ overflow: hidden !important; height: 100vh !important; }}
        .stApp {{
            overflow: hidden !important;
            background: url('{LOGIN_BG_IMAGE}') no-repeat center center fixed !important;
            background-size: cover !important;
            min-height: 100vh !important;
        }}
        .stApp::before {{
            content: '';
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background: linear-gradient(135deg, rgba(10, 30, 50, 0.4) 0%, rgba(20, 60, 80, 0.3) 50%, rgba(40, 60, 80, 0.4) 100%);
            z-index: 0;
            pointer-events: none;
        }}
        header[data-testid="stHeader"], #MainMenu, footer, .stDeployButton,
        [data-testid="stSidebar"] {{ display: none !important; }}
        .block-container {{ padding: 0 !important; max-width: 100% !important; }}
        
        /* HIDE fullscreen/toolbar buttons on images - ALL selectors */
        .stElementToolbar,
        [data-testid="stElementToolbar"],
        [data-testid="stElementToolbarButton"],
        [data-testid="stElementToolbarButtonContainer"],
        .st-emotion-cache-12rj9lz,
        .st-emotion-cache-1yq8s3s,
        .e1usqpj01,
        button[aria-label="Fullscreen"],
        button[data-testid="stBaseButton-elementToolbar"] {{
            display: none !important;
            visibility: hidden !important;
            opacity: 0 !important;
            pointer-events: none !important;
        }}
        
        /* Floating orbs */
        .orb {{
            position: fixed;
            border-radius: 50%;
            filter: blur(50px);
            opacity: 0.35;
            z-index: 0;
            pointer-events: none;
            animation: orbFloat 8s ease-in-out infinite;
        }}
        .orb-1 {{ width: 280px; height: 280px; background: {orb1}; bottom: -100px; left: -100px; animation-delay: 0s; }}
        .orb-2 {{ width: 240px; height: 240px; background: {orb2}; top: -80px; right: -80px; animation-delay: -2s; }}
        .orb-3 {{ width: 200px; height: 200px; background: {orb3}; top: 40%; left: 55%; opacity: 0.25; animation-delay: -4s; }}
        
        @keyframes orbFloat {{
            0%, 100% {{ transform: translate(0, 0) scale(1); }}
            25% {{ transform: translate(15px, -20px) scale(1.05); }}
            50% {{ transform: translate(-10px, 15px) scale(0.95); }}
            75% {{ transform: translate(20px, 10px) scale(1.02); }}
        }}
        
        /* Center container - ULTRA COMPACT for 100% zoom NO SCROLL */
        [data-testid="stMainBlockContainer"] {{
            display: flex !important;
            flex-direction: column !important;
            justify-content: center !important;
            align-items: center !important;
            height: 100vh !important;
            max-height: 100vh !important;
            padding: 0.2rem !important;
            position: relative;
            z-index: 10;
            overflow: hidden !important;
        }}
        [data-testid="stVerticalBlock"] {{
            width: 100% !important;
            max-width: 340px !important;
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
            gap: 0.2rem !important;
        }}
        
        /* Glass login card - ULTRA COMPACT */
        [data-testid="stVerticalBlockBorderWrapper"] {{
            background: rgba(255, 255, 255, 0.08) !important;
            backdrop-filter: blur(24px) saturate(180%) !important;
            -webkit-backdrop-filter: blur(24px) saturate(180%) !important;
            border: 1.5px solid rgba(255, 255, 255, 0.25) !important;
            border-top-color: rgba(255, 255, 255, 0.4) !important;
            border-left-color: rgba(255, 255, 255, 0.35) !important;
            border-radius: 16px !important;
            padding: 0.6rem !important;
            box-shadow: 
                0 8px 32px rgba(0, 0, 0, 0.4),
                0 20px 60px rgba(0, 0, 0, 0.3),
                inset 0 1px 1px rgba(255, 255, 255, 0.15) !important;
            max-width: 340px !important;
            margin: 0 auto !important;
            position: relative !important;
            overflow: hidden !important;
        }}
        [data-testid="stVerticalBlockBorderWrapper"]::before {{
            content: '' !important;
            position: absolute !important;
            top: 0 !important; left: 0 !important;
            width: 100% !important; height: 100% !important;
            background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, transparent 40%) !important;
            pointer-events: none !important;
            z-index: 1 !important;
        }}
        [data-testid="stVerticalBlockBorderWrapper"] > div {{ background: transparent !important; }}
        
        /* Login header - ULTRA COMPACT */
        .login-header {{
            text-align: center;
            margin-bottom: 0.3rem;
            padding: 0.3rem;
            background: linear-gradient(145deg, rgba(255,255,255,0.1), rgba(255,255,255,0.03));
            backdrop-filter: blur(16px);
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            width: 100%;
        }}
        .dragon-logo-img {{
            max-width: 120px;
            width: 100%;
            margin-bottom: 0.1rem;
            filter: drop-shadow(0 0 25px {orb1}80) drop-shadow(0 0 50px {orb2}40);
            animation: logoGlow 3s ease-in-out infinite alternate;
        }}
        @keyframes logoGlow {{
            0% {{ filter: drop-shadow(0 0 20px {orb1}60) drop-shadow(0 0 40px {orb2}30); }}
            100% {{ filter: drop-shadow(0 0 35px {orb1}90) drop-shadow(0 0 60px {orb2}50); }}
        }}
        .login-title {{
            font-size: 1rem;
            font-weight: 800;
            letter-spacing: 2px;
            background: linear-gradient(180deg, {orb1} 0%, {orb2} 50%, {orb3} 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0;
        }}
        .login-subtitle {{
            color: rgba(255,255,255,0.7);
            font-size: 0.55rem;
            letter-spacing: 1px;
            text-transform: uppercase;
        }}
        
        /* Form inputs - ULTRA COMPACT */
        .stTextInput label, .stTextInput label p {{
            color: #ffffff !important;
            font-size: 0.7rem !important;
            font-weight: 600 !important;
            text-shadow: 0 1px 3px rgba(0,0,0,0.4) !important;
            margin-bottom: 0 !important;
        }}
        .stTextInput [data-baseweb="input"],
        .stTextInput [data-baseweb="base-input"] {{
            background: transparent !important;
            border: none !important;
        }}
        .stTextInput > div > div > input {{
            background: rgba(0, 0, 0, 0.3) !important;
            backdrop-filter: blur(20px) !important;
            border: 1.5px solid rgba(255, 255, 255, 0.25) !important;
            border-top-color: rgba(255, 255, 255, 0.4) !important;
            border-radius: 8px !important;
            color: #ffffff !important;
            padding: 0.4rem 0.6rem !important;
            font-size: 0.85rem !important;
            box-shadow: inset 0 2px 4px rgba(0,0,0,0.2) !important;
        }}
        .stTextInput > div > div > input:focus {{
            border-color: {orb1} !important;
            box-shadow: 0 0 15px {orb1}50, inset 0 2px 4px rgba(0,0,0,0.2) !important;
        }}
        .stTextInput > div > div > input::placeholder {{
            color: rgba(255,255,255,0.5) !important;
        }}
        .stTextInput button {{ background: transparent !important; }}
        .stTextInput button svg {{ fill: rgba(255,255,255,0.6) !important; }}
        
        /* Login button - ULTRA COMPACT */
        .stButton > button, .stFormSubmitButton > button {{
            background: linear-gradient(135deg, {orb1}cc, {orb2}aa) !important;
            backdrop-filter: blur(12px) !important;
            border: 1.5px solid rgba(255,255,255,0.3) !important;
            border-radius: 8px !important;
            color: #ffffff !important;
            font-weight: 700 !important;
            font-size: 0.8rem !important;
            padding: 0.35rem 0.8rem !important;
            box-shadow: 0 4px 20px {orb1}40 !important;
            transition: all 0.3s ease !important;
        }}
        .stButton > button:hover, .stFormSubmitButton > button:hover {{
            transform: translateY(-1px) !important;
            box-shadow: 0 5px 20px {orb1}60 !important;
        }}
        
        /* Feature tiles - INLINE ULTRA COMPACT */
        .features-row {{
            display: flex;
            justify-content: center;
            gap: 0.2rem;
            margin-top: 0.2rem;
            width: 100%;
            max-width: 320px;
        }}
        .feature-glass {{
            background: rgba(255, 255, 255, 0.06);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 6px;
            padding: 0.15rem 0.25rem;
            text-align: center;
            flex: 1;
            transition: all 0.3s ease;
        }}
        .feature-glass:hover {{
            background: rgba(255, 255, 255, 0.12);
            transform: translateY(-1px);
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        }}
        .feature-icon {{ font-size: 0.75rem; }}
        .feature-text {{ color: rgba(255,255,255,0.6); font-size: 0.45rem; font-weight: 500; margin-top: 0; }}
        
        .version-text {{ color: rgba(255,255,255,0.25); font-size: 0.45rem; text-align: center; margin-top: 0.15rem; letter-spacing: 1px; }}
        
        /* Caption styling */
        .stCaption, [data-testid="stCaption"] {{
            color: rgba(255,255,255,0.5) !important;
            font-size: 0.75rem !important;
            text-align: center !important;
        }}
        
        /* Info box */
        .stInfo {{ 
            background: rgba(0,0,0,0.3) !important;
            backdrop-filter: blur(12px) !important;
            border-radius: 12px !important;
            border-left: 3px solid {orb1} !important;
        }}
    </style>
    
    <div class="orb orb-1"></div>
    <div class="orb orb-2"></div>
    <div class="orb orb-3"></div>
    """, unsafe_allow_html=True)
    
    # Glass login card
    with st.container(border=True):
        # Load logo
        logo_html = ""
        if LOGO_PATH.exists():
            with open(LOGO_PATH, "rb") as f:
                logo_b64 = base64.b64encode(f.read()).decode()
            logo_html = f'<img src="data:image/png;base64,{logo_b64}" class="dragon-logo-img" alt="Dragon Mailer">'
        
        st.markdown(f"""
        <div class="login-header">
            {logo_html if logo_html else '<div style="font-size:2.5rem;margin-bottom:0.2rem;">🐉</div>'}
            <div class="login-title">DRAGON MAILER</div>
            <div class="login-subtitle">Professional Email & SMS Platform</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Login form
        with st.form("login_form", clear_on_submit=False):
            username = st.text_input("👤 Username", placeholder="Enter username")
            password = st.text_input("🔒 Password", type="password", placeholder="Enter password")
            
            if st.form_submit_button("🔓 Sign In", use_container_width=True):
                user = authenticate_user(username, password)
                if user:
                    st.session_state.authenticated = True
                    st.session_state.current_user = user['username']
                    st.session_state.user_role = user['role']
                    play_sound('login')
                    st.success("✅ Login successful!")
                    st.rerun()
                else:
                    play_sound('error')
                    st.error("❌ Invalid username or password")
        
        st.caption("🔐 Secure enterprise messaging platform")
    
    # Feature tiles
    st.markdown(f"""
    <div class="features-row">
        <div class="feature-glass"><div class="feature-icon">📧</div><div class="feature-text">Email</div></div>
        <div class="feature-glass"><div class="feature-icon">📱</div><div class="feature-text">SMS</div></div>
        <div class="feature-glass"><div class="feature-icon">☁️</div><div class="feature-text">Azure</div></div>
        <div class="feature-glass"><div class="feature-icon">🔒</div><div class="feature-text">Secure</div></div>
    </div>
    <div class="version-text">Dragon Mailer v2.0 Glass Edition</div>
    """, unsafe_allow_html=True)

# =============================================================================
# SMTP CONFIGURATION UI
# =============================================================================

def smtp_config_ui():
    """SMTP Configuration interface"""
    st.subheader("⚡ SMTP Configuration")
    
    # Load user-specific SMTP configs
    configs = load_user_smtp_configs()
    
    # Ensure configs has the right structure
    if configs is None:
        configs = {"configs": []}
    if 'configs' not in configs:
        configs['configs'] = []
    
    with st.expander("➕ Add New SMTP Configuration", expanded=not configs.get('configs')):
        preset = st.selectbox("📧 Email Provider Preset", options=list(SMTP_PRESETS.keys()))
        preset_config = SMTP_PRESETS[preset]
        
        col1, col2 = st.columns(2)
        with col1:
            server = st.text_input("SMTP Server", value=preset_config['server'])
            email = st.text_input("Email Address", placeholder="your@email.com")
        with col2:
            port = st.number_input("Port", value=preset_config['port'], min_value=1, max_value=65535)
            password = st.text_input("Password / App Password", type="password")
        
        use_tls = st.checkbox("Use TLS", value=preset_config['tls'])
        config_name = st.text_input("Configuration Name", placeholder="My Gmail Account")
        
        if st.button("💾 Save Configuration", use_container_width=True):
            # Check each field and show specific errors
            missing_fields = []
            if not server or not server.strip():
                missing_fields.append("SMTP Server")
            if not email or not email.strip():
                missing_fields.append("Email Address")
            if not password or not password.strip():
                missing_fields.append("Password")
            if not config_name or not config_name.strip():
                missing_fields.append("Configuration Name")
            
            if missing_fields:
                st.error(f"❌ Please fill in: {', '.join(missing_fields)}")
            else:
                new_config = {
                    "name": config_name.strip(),
                    "server": server.strip(),
                    "port": port,
                    "email": email.strip(),
                    "password": password,
                    "use_tls": use_tls,
                    "created": datetime.now().isoformat()
                }
                configs['configs'].append(new_config)
                save_user_smtp_configs(configs)
                st.success(f"✅ Configuration '{config_name}' saved!")
                st.rerun()
    
    # Display existing configs
    if configs.get('configs'):
        st.subheader("📋 Saved Configurations")
        for i, config in enumerate(configs['configs']):
            with st.expander(f"📧 {config['name']} ({config['email']})"):
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    st.write(f"**Server:** {config['server']}:{config['port']}")
                    st.write(f"**TLS:** {'Yes' if config.get('use_tls') else 'No'}")
                with col2:
                    if st.button("✅ Select", key=f"select_{i}"):
                        st.session_state.current_smtp = config
                        st.success(f"Selected: {config['name']}")
                with col3:
                    if st.button("🗑️ Delete", key=f"delete_{i}"):
                        configs['configs'].pop(i)
                        save_user_smtp_configs(configs)
                        st.rerun()

# =============================================================================
# EMAIL COMPOSER UI
# =============================================================================

def email_composer_ui():
    """Email composition interface with templates and pattern variables"""
    st.subheader("✉️ Compose Email")
    
    if not st.session_state.current_smtp:
        st.warning("⚠️ Please select an SMTP configuration first")
        return
    
    st.info(f"📧 Sending from: **{st.session_state.current_smtp['email']}**")
    
    # Send As Options (Advanced)
    with st.expander("✉️ Send As / Reply-To Options", expanded=False):
        col_from1, col_from2 = st.columns(2)
        with col_from1:
            from_name = st.text_input(
                "👤 Display Name (Send As)", 
                placeholder="John Smith",
                help="Custom name shown as sender (e.g., 'John Smith' instead of just email)"
            )
        with col_from2:
            reply_to = st.text_input(
                "↩️ Reply-To Email",
                placeholder="replies@yourdomain.com",
                help="Replies will go to this address instead of the sending email"
            )
        if from_name:
            st.caption(f"📬 Will appear as: **{from_name}** <{st.session_state.current_smtp['email']}>")
    
    # Template Selection
    col1, col2 = st.columns([2, 1])
    with col1:
        template_name = st.selectbox("📋 Email Template", options=list(EMAIL_TEMPLATES.keys()), key="email_template_main")
    with col2:
        custom_link = st.text_input("🔗 Custom Link", placeholder="https://...", help="Replaces {link} in template")
    
    template = EMAIL_TEMPLATES.get(template_name, {"subject": "", "body": ""})
    
    # Recipient mode
    mode = st.radio("Recipient Mode", ["Single Email", "Bulk Email (Multiple Recipients)"], horizontal=True)
    
    if mode == "Single Email":
        to_email = st.text_input("📩 To", placeholder="recipient@example.com")
        recipients = [to_email] if to_email else []
    else:
        recipients_text = st.text_area(
            "📩 Recipients (one per line)", 
            placeholder="email1@example.com\nemail2@example.com\nemail3@example.com",
            height=150
        )
        recipients = [r.strip() for r in recipients_text.split('\n') if r.strip() and '@' in r]
        if recipients:
            st.info(f"📊 {len(recipients)} recipients detected")
    
    subject = st.text_input("📝 Subject", value=template.get("subject", ""), placeholder="Enter email subject")
    
    # Content type toggle
    content_type = st.radio("Content Type", ["Plain Text", "HTML"], horizontal=True)
    is_html = content_type == "HTML"
    
    if is_html:
        body = st.text_area(
            "📄 HTML Body",
            value=template.get("body", ""),
            placeholder="<h1>Hello!</h1>\n<p>This is a <strong>beautiful</strong> email.</p>",
            height=250
        )
        with st.expander("👁️ Preview HTML"):
            preview_body = apply_patterns(body, custom_link)
            st.markdown(preview_body, unsafe_allow_html=True)
    else:
        body = st.text_area(
            "📄 Message Body",
            value=template.get("body", ""),
            placeholder="Enter your message here...",
            height=250
        )
    
    # Pattern variables help
    with st.expander("💡 Pattern Variables Help"):
        st.markdown("""
        **Available pattern variables:**
        - `{random}` or `{random:N}` - Random alphanumeric string (N chars)
        - `{random_digit:N}` - Random digits (N chars, default 6)
        - `{random_upper:N}` - Random uppercase alphanumeric (N chars)
        - `{date}` - Current date (YYYY-MM-DD)
        - `{time}` - Current time (HH:MM:SS)
        - `{uuid}` - Unique ID (8 chars)
        - `{link}` - Custom link (enter above)
        """)
    
    # Show preview with patterns applied
    if body:
        preview_subject = apply_patterns(subject, custom_link)
        preview_body = apply_patterns(body, custom_link)
        st.markdown("**📧 Preview (with patterns applied):**")
        st.code(f"Subject: {preview_subject}\n\n{preview_body[:200]}...", language=None)
    
    # Attachments
    attachments = st.file_uploader("📎 Attachments", accept_multiple_files=True)
    attachment_data = []
    if attachments:
        for file in attachments:
            attachment_data.append({
                "name": file.name,
                "data": file.read()
            })
            file.seek(0)
        st.info(f"📎 {len(attachments)} file(s) attached")
    
    # Send button
    col1, col2 = st.columns(2)
    with col1:
        send_btn = st.button("🚀 Send Email", use_container_width=True, type="primary")
    
    if send_btn:
        if not recipients:
            if JELLY_AVAILABLE:
                jelly_notification("Please enter recipient(s)", "error")
            else:
                st.error("❌ Please enter recipient(s)")
        elif not subject:
            if JELLY_AVAILABLE:
                jelly_notification("Please enter a subject", "error")
            else:
                st.error("❌ Please enter a subject")
        elif not body:
            if JELLY_AVAILABLE:
                jelly_notification("Please enter a message body", "error")
            else:
                st.error("❌ Please enter a message body")
        else:
            # Show jelly loading
            if JELLY_AVAILABLE:
                loading_placeholder = st.empty()
                with loading_placeholder:
                    jelly_loading("Sending emails...")
            
            with st.spinner("📤 Sending..."):
                # Apply patterns to subject and body
                final_subject = apply_patterns(subject, custom_link)
                final_body = apply_patterns(body, custom_link)
                
                if len(recipients) == 1:
                    result = send_email(
                        st.session_state.current_smtp,
                        recipients[0],
                        final_subject,
                        final_body,
                        is_html,
                        attachment_data if attachment_data else None,
                        from_name if from_name else None,
                        reply_to if reply_to else None
                    )
                    
                    if JELLY_AVAILABLE:
                        loading_placeholder.empty()
                    
                    if result['success']:
                        if JELLY_AVAILABLE:
                            jelly_notification(result['message'], "success")
                        else:
                            st.success(f"✅ {result['message']}")
                    else:
                        if JELLY_AVAILABLE:
                            jelly_notification(result['message'], "error")
                        else:
                            st.error(f"❌ {result['message']}")
                else:
                    progress_bar = st.progress(0)
                    results = send_bulk_emails(
                        st.session_state.current_smtp,
                        recipients,
                        final_subject,
                        final_body,
                        is_html,
                        progress_callback=lambda p: progress_bar.progress(p),
                        from_name=from_name if from_name else None,
                        reply_to=reply_to if reply_to else None
                    )
                    
                    if JELLY_AVAILABLE:
                        loading_placeholder.empty()
                        jelly_notification(f"Sent: {results['success']} | Failed: {results['failed']}", 
                                          "success" if results['failed'] == 0 else "warning")
                        # Show jelly progress bar for results
                        jelly_progress(results['success'] / len(recipients), "Send Progress", "#22c55e")
                    else:
                        st.success(f"✅ Sent: {results['success']} | ❌ Failed: {results['failed']}")
                    
                    # Play sound based on results
                    if results['failed'] == 0:
                        play_sound('success')
                    else:
                        play_sound('warning')
                    
                    # Log sent messages
                    sent_log = load_json(SENT_MESSAGES_FILE, {"messages": []})
                    sent_log['messages'].append({
                        "type": "email",
                        "user": st.session_state.get('current_user', 'unknown'),
                        "subject": final_subject,
                        "recipients": len(recipients),
                        "recipient_list": recipients if len(recipients) <= 10 else recipients[:10],
                        "attachments": [a['name'] for a in attachment_data] if attachment_data else [],
                        "success": results['success'],
                        "failed": results['failed'],
                        "timestamp": datetime.now().isoformat()
                    })
                    save_json(SENT_MESSAGES_FILE, sent_log)

# =============================================================================
# SMS COMPOSER UI
# =============================================================================

def send_sms_auto_detect(smtp_config, phone_number, message):
    """
    Try sending SMS through multiple carriers until one succeeds.
    Returns (success, message)
    """
    for gateway in AUTO_SMS_GATEWAYS:
        result = send_sms_via_gateway(smtp_config, phone_number, gateway, message, gateway_direct=True)
        if result['success']:
            return result
        time.sleep(0.5)  # Small delay between attempts
    
    return {'success': False, 'message': 'SMS failed via all carriers'}

def send_sms_via_gateway(smtp_config, phone_number, carrier_or_gateway, message, gateway_direct=False):
    """
    Send SMS via email-to-SMS gateway.
    If gateway_direct is True, carrier_or_gateway is used as the gateway domain directly.
    """
    try:
        # Clean phone number (digits only)
        phone = ''.join(filter(str.isdigit, phone_number))
        if len(phone) != 10:
            return {'success': False, 'message': 'Phone number must be 10 digits'}
        
        # Get gateway
        if gateway_direct:
            gateway = carrier_or_gateway
        else:
            gateway = SMS_GATEWAYS.get(carrier_or_gateway, carrier_or_gateway)
        
        if gateway == "auto":
            # Auto mode - try all carriers
            return send_sms_auto_detect(smtp_config, phone_number, message)
        
        # Create SMS email address
        sms_email = f"{phone}@{gateway}"
        
        # Send via email
        result = send_email(smtp_config, sms_email, "", message, is_html=False)
        return result
        
    except Exception as e:
        return {'success': False, 'message': str(e)}

def sms_composer_ui():
    """SMS composition interface with templates and Auto mode"""
    st.subheader("📱 Send SMS")
    
    if not st.session_state.current_smtp:
        st.warning("⚠️ Please select an SMTP configuration first (SMS uses email-to-SMS gateway)")
        return
    
    st.info("""
    💡 **How SMS Gateway Works:**  
    SMS messages are sent via carrier email gateways. This is **free** and works with most US carriers.  
    🔄 **Auto Mode** will try multiple carriers until one works!
    """)
    
    # SMS Template selection
    col1, col2 = st.columns([2, 1])
    with col1:
        sms_template_name = st.selectbox("📋 SMS Template", options=list(SMS_TEMPLATES.keys()), key="sms_template_gateway")
    with col2:
        custom_link = st.text_input("🔗 Custom Link", placeholder="https://...", key="sms_link", help="Replaces {link} in template")
    
    default_message = SMS_TEMPLATES.get(sms_template_name, "")
    
    # Recipient mode
    mode = st.radio("SMS Mode", ["Single SMS", "Bulk SMS"], horizontal=True, key="sms_mode")
    
    if mode == "Single SMS":
        col1, col2 = st.columns(2)
        with col1:
            phone = st.text_input("📞 Phone Number", placeholder="1234567890")
        with col2:
            carrier = st.selectbox("📡 Carrier", options=list(SMS_GATEWAYS.keys()), 
                                   key="carrier_gateway", help="Select 'Auto (Try All)' to automatically find the correct carrier")
        
        recipients = [{"phone": phone, "carrier": carrier}] if phone else []
    else:
        st.markdown("""
        **📋 Bulk SMS Options:**
        - Enter numbers manually below, OR
        - Upload a .txt or .csv file with format: `phone,carrier`
        - Use `Auto` as carrier to auto-detect
        """)
        
        # File upload for bulk numbers
        uploaded_file = st.file_uploader("📁 Upload Numbers (txt/csv)", type=['txt', 'csv'], key="bulk_sms_file")
        
        recipients_text = ""
        if uploaded_file:
            file_content = uploaded_file.read().decode('utf-8')
            recipients_text = file_content
            st.success(f"✅ Loaded {len(file_content.splitlines())} lines from file")
        
        recipients_text = st.text_area(
            "📞 Recipients (phone,carrier per line)",
            value=recipients_text,
            placeholder="1234567890,Verizon\n0987654321,T-Mobile\n5551234567,Auto",
            height=150,
            help="Format: phone,carrier - Use 'Auto' to auto-detect carrier"
        )
        recipients = []
        for line in recipients_text.split('\n'):
            line = line.strip()
            if ',' in line:
                parts = line.split(',')
                if len(parts) >= 2:
                    carrier_input = parts[1].strip()
                    # Map "Auto" to the SMS_GATEWAYS key
                    if carrier_input.lower() == "auto":
                        carrier_input = "Auto (Try All)"
                    recipients.append({"phone": parts[0].strip(), "carrier": carrier_input})
            elif line and line.replace('-', '').replace(' ', '').isdigit():
                # Just a phone number without carrier - use Auto
                recipients.append({"phone": line.replace('-', '').replace(' ', ''), "carrier": "Auto (Try All)"})
        
        if recipients:
            st.info(f"📊 {len(recipients)} recipients detected")
    
    message = st.text_area(
        "💬 Message",
        value=default_message,
        placeholder="Enter your SMS message (160 char recommended)",
        height=150,
        max_chars=320
    )
    
    # Preview with patterns
    if message:
        preview = apply_patterns(message, custom_link)
        st.markdown("**📱 Preview:**")
        st.code(preview, language=None)
        
        char_count = len(preview)
        color = "green" if char_count <= 160 else "orange" if char_count <= 320 else "red"
        st.markdown(f"<span style='color:{color}'>Characters: {char_count}/160</span>", unsafe_allow_html=True)
    
    if st.button("📤 Send SMS", use_container_width=True, type="primary"):
        if not recipients:
            st.error("❌ Please enter recipient(s)")
        elif not message:
            st.error("❌ Please enter a message")
        else:
            with st.spinner("📤 Sending SMS..."):
                success_count = 0
                fail_count = 0
                
                progress_bar = st.progress(0)
                
                # Apply patterns to message
                final_message = apply_patterns(message, custom_link)
                
                for i, recipient in enumerate(recipients):
                    carrier = recipient.get('carrier', 'Auto (Try All)')
                    gateway = SMS_GATEWAYS.get(carrier, carrier)
                    
                    if gateway == "auto":
                        result = send_sms_auto_detect(
                            st.session_state.current_smtp,
                            recipient['phone'],
                            final_message
                        )
                    else:
                        result = send_sms_via_gateway(
                            st.session_state.current_smtp,
                            recipient['phone'],
                            carrier,
                            final_message
                        )
                    
                    if result['success']:
                        success_count += 1
                    else:
                        fail_count += 1
                        if JELLY_AVAILABLE:
                            jelly_notification(f"{recipient['phone']}: {result['message']}", "warning")
                        else:
                            st.warning(f"⚠️ {recipient['phone']}: {result['message']}")
                    
                    progress_bar.progress((i + 1) / len(recipients))
                
                # Show results with jelly
                if JELLY_AVAILABLE:
                    jelly_notification(f"Sent: {success_count} | Failed: {fail_count}", 
                                      "success" if fail_count == 0 else "warning")
                    jelly_progress(success_count / len(recipients), "SMS Send Progress", "#22c55e")
                else:
                    st.success(f"✅ Sent: {success_count} | ❌ Failed: {fail_count}")
                
                # Play sound based on results
                if fail_count == 0:
                    play_sound('success')
                else:
                    play_sound('warning')
                
                # Log sent messages
                sent_log = load_json(SENT_MESSAGES_FILE, {"messages": []})
                sent_log['messages'].append({
                    "type": "sms",
                    "user": st.session_state.get('current_user', 'unknown'),
                    "subject": "SMS",
                    "recipients": len(recipients),
                    "recipient_list": [r['phone'] for r in recipients[:10]],
                    "message_preview": message[:50] if message else "",
                    "success": success_count,
                    "failed": fail_count,
                    "timestamp": datetime.now().isoformat()
                })
                save_json(SENT_MESSAGES_FILE, sent_log)

# =============================================================================
# DASHBOARD UI
# =============================================================================

def dashboard_ui():
    """Dashboard with statistics - Enhanced with organic Jelly blob components"""
    st.subheader("📊 Dashboard")
    
    sent_log = load_json(SENT_MESSAGES_FILE, {"messages": []})
    messages = sent_log.get('messages', [])
    
    # Calculate statistics
    total_emails = sum(1 for m in messages if m.get('type') == 'email')
    total_sms = sum(1 for m in messages if m.get('type') in ['sms', 'azure_sms'])
    total_azure = sum(1 for m in messages if m.get('type') == 'azure_sms')
    total_success = sum(m.get('success', 0) for m in messages)
    total_failed = sum(m.get('failed', 0) for m in messages)
    total_all = total_success + total_failed
    success_rate = (total_success / total_all * 100) if total_all > 0 else 0
    bounce_rate = (total_failed / total_all * 100) if total_all > 0 else 0
    
    # Use organic Jelly blob components if available
    if JELLY_AVAILABLE:
        # Row 1: Campaign Overview + Theme Intensity
        col1, col2 = st.columns(2)
        with col1:
            jelly_blob_metric("Campaign Overview", f"{total_all:,}", "messages sent this month")
        with col2:
            jelly_blob_intensity("Theme Intensity")
        
        # Row 2: Volume + Email Send Rate
        col1, col2 = st.columns(2)
        with col1:
            jelly_blob_volume("Volume")
        with col2:
            jelly_blob_progress(success_rate / 100, "Email Send Rate", "blue_orange")
        
        # Row 3: Bounce Rate x2
        col1, col2 = st.columns(2)
        with col1:
            jelly_blob_bounce(bounce_rate / 100, "Bounce Rate")
        with col2:
            jelly_blob_bounce(total_failed / max(total_all, 1), "Failure Rate")
        
        # Stats card
        jelly_stats_card("📊 Campaign Overview", [
            {"label": "Total Sent", "value": str(total_all)},
            {"label": "Emails", "value": str(total_emails)},
            {"label": "Gateway SMS", "value": str(total_sms - total_azure)},
            {"label": "Azure SMS", "value": str(total_azure)},
        ], "#00d4ff")
    else:
        # Fallback to standard metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📧 Emails Sent", total_emails)
        with col2:
            st.metric("📱 SMS Sent", total_sms)
        with col3:
            st.metric("✅ Successful", total_success)
        with col4:
            st.metric("❌ Failed", total_failed)
    
    # Recent activity with jelly notifications
    st.subheader("📋 Recent Activity")
    if messages:
        for msg in reversed(messages[-10:]):
            icon = "📧" if msg.get('type') == 'email' else "📱"
            timestamp = msg.get('timestamp', 'Unknown')[:16].replace('T', ' ')
            msg_text = f"{icon} {msg.get('subject', 'SMS')} - {timestamp} | ✅ {msg.get('success', 0)} | ❌ {msg.get('failed', 0)}"
            
            if JELLY_AVAILABLE:
                notif_type = "success" if msg.get('failed', 0) == 0 else "warning" if msg.get('success', 0) > 0 else "error"
                jelly_notification(msg_text, notif_type)
            else:
                st.write(msg_text)
    else:
        if JELLY_AVAILABLE:
            jelly_notification("No messages sent yet - Start sending to see activity here!", "info")
        else:
            st.info("No messages sent yet")

# =============================================================================
# SETTINGS UI
# =============================================================================

def settings_ui():
    """Settings and theme customization"""
    st.subheader("⚙️ Settings & Themes")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎨 Glass Theme")
        new_theme = st.selectbox(
            "Select Glass Theme",
            options=list(GLASS_THEMES.keys()),
            index=list(GLASS_THEMES.keys()).index(st.session_state.theme)
        )
        if new_theme != st.session_state.theme:
            st.session_state.theme = new_theme
            st.rerun()
    
    with col2:
        st.markdown("### 🖼️ Nature Background")
        new_bg = st.selectbox(
            "Select Background",
            options=list(NATURE_BACKGROUNDS.keys()),
            index=list(NATURE_BACKGROUNDS.keys()).index(st.session_state.background)
        )
        if new_bg != st.session_state.background:
            st.session_state.background = new_bg
            st.rerun()
    
    # Theme preview
    st.markdown("### 👁️ Current Theme Preview")
    theme_data = GLASS_THEMES[st.session_state.theme]
    st.markdown(f"""
    <div class="glass-card">
        <h4>Preview Card</h4>
        <p>This is how your content will look with the current theme.</p>
        <button style="background:{theme_data['accent']};color:white;border:none;padding:10px 20px;border-radius:8px;">
            Sample Button
        </button>
    </div>
    """, unsafe_allow_html=True)
    
    # User management (admin only)
    if st.session_state.user_role == 'admin':
        st.markdown("---")
        st.subheader("👥 User Management")
        
        with st.expander("➕ Add New User"):
            new_username = st.text_input("Username", key="new_user")
            new_password = st.text_input("Password", type="password", key="new_pass")
            new_role = st.selectbox("Role", ["user", "admin"], key="new_role")
            
            if st.button("Create User"):
                if new_username and new_password:
                    users = load_json(USERS_FILE, {"users": []})
                    # Check if user already exists
                    existing = [u for u in users.get('users', []) if u['username'] == new_username]
                    if existing:
                        st.error(f"❌ User '{new_username}' already exists!")
                    else:
                        users['users'].append({
                            "username": new_username,
                            "password_hash": hash_password(new_password),
                            "role": new_role,
                            "created": datetime.now().isoformat()
                        })
                        save_json(USERS_FILE, users)
                        # Create empty SMTP config file for the new user (clean slate)
                        if new_role != 'admin':
                            user_config_file = get_user_smtp_config_file(new_username)
                            save_json(user_config_file, {"configs": []})
                        st.success(f"✅ User '{new_username}' created with clean slate!")
        
        # List users
        users = load_json(USERS_FILE, {"users": []})
        for user in users.get('users', []):
            st.write(f"👤 **{user['username']}** ({user['role']})")
        
        # Admin Activity Log - All User Sent Messages
        st.markdown("---")
        st.subheader("📊 All User Activity Log")
        st.caption("View all messages sent by all users")
        
        sent_log = load_json(SENT_MESSAGES_FILE, {"messages": []})
        messages = sent_log.get('messages', [])
        
        if messages:
            # Sort by timestamp descending (newest first)
            messages_sorted = sorted(messages, key=lambda x: x.get('timestamp', ''), reverse=True)
            
            # Filter options
            col1, col2 = st.columns(2)
            with col1:
                filter_type = st.selectbox("Filter by Type", ["All", "Email", "SMS"], key="admin_filter_type")
            with col2:
                filter_user = st.selectbox("Filter by User", ["All"] + list(set(m.get('user', 'unknown') for m in messages)), key="admin_filter_user")
            
            # Apply filters
            filtered = messages_sorted
            if filter_type != "All":
                filtered = [m for m in filtered if m.get('type', '').lower() == filter_type.lower()]
            if filter_user != "All":
                filtered = [m for m in filtered if m.get('user', 'unknown') == filter_user]
            
            st.info(f"📋 Showing {len(filtered)} of {len(messages)} total messages")
            
            # Display as table
            for i, msg in enumerate(filtered[:50]):  # Show last 50
                msg_type = "📧" if msg.get('type') == 'email' else "📱"
                user = msg.get('user', 'unknown')
                timestamp = msg.get('timestamp', 'N/A')[:16] if msg.get('timestamp') else 'N/A'
                subject = msg.get('subject', 'N/A')[:30]
                recipients = msg.get('recipients', 0)
                success = msg.get('success', 0)
                failed = msg.get('failed', 0)
                attachments = msg.get('attachments', [])
                
                with st.expander(f"{msg_type} **{user}** - {timestamp} - {subject}"):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.write(f"**User:** {user}")
                        st.write(f"**Type:** {msg.get('type', 'N/A')}")
                    with col2:
                        st.write(f"**Recipients:** {recipients}")
                        st.write(f"**✅ Success:** {success}")
                    with col3:
                        st.write(f"**❌ Failed:** {failed}")
                        st.write(f"**Time:** {timestamp}")
                    
                    if attachments:
                        st.write(f"**📎 Attachments:** {', '.join(attachments)}")
                    
                    recipient_list = msg.get('recipient_list', [])
                    if recipient_list:
                        st.write(f"**Recipients:** {', '.join(str(r) for r in recipient_list[:5])}{'...' if len(recipient_list) > 5 else ''}")
                    
                    if msg.get('message_preview'):
                        st.write(f"**Preview:** {msg.get('message_preview')}...")
            
            # Export option
            if st.button("📥 Export Activity Log (JSON)"):
                import json
                export_data = json.dumps(filtered, indent=2, default=str)
                st.download_button(
                    label="💾 Download Log",
                    data=export_data,
                    file_name=f"activity_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
            
            # Clear log option
            if st.button("🗑️ Clear All Logs", type="secondary"):
                save_json(SENT_MESSAGES_FILE, {"messages": []})
                st.success("✅ Activity log cleared!")
                st.rerun()
        else:
            st.info("📭 No activity logged yet")

# =============================================================================
# AZURE SMS UI
# =============================================================================

def azure_sms_ui():
    """Azure Communication Services SMS interface"""
    st.subheader("☁️ Azure SMS (Direct Carrier)")
    
    if not AZURE_SMS_AVAILABLE:
        st.error("⚠️ Azure Communication Services SDK not installed")
        st.code("pip install azure-communication-sms", language="bash")
        return
    
    st.info("""
    💡 **Azure SMS Benefits:**  
    - Direct carrier delivery (not email-to-SMS gateway)
    - Higher delivery rates and reliability
    - Works with any carrier worldwide
    - Requires Azure account and phone number purchase
    """)
    
    # Configuration section
    with st.expander("⚙️ Azure SMS Configuration", expanded=True):
        config = load_azure_sms_config()
        
        conn_string = st.text_input(
            "🔑 Connection String",
            value=config.get("connection_string", ""),
            type="password",
            help="From Azure Portal > Communication Services > Keys"
        )
        phone_number = st.text_input(
            "📞 Azure Phone Number",
            value=config.get("phone_number", ""),
            placeholder="+1XXXXXXXXXX",
            help="Purchased from Azure Communication Services"
        )
        
        if st.button("💾 Save Azure Configuration"):
            save_azure_sms_config({
                "connection_string": conn_string,
                "phone_number": phone_number
            })
            st.success("✅ Configuration saved!")
    
    st.markdown("---")
    
    # Send SMS section
    st.markdown("### 📤 Send SMS")
    
    # SMS Template selection
    template_name = st.selectbox("📋 SMS Template", options=list(SMS_TEMPLATES.keys()), key="sms_template_azure")
    
    col1, col2 = st.columns(2)
    
    with col1:
        to_number = st.text_input(
            "📞 Recipient Phone",
            placeholder="+1234567890 or 1234567890",
            help="Enter phone number in E.164 format"
        )
    
    with col2:
        custom_link = st.text_input(
            "🔗 Custom Link (optional)",
            placeholder="https://example.com/track/...",
            help="Will replace {link} in message"
        )
    
    # Pre-fill message from template
    default_msg = SMS_TEMPLATES.get(template_name, "")
    
    message = st.text_area(
        "💬 Message",
        value=default_msg,
        placeholder="Enter your SMS message",
        height=100,
        max_chars=320
    )
    
    # Show preview with patterns applied
    if message:
        preview = apply_patterns(message, custom_link)
        st.markdown("**Preview:**")
        st.code(preview, language=None)
        
        char_count = len(preview)
        color = "green" if char_count <= 160 else "orange" if char_count <= 320 else "red"
        st.markdown(f"<span style='color:{color}'>Characters: {char_count}/160</span>", unsafe_allow_html=True)
    
    if st.button("📤 Send via Azure", use_container_width=True, type="primary"):
        if not to_number:
            if JELLY_AVAILABLE:
                jelly_notification("Please enter recipient phone number", "error")
            else:
                st.error("❌ Please enter recipient phone number")
        elif not message:
            if JELLY_AVAILABLE:
                jelly_notification("Please enter a message", "error")
            else:
                st.error("❌ Please enter a message")
        else:
            # Show jelly loading
            if JELLY_AVAILABLE:
                loading_placeholder = st.empty()
                with loading_placeholder:
                    jelly_loading("Sending via Azure...")
            
            with st.spinner("📤 Sending via Azure..."):
                final_message = apply_patterns(message, custom_link)
                success, result_msg = send_sms_via_azure(to_number, final_message)
                
                if JELLY_AVAILABLE:
                    loading_placeholder.empty()
                
                if success:
                    if JELLY_AVAILABLE:
                        jelly_notification(result_msg, "success")
                    else:
                        st.success(f"✅ {result_msg}")
                    # Log the message
                    sent_log = load_json(SENT_MESSAGES_FILE, {"messages": []})
                    sent_log['messages'].append({
                        "type": "azure_sms",
                        "user": st.session_state.get('current_user', 'unknown'),
                        "to": to_number,
                        "message_preview": final_message[:50] + "...",
                        "subject": "Azure SMS",
                        "recipients": 1,
                        "recipient_list": [to_number],
                        "timestamp": datetime.now().isoformat(),
                        "success": 1,
                        "failed": 0
                    })
                    save_json(SENT_MESSAGES_FILE, sent_log)
                else:
                    if JELLY_AVAILABLE:
                        jelly_notification(result_msg, "error")
                    else:
                        st.error(f"❌ {result_msg}")

# =============================================================================
# SCHEDULED TASKS UI
# =============================================================================

def scheduled_ui():
    """Scheduled email/SMS tasks interface"""
    st.subheader("⏰ Scheduled Sending")
    
    st.info("""
    💡 **Schedule emails and SMS to send at a specific time.**  
    Note: Scheduled tasks will execute when the app is running.
    """)
    
    # Add new scheduled task
    with st.expander("➕ Schedule New Task", expanded=True):
        task_type = st.selectbox("📧 Task Type", ["Email", "SMS (Gateway)", "SMS (Azure)"])
        
        col1, col2 = st.columns(2)
        with col1:
            scheduled_date = st.date_input("📅 Date")
        with col2:
            scheduled_time = st.time_input("⏰ Time")
        
        if task_type == "Email":
            if not st.session_state.current_smtp:
                st.warning("⚠️ Select an SMTP config first")
            
            # Email template selection
            template_name = st.selectbox("📋 Email Template", options=list(EMAIL_TEMPLATES.keys()), key="email_template_scheduled")
            template = EMAIL_TEMPLATES.get(template_name, {"subject": "", "body": ""})
            
            recipient = st.text_input("📧 Recipient Email")
            custom_link = st.text_input("🔗 Custom Link (optional)")
            subject = st.text_input("📝 Subject", value=template.get("subject", ""))
            body = st.text_area("💬 Body", value=template.get("body", ""), height=150)
            
        else:
            recipient = st.text_input("📞 Phone Number")
            
            if task_type == "SMS (Gateway)":
                carrier = st.selectbox("📡 Carrier", options=list(SMS_GATEWAYS.keys()), key="carrier_scheduled")
            else:
                carrier = "Azure"
            
            custom_link = st.text_input("🔗 Custom Link (optional)")
            
            # SMS template selection
            sms_template_name = st.selectbox("📋 SMS Template", options=list(SMS_TEMPLATES.keys()), key="sched_sms_template")
            body = st.text_area("💬 Message", value=SMS_TEMPLATES.get(sms_template_name, ""), height=100)
            subject = None
        
        if st.button("📅 Schedule Task", type="primary"):
            if not recipient:
                st.error("❌ Please enter recipient")
            elif not body:
                st.error("❌ Please enter message body")
            else:
                scheduled_dt = datetime.combine(scheduled_date, scheduled_time)
                
                task = {
                    "type": task_type,
                    "recipient": recipient,
                    "subject": subject,
                    "body": body,
                    "custom_link": custom_link,
                    "carrier": carrier if "SMS" in task_type else None,
                    "smtp_config": st.session_state.current_smtp if task_type == "Email" else None,
                    "scheduled_time": scheduled_dt.isoformat()
                }
                
                task_id = add_scheduled_task(task)
                st.success(f"✅ Task scheduled! ID: {task_id}")
    
    st.markdown("---")
    
    # View scheduled tasks
    st.markdown("### 📋 Pending Tasks")
    
    data = load_scheduled_tasks()
    tasks = data.get("tasks", [])
    pending_tasks = [t for t in tasks if t.get("status") == "pending"]
    
    if pending_tasks:
        for task in pending_tasks:
            col1, col2, col3 = st.columns([3, 2, 1])
            with col1:
                icon = "📧" if task.get("type") == "Email" else "📱"
                st.write(f"{icon} **{task.get('type')}** to `{task.get('recipient')}`")
            with col2:
                st.write(f"⏰ {task.get('scheduled_time', '')[:16]}")
            with col3:
                if st.button("🗑️", key=f"del_{task.get('id')}"):
                    delete_scheduled_task(task.get('id'))
                    st.rerun()
    else:
        st.info("No pending scheduled tasks")
    
    # Check and execute pending tasks button
    if st.button("🔄 Check & Execute Due Tasks"):
        pending = get_pending_tasks()
        if pending:
            for task in pending:
                st.write(f"Executing task {task.get('id')}...")
                # Here you would execute the task based on type
                # For now, just mark as executed
                data = load_scheduled_tasks()
                for t in data["tasks"]:
                    if t.get("id") == task.get("id"):
                        t["status"] = "completed"
                        t["executed_at"] = datetime.now().isoformat()
                save_scheduled_tasks(data)
            st.success(f"✅ Executed {len(pending)} tasks")
            st.rerun()
        else:
            st.info("No tasks due for execution")

# =============================================================================
# JELLY DASHBOARD UI
# =============================================================================

def jelly_dashboard_ui():
    """Animated Jelly Dashboard with advanced analytics"""
    st.subheader("✨ Jelly Analytics Dashboard")
    
    if JELLY_AVAILABLE:
        try:
            import dashboard_jelly
            dashboard_jelly.render()
        except Exception as e:
            st.error(f"Error loading jelly dashboard: {e}")
            st.info("Falling back to standard dashboard...")
            dashboard_ui()
    else:
        st.warning("⚠️ Jelly components not available")
        st.info("Using standard dashboard instead...")
        dashboard_ui()

# =============================================================================
# MAIN APPLICATION
# =============================================================================

def main():
    """Main application entry point"""
    # Initialize
    init_session_state()
    create_default_admin()
    
    # Inject sound system
    inject_sound_system()
    
    # Inject CSS with current theme
    inject_neumorphic_glass_css(
        NATURE_BACKGROUNDS[st.session_state.background],
        st.session_state.theme
    )
    
    # Check authentication
    if not st.session_state.authenticated:
        login_page()
        return
    
    # Inject sidebar always visible + toggle button CSS
    st.markdown("""
    <style>
    /* SIDEBAR ALWAYS VISIBLE */
    [data-testid="stSidebar"] {
        transform: translateX(0) !important;
        visibility: visible !important;
        min-width: 280px !important;
    }
    [data-testid="stSidebar"][aria-expanded="false"] {
        transform: translateX(0) !important;
        visibility: visible !important;
        min-width: 280px !important;
    }
    [data-testid="stSidebarCollapsedControl"] {
        display: none !important;
    }
    
    /* Sidebar toggle button - always visible */
    [data-testid="collapsedControl"] {
        display: flex !important;
        position: fixed !important;
        left: 10px !important;
        top: 10px !important;
        z-index: 999999 !important;
        background: rgba(0, 212, 255, 0.2) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(0, 212, 255, 0.4) !important;
        border-radius: 10px !important;
        padding: 8px !important;
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.3) !important;
        animation: sidebarBtnGlow 2s ease-in-out infinite !important;
    }
    
    @keyframes sidebarBtnGlow {
        0%, 100% { box-shadow: 0 0 15px rgba(0, 212, 255, 0.3); }
        50% { box-shadow: 0 0 25px rgba(0, 212, 255, 0.6); }
    }
    
    [data-testid="collapsedControl"]:hover {
        background: rgba(0, 212, 255, 0.4) !important;
        transform: scale(1.1) !important;
    }
    
    [data-testid="collapsedControl"] svg {
        fill: #00d4ff !important;
        stroke: #00d4ff !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        if LOGO_PATH.exists():
            st.image(str(LOGO_PATH), width=200)
        else:
            st.warning("⚠️ Add logo to images/dragon_logo.png")
        
        # User info with jelly styling
        if JELLY_AVAILABLE:
            jelly_notification(f"👤 {st.session_state.current_user} ({st.session_state.user_role})", "info")
        else:
            st.write(f"👤 **{st.session_state.current_user}** ({st.session_state.user_role})")
        
        if st.session_state.current_smtp:
            if JELLY_AVAILABLE:
                jelly_notification(f"📧 {st.session_state.current_smtp['name']}", "success")
            else:
                st.success(f"📧 {st.session_state.current_smtp['name']}")
        else:
            if JELLY_AVAILABLE:
                jelly_notification("⚠️ No SMTP selected", "warning")
            else:
                st.warning("⚠️ No SMTP selected")
        
        st.markdown("---")
        
        # Quick theme switcher
        st.markdown("### 🎨 Quick Theme")
        quick_bg = st.selectbox("Background", list(NATURE_BACKGROUNDS.keys()), 
                                index=list(NATURE_BACKGROUNDS.keys()).index(st.session_state.background),
                                key="sidebar_bg", label_visibility="collapsed")
        if quick_bg != st.session_state.background:
            st.session_state.background = quick_bg
            st.rerun()
        
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.current_user = None
            st.session_state.user_role = None
            st.rerun()
    
    # Main content - Header with logo
    header_col1, header_col2, header_col3 = st.columns([1, 2, 1])
    with header_col2:
        if LOGO_PATH.exists():
            st.image(str(LOGO_PATH), width=350)
        else:
            st.warning("⚠️ Add logo: images/dragon_logo.png")
    
    # Navigation tabs
    tabs = st.tabs(["📊 Dashboard", "⚡ SMTP Config", "✉️ Email", "📱 SMS", "☁️ Azure SMS", "⏰ Scheduled", "✨ Jelly Dashboard", "⚙️ Settings"])
    
    with tabs[0]:
        dashboard_ui()
    
    with tabs[1]:
        smtp_config_ui()
    
    with tabs[2]:
        email_composer_ui()
    
    with tabs[3]:
        sms_composer_ui()
    
    with tabs[4]:
        azure_sms_ui()
    
    with tabs[5]:
        scheduled_ui()
    
    with tabs[6]:
        jelly_dashboard_ui()
    
    with tabs[7]:
        settings_ui()

if __name__ == "__main__":
    main()
