# 🚀 DRAGON MAILER - LIVE DEPLOYMENT GUIDE
# Server: 62.72.3.154
# Domain: dragon-mailer.com (Already pointing to IP ✅)

## ⚡ SUPER QUICK START (Copy & Paste These Commands)

### STEP 1: SSH into your server
```bash
ssh root@62.72.3.154
```

### STEP 2: Update system and install dependencies (Copy all at once)
```bash
apt update && apt upgrade -y
apt install -y python3 python3-pip python3-venv nginx git certbot python3-certbot-nginx
```

### STEP 3: Create app directory and navigate to it
```bash
mkdir -p /var/www/dragonmailer
cd /var/www/dragonmailer
```

### STEP 4: Set up Python virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
```

### STEP 5: Upload your files (Use SFTP in a NEW terminal on your LOCAL machine)
```bash
# On your LOCAL machine (not SSH):
sftp root@62.72.3.154

# Inside SFTP:
cd /var/www/dragonmailer
put -r * 
exit
```

### STEP 6: Back on SSH - Install Python dependencies
```bash
cd /var/www/dragonmailer
source venv/bin/activate
pip install -r requirements.txt
```

### STEP 7: Set proper permissions
```bash
chown -R www-data:www-data /var/www/dragonmailer
chmod -R 755 /var/www/dragonmailer
```

### STEP 8: Install Nginx configuration (Copy files if not uploaded)
```bash
# If dragonmailer.service exists:
cp /var/www/dragonmailer/dragonmailer.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable dragonmailer

# If nginx_dragon_mailer.conf exists:
cp /var/www/dragonmailer/nginx_dragon_mailer.conf /etc/nginx/sites-available/dragon-mailer.conf
rm -f /etc/nginx/sites-enabled/default
ln -sf /etc/nginx/sites-available/dragon-mailer.conf /etc/nginx/sites-enabled/dragon-mailer.conf

# Test and reload
nginx -t
systemctl reload nginx
```

### STEP 9: Allow firewall ports
```bash
ufw allow 'Nginx Full'
ufw allow 22/tcp
ufw enable
```

### STEP 10: Install SSL Certificate (IMPORTANT - HTTPS)
```bash
certbot --nginx -d dragon-mailer.com -d www.dragon-mailer.com
```

### STEP 11: Start your application
```bash
systemctl start dragonmailer
systemctl status dragonmailer
```

---

## ✅ YOU'RE LIVE!

Your app should now be accessible at:
- 🌐 **https://dragon-mailer.com**
- 🌐 **https://www.dragon-mailer.com**

---

## 📊 Useful Commands After Deployment

### View application logs
```bash
sudo journalctl -u dragonmailer -f
```

### Restart the app
```bash
sudo systemctl restart dragonmailer
```

### Check service status
```bash
sudo systemctl status dragonmailer
```

### Restart Nginx
```bash
sudo systemctl restart nginx
```

### Test Nginx configuration
```bash
sudo nginx -t
```

### Renew SSL certificate (before expiry)
```bash
sudo certbot renew
```

### Update app (pull latest code)
```bash
cd /var/www/dragonmailer
sudo git pull
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart dragonmailer
```

---

## 🔧 Troubleshooting

### App won't start?
```bash
sudo journalctl -u dragonmailer -f
# Check the error message
```

### Can't reach website?
```bash
# Check DNS:
nslookup dragon-mailer.com

# Check if Nginx is running:
sudo systemctl status nginx

# Check ports:
sudo ss -tuln | grep -E '80|443'

# Reload Nginx:
sudo systemctl reload nginx
```

### SSL certificate issues?
```bash
# Renew certificate:
sudo certbot renew --nginx

# Test renewal:
sudo certbot renew --dry-run
```

### Permission denied errors?
```bash
sudo chown -R www-data:www-data /var/www/dragonmailer
sudo chmod -R 755 /var/www/dragonmailer
sudo systemctl restart dragonmailer
```

---

## 📝 File Upload via SFTP (Windows Users)

If you prefer GUI:
1. Download **FileZilla** or **WinSCP**
2. Connect to `62.72.3.154` as root
3. Navigate to `/var/www/dragonmailer`
4. Drag & drop all files from `DragonMailerGlass` folder
5. Wait for upload to complete

---

## 🎯 Final Checklist

- [ ] SSH access works (ssh root@62.72.3.154)
- [ ] Files uploaded to `/var/www/dragonmailer`
- [ ] Virtual environment created and activated
- [ ] Python dependencies installed (pip install -r requirements.txt)
- [ ] Nginx configured
- [ ] SSL certificate installed
- [ ] Service enabled and started
- [ ] Can access https://dragon-mailer.com
- [ ] Dashboard loads correctly

---

## 🆘 Need Help?

If anything breaks:
1. Check logs: `sudo journalctl -u dragonmailer -f`
2. Check Nginx logs: `sudo tail -f /var/log/nginx/error.log`
3. Verify permissions: `ls -la /var/www/dragonmailer`
4. Test config: `sudo nginx -t`

---

**🎉 Your Dragon Mailer is now LIVE on dragon-mailer.com!**
