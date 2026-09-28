#!/bin/bash
# Quick deployment script for GWS Exporter

set -e

echo "🚀 GWS Exporter Deployment Script"
echo "=================================="

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   echo "❌ This script must be run as root (use sudo)"
   exit 1
fi

# Variables
APP_DIR="/opt/gws-workspace-exporter"
APP_USER="gws-app"
UPLOAD_DIR="/var/gws-uploads"

echo "📦 Step 1: Installing system dependencies..."
apt update
apt install -y python3 python3-pip python3-venv git nginx curl

echo "📂 Step 2: Creating directories..."
mkdir -p $APP_DIR
mkdir -p $UPLOAD_DIR

echo "👤 Step 3: Creating app user..."
useradd -r -s /bin/bash $APP_USER || true

echo "🔐 Step 4: Setting permissions..."
chown -R $APP_USER:$APP_USER $APP_DIR
chown -R $APP_USER:$APP_USER $UPLOAD_DIR
chmod 750 $UPLOAD_DIR

echo "🐍 Step 5: Setting up Python environment..."
cd $APP_DIR
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "⚙️ Step 6: Creating systemd service..."
cat > /etc/systemd/system/gws-exporter.service << 'EOF'
[Unit]
Description=Google Workspace Exporter
After=network.target

[Service]
Type=notify
User=gws-app
WorkingDirectory=/opt/gws-workspace-exporter
Environment="PATH=/opt/gws-workspace-exporter/venv/bin"
ExecStart=/opt/gws-workspace-exporter/venv/bin/gunicorn \
    --workers 4 \
    --worker-class sync \
    --bind 127.0.0.1:8000 \
    --timeout 3600 \
    server:app

Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable gws-exporter
systemctl start gws-exporter

echo "🌐 Step 7: Configuring Nginx..."
cp $APP_DIR/nginx.conf /etc/nginx/sites-available/gws-exporter
ln -sf /etc/nginx/sites-available/gws-exporter /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

nginx -t
systemctl restart nginx

echo "✅ Deployment Complete!"
echo ""
echo "📍 Next Steps:"
echo "1. Edit your domain in Nginx config:"
echo "   sudo nano /etc/nginx/sites-available/gws-exporter"
echo ""
echo "2. Setup SSL (free with Let's Encrypt):"
echo "   sudo certbot certonly --standalone -d your-domain.com"
echo ""
echo "3. Test the service:"
echo "   curl http://localhost:8000/health"
echo ""
echo "4. Check logs:"
echo "   sudo journalctl -u gws-exporter -f"
echo ""
echo "5. Share URL with users:"
echo "   https://your-domain.com"
echo ""
echo "For more details, see: SERVER-SETUP.md"
