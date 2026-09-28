# GWS Exporter - Self-Hosted Server Setup Guide

## System Requirements

- **OS**: Linux (Ubuntu 20.04+, Debian 10+) or macOS
- **Python**: 3.10 or newer
- **Storage**: 100GB+ (for extracted data)
- **RAM**: 4GB minimum
- **Network**: Static IP or domain name
- **Web Server**: Nginx (recommended) or Apache

---

## Installation Steps

### 1. Prepare Server

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3 python3-pip python3-venv nginx git curl
```

### 2. Clone Repository

```bash
cd /opt
sudo git clone https://github.com/anujchahar-lh2/gws-workspace-exporter.git
cd gws-workspace-exporter
```

### 3. Create Python Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Create App User (Security)

```bash
sudo useradd -r -s /bin/bash gws-app
sudo chown -R gws-app:gws-app /opt/gws-workspace-exporter
sudo chmod -R 755 /opt/gws-workspace-exporter
```

### 5. Create Upload Directory

```bash
sudo mkdir -p /var/gws-uploads
sudo chown gws-app:gws-app /var/gws-uploads
sudo chmod 750 /var/gws-uploads
```

### 6. Create Systemd Service

Create `/etc/systemd/system/gws-exporter.service`:

```ini
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
```

Enable service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable gws-exporter
sudo systemctl start gws-exporter
```

Check status:
```bash
sudo systemctl status gws-exporter
```

---

## Web Server Configuration

### Option A: Nginx (Recommended)

1. **Copy configuration**:
```bash
sudo cp nginx.conf /etc/nginx/sites-available/gws-exporter
sudo ln -s /etc/nginx/sites-available/gws-exporter /etc/nginx/sites-enabled/
```

2. **Edit configuration**:
```bash
sudo nano /etc/nginx/sites-available/gws-exporter
# Replace "your-domain.com" with your actual domain
```

3. **Test and reload**:
```bash
sudo nginx -t
sudo systemctl restart nginx
```

### Option B: Apache

1. **Enable proxy modules**:
```bash
sudo a2enmod proxy proxy_http proxy_wstunnel headers ssl
```

2. **Copy configuration**:
```bash
sudo cp apache.conf /etc/apache2/sites-available/gws-exporter.conf
sudo a2ensite gws-exporter
```

3. **Edit configuration**:
```bash
sudo nano /etc/apache2/sites-available/gws-exporter.conf
# Replace "your-domain.com" with your actual domain
```

4. **Restart Apache**:
```bash
sudo apache2ctl configtest
sudo systemctl restart apache2
```

---

## SSL/HTTPS Setup (Recommended)

### Using Let's Encrypt (Free)

```bash
sudo apt install -y certbot python3-certbot-nginx  # For Nginx
# OR
sudo apt install -y certbot python3-certbot-apache  # For Apache

# Generate certificate
sudo certbot certonly --standalone -d your-domain.com

# Auto-renew
sudo systemctl enable certbot.timer
```

Then update Nginx/Apache config with certificate paths.

---

## Environment Configuration

Create `/opt/gws-workspace-exporter/.env`:

```
UPLOAD_FOLDER=/var/gws-uploads
FLASK_ENV=production
FLASK_DEBUG=False
MAX_UPLOAD_SIZE=104857600
```

---

## Monitoring and Logs

### Check service status:
```bash
sudo systemctl status gws-exporter
```

### View logs:
```bash
# Service logs
sudo journalctl -u gws-exporter -f

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Apache logs (if using Apache)
sudo tail -f /var/log/apache2/gws-exporter-access.log
sudo tail -f /var/log/apache2/gws-exporter-error.log
```

### Monitor performance:
```bash
# CPU and Memory
top -p $(pgrep -f gunicorn | head -1)

# Disk usage
df -h /var/gws-uploads
du -sh /opt/gws-workspace-exporter/out/*
```

---

## Backup Strategy

### Backup extracted data:
```bash
#!/bin/bash
# Save as /opt/backup-gws.sh

BACKUP_DIR="/backups/gws-exporter"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR
tar -czf $BACKUP_DIR/gws-data-$DATE.tar.gz /opt/gws-workspace-exporter/out/

# Keep only last 7 days
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
```

Run daily:
```bash
sudo crontab -e
# Add: 0 2 * * * /opt/backup-gws.sh
```

---

## Security Checklist

- [ ] SSH key authentication enabled (no password login)
- [ ] Firewall configured (only ports 80, 443 open)
- [ ] SSL/HTTPS enabled
- [ ] Regular security updates: `sudo apt update && sudo apt upgrade`
- [ ] Service runs as non-root user
- [ ] Upload directory has proper permissions
- [ ] Logs rotated: `sudo apt install logrotate`
- [ ] Fail2ban enabled: `sudo apt install fail2ban`

---

## Troubleshooting

### Service won't start
```bash
sudo journalctl -u gws-exporter -n 50
# Check Python errors, permissions, ports
```

### Nginx 502 Bad Gateway
```bash
# Check if Flask app is running
curl http://127.0.0.1:8000/health

# Check logs
sudo tail -f /var/log/nginx/error.log
```

### Permission denied on uploads
```bash
sudo chown -R gws-app:gws-app /var/gws-uploads
sudo chmod 750 /var/gws-uploads
```

### Out of disk space
```bash
# Clean old extractions
sudo rm -rf /opt/gws-workspace-exporter/out/old_*

# Check what's using space
du -sh /opt/gws-workspace-exporter/*
du -sh /var/gws-uploads/*
```

---

## Performance Tuning

### Increase Gunicorn workers (in systemd service):
```
ExecStart=/opt/gws-workspace-exporter/venv/bin/gunicorn \
    --workers 8 \        # Increase for more CPU cores
    --worker-class sync \
    --bind 127.0.0.1:8000
```

### Nginx worker processes:
```
user www-data;
worker_processes auto;  # Auto-detect CPU cores
worker_connections 2048;
```

### Increase file descriptor limit:
```bash
sudo nano /etc/security/limits.conf
# Add: * soft nofile 65535
# Add: * hard nofile 65535
```

---

## Deployment Checklist

- [ ] Python 3.10+ installed
- [ ] Virtual environment created
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Service account JSON ready
- [ ] Systemd service created and enabled
- [ ] Web server (Nginx/Apache) configured
- [ ] Domain/IP pointing to server
- [ ] SSL certificate installed
- [ ] Firewall rules configured
- [ ] Backup strategy in place
- [ ] Monitoring setup (optional)
- [ ] Users can access: `https://your-domain.com`

---

## File Structure

```
/opt/gws-workspace-exporter/
├── venv/                          # Python virtual environment
├── server.py                       # Flask app
├── gws-exporter-ui.html           # Web interface
├── run_org_classify.py            # Extraction script
├── requirements.txt               # Python dependencies
├── .env                           # Configuration
└── out/                           # Extracted data

/var/gws-uploads/                 # Temporary uploads
/var/log/nginx/                   # Nginx logs (if using Nginx)
/etc/nginx/sites-available/       # Nginx configs
/etc/systemd/system/              # Systemd service
```

---

## Support & Maintenance

### Weekly tasks:
- [ ] Check disk space: `df -h`
- [ ] Review logs for errors: `journalctl -u gws-exporter`
- [ ] Verify service running: `systemctl status gws-exporter`

### Monthly tasks:
- [ ] Update packages: `apt update && apt upgrade`
- [ ] Backup data: `./backup-gws.sh`
- [ ] Review security logs: `/var/log/auth.log`

### Quarterly tasks:
- [ ] SSL certificate renewal check (auto with certbot)
- [ ] Performance review (check slow queries/requests)
- [ ] Security audit (firewall rules, user permissions)

---

**Once setup is complete, your server URL is ready to share with your team!** 🚀
