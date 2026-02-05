"""
Test Script for Dragon Mailer - Email and SMS Functionality
This script tests the core sending functions without the Streamlit UI
"""

import smtplib
import json
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Configuration paths
CONFIG_DIR = os.path.join(os.path.dirname(__file__), "config")
SMTP_CONFIG_FILE = os.path.join(CONFIG_DIR, "smtp_configs.json")

# SMS Carrier Gateways
SMS_GATEWAYS = {
    "Verizon": "vtext.com",
    "T-Mobile": "tmomail.net",
    "AT&T": "txt.att.net",
    "Sprint": "messaging.sprintpcs.com",
    "Metro PCS": "mymetropcs.com",
    "US Cellular": "email.uscc.net",
    "Boost Mobile": "sms.myboostmobile.com",
    "Cricket": "sms.cricketwireless.net",
    "Virgin Mobile": "vmobl.com",
}

def load_json(filepath, default=None):
    """Load JSON file"""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except:
        return default or {}

def get_smtp_config():
    """Get the first SMTP config"""
    configs = load_json(SMTP_CONFIG_FILE, {"configs": []})
    if configs.get('configs'):
        return configs['configs'][0]
    return None

def test_smtp_connection(smtp_config):
    """Test SMTP connection without sending"""
    print("\n" + "="*60)
    print("📧 TESTING SMTP CONNECTION")
    print("="*60)
    
    try:
        print(f"Server: {smtp_config['server']}:{smtp_config['port']}")
        print(f"Email: {smtp_config['email']}")
        print(f"TLS: {smtp_config.get('use_tls', True)}")
        print("-"*40)
        
        print("Connecting to SMTP server...")
        server = smtplib.SMTP(smtp_config['server'], smtp_config['port'], timeout=30)
        server.ehlo()
        print("✅ Connected!")
        
        if smtp_config.get('use_tls', True):
            print("Starting TLS...")
            server.starttls()
            server.ehlo()
            print("✅ TLS established!")
        
        print("Authenticating...")
        server.login(smtp_config['email'], smtp_config['password'])
        print("✅ Authentication successful!")
        
        server.quit()
        print("\n✅ SMTP CONNECTION TEST PASSED!")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"\n❌ Authentication failed: {e}")
        return False
    except smtplib.SMTPConnectError as e:
        print(f"\n❌ Connection failed: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Error: {type(e).__name__}: {e}")
        return False

def test_send_email(smtp_config, test_email=None):
    """Test sending an actual email"""
    print("\n" + "="*60)
    print("📧 TESTING EMAIL SEND")
    print("="*60)
    
    if not test_email:
        # Send test to self
        test_email = smtp_config['email']
    
    try:
        print(f"Sending test email to: {test_email}")
        
        msg = MIMEMultipart('alternative')
        msg['From'] = smtp_config['email']
        msg['To'] = test_email
        msg['Subject'] = f"Dragon Mailer Test - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        body_text = "This is a test email from Dragon Mailer."
        body_html = """
        <html>
        <body style="font-family: Arial, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background: rgba(255,255,255,0.95); border-radius: 20px; padding: 30px; box-shadow: 0 10px 40px rgba(0,0,0,0.2);">
                <h1 style="color: #667eea; text-align: center;">🐉 Dragon Mailer</h1>
                <h2 style="color: #333; text-align: center;">Test Email Successful!</h2>
                <p style="color: #666; text-align: center; font-size: 16px;">
                    If you're seeing this email, your SMTP configuration is working correctly!
                </p>
                <div style="background: linear-gradient(90deg, #667eea, #764ba2); height: 3px; margin: 20px 0;"></div>
                <p style="color: #999; text-align: center; font-size: 12px;">
                    Sent at: {timestamp}
                </p>
            </div>
        </body>
        </html>
        """.format(timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        msg.attach(MIMEText(body_text, 'plain'))
        msg.attach(MIMEText(body_html, 'html'))
        
        server = smtplib.SMTP(smtp_config['server'], smtp_config['port'], timeout=30)
        server.ehlo()
        
        if smtp_config.get('use_tls', True):
            server.starttls()
            server.ehlo()
        
        server.login(smtp_config['email'], smtp_config['password'])
        server.sendmail(smtp_config['email'], test_email, msg.as_string())
        server.quit()
        
        print(f"✅ EMAIL SENT SUCCESSFULLY to {test_email}!")
        return True
        
    except Exception as e:
        print(f"❌ EMAIL SEND FAILED: {type(e).__name__}: {e}")
        return False

def test_send_sms(smtp_config, phone_number, carrier="Verizon"):
    """Test sending SMS via carrier gateway"""
    print("\n" + "="*60)
    print("📱 TESTING SMS SEND (via Email Gateway)")
    print("="*60)
    
    try:
        gateway = SMS_GATEWAYS.get(carrier)
        if not gateway:
            print(f"❌ Unknown carrier: {carrier}")
            print(f"Available carriers: {', '.join(SMS_GATEWAYS.keys())}")
            return False
        
        # Clean phone number
        phone = ''.join(filter(str.isdigit, phone_number))
        if len(phone) == 11 and phone.startswith('1'):
            phone = phone[1:]
        
        if len(phone) != 10:
            print(f"❌ Phone number must be 10 digits, got: {phone}")
            return False
        
        sms_email = f"{phone}@{gateway}"
        print(f"Phone: {phone_number}")
        print(f"Carrier: {carrier}")
        print(f"Gateway: {gateway}")
        print(f"SMS Email: {sms_email}")
        print("-"*40)
        
        # Create SMS message
        message = f"🐉 Dragon Mailer Test SMS - {datetime.now().strftime('%H:%M:%S')}"
        
        msg = MIMEText(message)
        msg['From'] = smtp_config['email']
        msg['To'] = sms_email
        msg['Subject'] = ""  # SMS doesn't need subject
        
        server = smtplib.SMTP(smtp_config['server'], smtp_config['port'], timeout=30)
        server.ehlo()
        
        if smtp_config.get('use_tls', True):
            server.starttls()
            server.ehlo()
        
        server.login(smtp_config['email'], smtp_config['password'])
        server.sendmail(smtp_config['email'], sms_email, msg.as_string())
        server.quit()
        
        print(f"✅ SMS SENT SUCCESSFULLY!")
        print(f"   Message should arrive at {phone_number}")
        return True
        
    except Exception as e:
        print(f"❌ SMS SEND FAILED: {type(e).__name__}: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("🐉 DRAGON MAILER - FUNCTIONALITY TEST")
    print("="*60)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Load SMTP config
    smtp_config = get_smtp_config()
    if not smtp_config:
        print("\n❌ NO SMTP CONFIGURATION FOUND!")
        print("Please add an SMTP config in the app first.")
        return False
    
    print(f"\nUsing SMTP Config: {smtp_config['name']}")
    
    results = {
        "smtp_connection": False,
        "email_send": False,
        "sms_ready": True  # SMS just requires SMTP to work
    }
    
    # Test 1: SMTP Connection
    results["smtp_connection"] = test_smtp_connection(smtp_config)
    
    # Test 2: Send Email (if connection works)
    if results["smtp_connection"]:
        results["email_send"] = test_send_email(smtp_config)
    else:
        print("\n⚠️ Skipping email send test due to connection failure")
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    print(f"SMTP Connection: {'✅ PASS' if results['smtp_connection'] else '❌ FAIL'}")
    print(f"Email Send:      {'✅ PASS' if results['email_send'] else '❌ FAIL'}")
    print(f"SMS Ready:       {'✅ READY' if results['sms_ready'] and results['smtp_connection'] else '❌ NOT READY'}")
    
    if all([results['smtp_connection'], results['email_send']]):
        print("\n🎉 ALL TESTS PASSED! Dragon Mailer is working correctly!")
    else:
        print("\n⚠️ Some tests failed. Check the errors above.")
    
    return results

if __name__ == "__main__":
    run_all_tests()
