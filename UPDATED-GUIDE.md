# Google Workspace Data Extraction - Updated Guide

**Version:** 2.0 with Web UI  
**Date:** 2026-09-28  
**Status:** Ready to use - Web UI + Terminal CLI + Self-Hosted options

---

## What's New

✨ **NEW:** Complete web-based UI (no terminal needed!)
✨ **NEW:** `--modified-before` flag for closed date-range extraction
✨ **NEW:** Self-hosted deployment option
✨ **IMPROVED:** Better error handling and retry logic
✨ **IMPROVED:** Fast-fail for permanent errors (no wasted retries)

---

## Three Ways to Use This Tool

### Option 1: Web UI (Recommended for Most Users) 🎨
**Best for:** Non-technical users, visual progress tracking

```bash
pip3 install -r requirements.txt
python3 server.py
# Open: http://localhost:5000
```

Upload JSON → Add emails → Set dates → Click START → Done!

### Option 2: Command Line (For Power Users) 💻
**Best for:** Advanced users, automation, scripts

```bash
python3 run_org_classify.py \
  --admin admin@company.com \
  --only alice@company.com \
  --only bob@company.com \
  --export-only --local-only \
  --modified-after 2024-01-01 \
  --modified-before 2024-03-31
```

### Option 3: Self-Hosted Server (For Teams) 🖥️
**Best for:** Organizations, sharing across team

Deploy on your own server:
```bash
sudo ./deploy.sh
# Access at: https://your-domain.com
```

---

## Quick Start - Web UI

### Installation (5 minutes)

1. **Check Python:**
```bash
python3 --version  # Should be 3.10+
```

2. **Install Dependencies:**
```bash
cd gws-workspace-exporter  # or your project directory
pip3 install -r requirements.txt
```

3. **Start Server:**
```bash
python3 server.py
```

4. **Open Browser:**
```
http://localhost:5000
```

### Using the UI

**Step 1:** Upload `service_account.json`
- Click the upload area
- Select your Google service account key

**Step 2:** Enter Admin Email
- Type: `admin@company.com`

**Step 3:** Add Employee Emails
- Type: `alice@company.com`
- Click: + Add
- Repeat for each employee

**Step 4:** Set Date Range (Optional)
- From: `2024-01-01`
- To: `2024-03-31`
- Or leave empty for all data

**Step 5:** Click START
- Watch progress bar
- See real-time logs in terminal

---

## What Gets Extracted

For each employee:

📁 **Google Drive**
- All files (original folder structure preserved)
- Organized exactly as in Google Drive

📧 **Gmail**
- All emails in date range
- Complete metadata (sender, subject, date, etc.)
- All attachments downloaded
- CSV file for easy Excel viewing

---

## File Locations

```
./out/

├── alice_at_company_com/
│   ├── dump/
│   │   ├── files/              (Google Drive files)
│   │   └── emails/             (Gmail data)
│   │       ├── emails_all.json
│   │       ├── emails_metadata.csv  (Open in Excel!)
│   │       ├── email_00001.txt
│   │       └── attachments/
│   └── ...
│
└── org_inventory.csv           (Summary of all data)
```

---

## Advanced: Command Line with Date Range

**Extract multiple employees for April-June 2026:**

```bash
python3 run_org_classify.py \
  --admin suraj@clinikk.com \
  --only chaitrap@clinikk.com \
  --only umeshn@clinikk.com \
  --only santosh@clinikk.com \
  --export-only \
  --local-only \
  --modified-after 2026-04-01 \
  --modified-before 2026-07-01
```

**Key features:**
- `--modified-after`: Start date (inclusive)
- `--modified-before`: End date (exclusive)
- `--only`: Add multiple employees
- `--export-only`: Skip AI classification
- `--local-only`: Keep data on your computer

---

## For Self-Hosted Deployment

**One-command server setup:**

```bash
sudo ./deploy.sh
```

This automatically:
- Installs all dependencies
- Configures Nginx web server
- Sets up systemd service
- Enables auto-start on reboot

**Then access at:** `https://your-domain.com`

See `SERVER-SETUP.md` for complete guide.

---

## System Requirements

- **OS:** macOS, Windows, Linux
- **Python:** 3.10 or newer
- **Storage:** 50GB+ (for extracted data)
- **RAM:** 4GB minimum
- **Network:** Stable internet for extraction

---

## Troubleshooting

### "python3: command not found"
Install Python 3.10+ from [python.org](https://python.org)

### "Module not found"
```bash
pip3 install -r requirements.txt
```

### "Port 5000 already in use"
```bash
lsof -i :5000
kill -9 <PID>
python3 server.py
```

### Extraction taking hours
This is normal! Keep the terminal open. Don't close it.

If it stops, just run `python3 server.py` again to resume.

### No progress shown
Give it 30-60 seconds. Initial setup takes time.

---

## Key Improvements in This Version

### ✅ Closed Date Range Support
Now you can extract "April 1 to June 30, 2026" (not just "since April 1")

**Old:** `--modified-after 2026-04-01` (everything from April onward)  
**New:** `--modified-after 2026-04-01 --modified-before 2026-07-01` (April-June only)

### ✅ Better Error Handling
- Retries network timeouts automatically
- Fast-fails on permanent errors (no wasted time)
- Partial results preserved even if extraction stops
- Clear error messages in logs

### ✅ Web UI (No Terminal Required)
- Drag-drop file upload
- Email management
- Date range picker
- Real-time progress tracking
- Completion notifications

### ✅ Production Ready
- Can self-host on your server
- Systemd service management
- Nginx configuration included
- SSL/HTTPS support
- Log rotation and backups

---

## Documentation Files

| File | Purpose |
|------|---------|
| `QUICKSTART.md` | 2-minute quick start |
| `LOCAL-SETUP.md` | Complete localhost guide |
| `SERVER-SETUP.md` | Self-hosted deployment |
| `DEPLOYMENT-CHECKLIST.md` | Production checklist |
| `UI-SETUP.md` | Local testing guide |

---

## Data Security & Privacy

✅ **All data stays on your computer**  
✅ **Read-only access** (nothing deleted or modified)  
✅ **No uploads** to external services  
✅ **Service account JSON** only used locally  
✅ **Network requests** only to Google APIs  

---

## Getting Started

### Quickest Start (Web UI):
```bash
pip3 install -r requirements.txt
python3 server.py
# Open: http://localhost:5000
```

### More Details:
See `LOCAL-SETUP.md` or `QUICKSTART.md`

### Self-Hosted Server:
See `SERVER-SETUP.md`

---

## Support

- Check `LOCAL-SETUP.md` for detailed troubleshooting
- Review terminal logs for error details
- See `DEPLOYMENT-CHECKLIST.md` for production setup

---

**Questions?** All documentation is in the repository. Start with `QUICKSTART.md` or `LOCAL-SETUP.md`.

**Ready?** Run `python3 server.py` and visit `http://localhost:5000` 🚀
