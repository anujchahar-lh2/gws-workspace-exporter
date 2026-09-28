# GWS Exporter - Self-Hosted Deployment Checklist

## Files Included ✅

All files are in `/Users/anuj/workspace-classifier/`:

### Core Application
- ✅ `server.py` - Flask backend server
- ✅ `gws-exporter-ui.html` - Web interface (UI)
- ✅ `run_org_classify.py` - Extraction script (from repo)
- ✅ `gmail/` - Gmail module (from repo)
- ✅ `dump/` - Drive download module (from repo)

### Configuration Files
- ✅ `requirements.txt` - Python dependencies
- ✅ `nginx.conf` - Nginx web server config
- ✅ `apache.conf` - Apache web server config (alternative)

### Deployment Files
- ✅ `deploy.sh` - Automated deployment script
- ✅ `SERVER-SETUP.md` - Complete setup guide
- ✅ `DEPLOYMENT-CHECKLIST.md` - This file
- ✅ `UI-SETUP.md` - Local UI setup guide

---

## Quick Deployment (3 Steps)

### Step 1: Copy to Your Server
```bash
scp -r /Users/anuj/workspace-classifier/* user@your-server:/opt/gws-workspace-exporter/
```

### Step 2: Run Deployment Script (on server)
```bash
ssh user@your-server
sudo chmod +x /opt/gws-workspace-exporter/deploy.sh
sudo /opt/gws-workspace-exporter/deploy.sh
```

### Step 3: Configure Domain & SSL
```bash
# Edit Nginx config
sudo nano /etc/nginx/sites-available/gws-exporter
# Replace "your-domain.com" with your actual domain

# Get SSL certificate (free)
sudo certbot certonly --standalone -d your-domain.com

# Update Nginx config with certificate paths and restart
sudo systemctl restart nginx
```

**Done!** Your server is live at: `https://your-domain.com` 🎉

---

## What Each File Does

| File | Purpose | Notes |
|------|---------|-------|
| `server.py` | Flask web server | Main backend application |
| `gws-exporter-ui.html` | Web interface | Frontend for users |
| `requirements.txt` | Dependencies | All Python packages needed |
| `nginx.conf` | Web server config | Reverse proxy setup |
| `deploy.sh` | Automation | Installs everything automatically |
| `SERVER-SETUP.md` | Documentation | Detailed setup instructions |

---

## System Requirements

```
OS:        Linux (Ubuntu 20.04+) or macOS
Python:    3.10+
Storage:   100GB+ (for extracted data)
RAM:       4GB minimum
CPU:       2+ cores
Network:   Static IP or domain
Ports:     80, 443 (HTTP, HTTPS)
```

---

## Installation Options

### Option A: Automatic (Recommended)
```bash
sudo /opt/gws-workspace-exporter/deploy.sh
```
✅ Fastest  
✅ Everything configured automatically  
✅ Service runs on systemd

### Option B: Manual
Follow detailed instructions in `SERVER-SETUP.md`

✅ More control  
✅ Better for learning  
⏱️ Takes ~30 minutes

---

## Customization Guide

### Change default port:
Edit `server.py`:
```python
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)  # Change 5000 here
```

### Increase upload size:
Edit `server.py`:
```python
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # Change size here
```

### Change upload directory:
Edit `server.py`:
```python
app.config['UPLOAD_FOLDER'] = '/your/custom/path'
```

### Modify UI design:
Edit `gws-exporter-ui.html` directly (HTML/CSS/JavaScript)

### Change extraction options:
Edit `server.py` function `run_extraction()` to add CLI flags

---

## Security Best Practices

### Before Going Live:
1. ✅ Enable SSL/HTTPS with Let's Encrypt (free)
2. ✅ Configure firewall (only 80, 443 open)
3. ✅ Use SSH keys, disable password login
4. ✅ Run as non-root user (`gws-app`)
5. ✅ Set proper file permissions
6. ✅ Enable log rotation
7. ✅ Setup fail2ban (brute-force protection)
8. ✅ Regular backups (see `SERVER-SETUP.md`)

### SSL Certificate (Free with Let's Encrypt):
```bash
sudo apt install certbot
sudo certbot certonly --standalone -d your-domain.com
# Auto-renews automatically
```

---

## Monitoring & Maintenance

### Check service status:
```bash
sudo systemctl status gws-exporter
```

### View logs in real-time:
```bash
sudo journalctl -u gws-exporter -f
```

### View Nginx errors:
```bash
sudo tail -f /var/log/nginx/error.log
```

### Monitor disk space:
```bash
df -h /var/gws-uploads
```

### Restart service:
```bash
sudo systemctl restart gws-exporter
```

---

## Backup Strategy

Run daily backup:
```bash
#!/bin/bash
tar -czf /backups/gws-data-$(date +%Y%m%d).tar.gz \
    /opt/gws-workspace-exporter/out/
```

See `SERVER-SETUP.md` for automated backup setup.

---

## Performance Tuning

### Increase workers (in `/etc/systemd/system/gws-exporter.service`):
```
ExecStart=/opt/gws-workspace-exporter/venv/bin/gunicorn \
    --workers 8 \        # Increase based on CPU cores
    --worker-class sync \
    --bind 127.0.0.1:8000
```

Then restart:
```bash
sudo systemctl restart gws-exporter
```

---

## Troubleshooting

### Service won't start
```bash
sudo journalctl -u gws-exporter -n 50  # Show last 50 lines
```

### 502 Bad Gateway error
```bash
# Check if Flask is running
curl http://127.0.0.1:8000/health

# Check Nginx logs
sudo tail -f /var/log/nginx/error.log
```

### Permission denied errors
```bash
sudo chown -R gws-app:gws-app /opt/gws-workspace-exporter
sudo chown -R gws-app:gws-app /var/gws-uploads
sudo chmod 750 /var/gws-uploads
```

### Out of disk space
```bash
# Check usage
du -sh /opt/gws-workspace-exporter/*
du -sh /var/gws-uploads/*

# Clean old extractions
sudo rm -rf /opt/gws-workspace-exporter/out/old_*
```

---

## Production Checklist

Before sharing with your team:

- [ ] Domain registered and pointing to server
- [ ] SSL certificate installed
- [ ] Firewall configured (80, 443 open; others closed)
- [ ] Service running: `sudo systemctl status gws-exporter`
- [ ] Health check passing: `curl https://your-domain.com/health`
- [ ] UI loads: `https://your-domain.com`
- [ ] Test extraction works with sample data
- [ ] Backups configured and tested
- [ ] Monitoring/logs accessible
- [ ] Documentation shared with team
- [ ] Support contact information provided

---

## Next Steps

1. **Prepare your server** (Ubuntu 20.04+ recommended)
2. **Copy files** to `/opt/gws-workspace-exporter/`
3. **Run deploy script**: `sudo ./deploy.sh`
4. **Configure domain** in Nginx config
5. **Get SSL certificate**: `sudo certbot certonly --standalone -d your-domain.com`
6. **Test**: Visit `https://your-domain.com`
7. **Share URL** with your team!

---

## Support Resources

- **Full setup guide**: `SERVER-SETUP.md`
- **Local testing**: `UI-SETUP.md`
- **GitHub repo**: https://github.com/anujchahar-lh2/gws-workspace-exporter
- **Logs location**: `/var/log/nginx/` or `journalctl -u gws-exporter`

---

## Cost Estimate

- **Domain**: $10-15/year
- **SSL Certificate**: FREE (Let's Encrypt)
- **Server**: $5-50/month depending on provider
- **Backup Storage**: $0-10/month

**Total: ~$5-20/month** for a small to medium team

---

**Questions?** Check `SERVER-SETUP.md` for detailed troubleshooting or review the deployment logs:
```bash
sudo journalctl -u gws-exporter
```

**Ready to deploy?** Run the deploy script and you're done! 🚀
