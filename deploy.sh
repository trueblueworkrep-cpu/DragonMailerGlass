#!/bin/bash
#============================================================
# Dragon Mailer - Auto Deploy Script
# Domain: dragon-mailer.com
# Server: 66.113.136.229
#============================================================

set -e

echo "============================================"
echo "   Dragon Mailer - Auto Deployment"
echo "============================================"
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root (sudo ./deploy.sh)"
    exit 1
fi

# Variables
DOMAIN="dragon-mailer.com"
APP_DIR="/var/www/dragonmailer"
REPO_URL="https://github.com/trueblueworkrep-cpu/DragonMailerGlass.git"

echo "[1/8] Updating system packages..."
apt update && apt upgrade -y

echo "[2/8] Installing dependencies..."
apt install -y python3 python3-pip python3-venv nginx git certbot python3-certbot-nginx

echo "[3/8] Creating application directory..."
mkdir -p $APP_DIR
cd $APP_DIR

echo "[4/8] Cloning repository..."
if [ -d ".git" ]; then
    git pull
else
    git clone $REPO_URL .
fi

echo "[5/8] Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
deactivate

echo "[6/8] Setting permissions..."
chown -R www-data:www-data $APP_DIR
chmod -R 755 $APP_DIR

echo "[7/8] Installing systemd service..."
cp dragonmailer.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable dragonmailer
systemctl start dragonmailer

echo "[8/8] Configuring nginx..."
cp nginx_dragon_mailer.conf /etc/nginx/sites-available/dragon-mailer.conf
ln -sf /etc/nginx/sites-available/dragon-mailer.conf /etc/nginx/sites-enabled/
nginx -t && systemctl reload nginx

echo ""
echo "============================================"
echo "   Deployment Complete!"
echo "============================================"
echo ""
echo "Your app should now be running at:"
echo "  http://$DOMAIN"
echo ""
echo "To add SSL certificate, run:"
echo "  sudo certbot --nginx -d $DOMAIN -d www.$DOMAIN"
echo ""
echo "Check app status:"
echo "  sudo systemctl status dragonmailer"
echo ""
echo "View logs:"
echo "  sudo journalctl -u dragonmailer -f"
echo ""
