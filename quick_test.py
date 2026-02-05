"""Quick test - send email to external Gmail"""
import smtplib
import json
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Load config - use absolute path
script_dir = os.path.dirname(os.path.abspath(__file__))
config_file = os.path.join(script_dir, 'config', 'smtp_configs.json')
print(f"Loading config from: {config_file}")

with open(config_file) as f:
    data = json.load(f)
    config = data.get('configs', [{}])[0]
    print(f"Using SMTP: {config.get('name', 'Unknown')}")

# Create email
msg = MIMEMultipart('alternative')
msg['From'] = config['email']
msg['To'] = 'jeffcarter504@gmail.com'
msg['Subject'] = f'Dragon Mailer Test - {datetime.now().strftime("%H:%M:%S")}'

html = """
<html>
<body style="font-family: Arial, sans-serif; background: linear-gradient(135deg, #0ea5e9 0%, #22c55e 100%); padding: 20px;">
    <div style="max-width: 600px; margin: 0 auto; background: white; border-radius: 20px; padding: 30px; box-shadow: 0 10px 40px rgba(0,0,0,0.2);">
        <h1 style="color: #0ea5e9; text-align: center;">🐉 Dragon Mailer</h1>
        <h2 style="color: #22c55e; text-align: center;">Email Test Successful!</h2>
        <p style="color: #333; text-align: center; font-size: 16px;">
            Your SMTP configuration is working perfectly!<br>
            You can now send emails from Dragon Mailer.
        </p>
        <div style="background: linear-gradient(90deg, #0ea5e9, #22c55e); height: 4px; margin: 20px 0; border-radius: 2px;"></div>
        <p style="color: #999; text-align: center; font-size: 12px;">
            Sent via Dragon Mailer Glass Edition<br>
            """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """
        </p>
    </div>
</body>
</html>
"""

msg.attach(MIMEText(html, 'html'))

# Send
print("Sending email to jeffcarter504@gmail.com...")
server = smtplib.SMTP(config['server'], config['port'], timeout=30)
server.ehlo()
server.starttls()
server.ehlo()
server.login(config['email'], config['password'])
server.sendmail(config['email'], 'jeffcarter504@gmail.com', msg.as_string())
server.quit()
print("✅ Email sent successfully to jeffcarter504@gmail.com!")
print("Check your Gmail inbox (and spam folder).")
