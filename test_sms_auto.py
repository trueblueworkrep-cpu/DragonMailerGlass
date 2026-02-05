"""Test SMS sending with auto-detect carrier"""
import smtplib
import json
import os
import time
from email.mime.text import MIMEText
from datetime import datetime

# Load config
script_dir = os.path.dirname(os.path.abspath(__file__))
config_file = os.path.join(script_dir, 'config', 'smtp_configs.json')
with open(config_file) as f:
    config = json.load(f).get('configs', [{}])[0]

print(f"Using SMTP: {config.get('name')}")
print(f"Email: {config.get('email')}")

# SMS Carrier Gateways
SMS_GATEWAYS = [
    ("Verizon", "vtext.com"),
    ("T-Mobile", "tmomail.net"),
    ("AT&T", "txt.att.net"),
    ("Sprint", "messaging.sprintpcs.com"),
    ("Metro PCS", "mymetropcs.com"),
    ("US Cellular", "email.uscc.net"),
    ("Boost Mobile", "sms.myboostmobile.com"),
    ("Cricket", "sms.cricketwireless.net"),
    ("Virgin Mobile", "vmobl.com"),
]

phone = "8502585770"
message = f"Dragon Mailer Test SMS - {datetime.now().strftime('%H:%M:%S')}"

print(f"\n📱 Testing SMS to: {phone}")
print(f"Message: {message}")
print("="*50)

def send_sms(phone, gateway_domain, carrier_name):
    """Try sending SMS via carrier gateway"""
    try:
        sms_email = f"{phone}@{gateway_domain}"
        print(f"\n🔄 Trying {carrier_name}: {sms_email}")
        
        msg = MIMEText(message)
        msg['From'] = config['email']
        msg['To'] = sms_email
        msg['Subject'] = ""
        
        server = smtplib.SMTP(config['server'], config['port'], timeout=30)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(config['email'], config['password'])
        server.sendmail(config['email'], sms_email, msg.as_string())
        server.quit()
        
        print(f"   ✅ Sent via {carrier_name}!")
        return True
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        return False

# Try all carriers
print("\n🔍 Auto-detecting carrier by trying all gateways...\n")
success_count = 0

for carrier_name, gateway in SMS_GATEWAYS:
    result = send_sms(phone, gateway, carrier_name)
    if result:
        success_count += 1
    time.sleep(1)  # Small delay between attempts

print("\n" + "="*50)
print(f"📊 Results: {success_count}/{len(SMS_GATEWAYS)} carriers accepted the message")
print("\n💡 Note: The SMS will arrive from whichever carrier matches your phone.")
print("   Check your phone for the message!")
