# GWS Exporter - Local Setup Guide (Localhost)

## Overview

Run the Google Workspace Exporter on your own computer using `localhost:5000`. No server, no deployment needed!

---

## System Requirements

- **OS**: macOS, Windows, or Linux
- **Python**: 3.10 or newer
- **Storage**: 50GB+ (for extracted data)
- **RAM**: 4GB minimum
- **Internet**: Stable connection for extraction

---

## Installation (5 Minutes)

### Step 1: Check Python Version

```bash
python3 --version
```

Should show `Python 3.10.x` or newer. If not, download from [python.org](https://python.org)

### Step 2: Install Dependencies

```bash
cd gws-workspace-exporter  # or your project directory
pip3 install -r requirements.txt
```

Expected output:
```
Successfully installed flask flask-cors google-auth google-api-python-client ...
```

### Step 3: Start the Server

```bash
python3 server.py
```

You'll see:
```
🚀 GWS Exporter Server starting...
📊 Open http://localhost:5000 in your browser
 * Running on http://127.0.0.1:5000
```

### Step 4: Open in Browser

Go to: **http://localhost:5000** 🌐

---

## How to Use (Step by Step)

### 1️⃣ **Upload Service Account JSON**

- Click the **"Upload service_account.json"** area
- Select your Google service account JSON key file
- Should show: **✓ service_account.json**

### 2️⃣ **Enter Admin Email**

- Type your Google Workspace admin email
- Example: `suraj@clinikk.com`

### 3️⃣ **Add Employee Emails**

- Type employee email: `alice@company.com`
- Click **+ Add** (or press Enter)
- Repeat for each employee
- Remove any with the **"Remove"** button

**Example:**
```
alice@company.com
bob@company.com
carol@company.com
```

### 4️⃣ **Set Date Range (Optional)**

- **From**: `2024-01-01` (leave empty for all data)
- **To**: `2024-03-31` (leave empty for all data)

**Examples:**
```
April 1 - June 30, 2026:
  From: 2026-04-01
  To: 2026-07-01

Last 90 days:
  From: [empty] - will extract from 90 days ago
  To: [empty] - will extract until today
```

### 5️⃣ **Start Extraction**

- Click **🚀 START EXTRACTION**
- Watch the progress bar fill up
- See real-time status:
  - Current employee being processed
  - Estimated time remaining
  - Emails/files downloaded

### 6️⃣ **Download Results**

When done, you'll see:
```
✅ Success!
Extracted data for 3 employee(s).
Data location: /out/
Archive: workspace_export.zip
```

---

## Where Is My Data?

All extracted data is saved locally in your project directory:

```
./out/

├── alice_at_company_com/
│   ├── dump/
│   │   ├── files/          (Google Drive files)
│   │   └── emails/         (Gmail data)
│   └── ...
│
├── bob_at_company_com/
│   ├── dump/
│   │   ├── files/
│   │   └── emails/
│   └── ...
│
└── org_inventory.csv       (Summary of all data)
```

---

## Email Data Structure

For each employee, in the `emails/` folder:

```
emails/
├── emails_all.json           (Complete email data)
├── emails_metadata.csv       (Simple spreadsheet - open in Excel)
├── email_00001.txt           (Individual email texts)
├── email_00002.txt
├── ...
└── attachments/              (Downloaded email attachments)
    ├── msg_id_1/
    │   └── document.pdf
    └── msg_id_2/
        └── image.jpg
```

**Open `emails_metadata.csv` in Excel to see:**
- Message ID
- Subject
- Sender
- Date
- Has Attachments (yes/no)
- Email snippet

---

## Drive Data Structure

For each employee, in the `files/` folder:

```
files/
├── original_filename.pdf
├── spreadsheet.xlsx
├── document.docx
├── folder/
│   ├── nested_file.txt
│   └── subfolder/
│       └── deep_file.pptx
└── ...
```

**Folder structure matches Google Drive!**

---

## Common Tasks

### Extract Multiple Times

You can run the extraction multiple times:

```bash
python3 server.py
```

Open `http://localhost:5000` → Repeat steps above

Each run will:
- ✅ Add to the same `/out/` folder
- ✅ Skip already-extracted employees
- ✅ Continue where it left off

### Keep Terminal Running

**Important:** Keep the terminal window open while extracting. Don't close it!

If you close it:
- Extraction stops
- Just run `python3 server.py` again to resume

### Stop Extraction

Press `Ctrl+C` in the terminal to stop

### Change Data Location

Want to save to a different folder? Edit `server.py`:

```python
app.config['UPLOAD_FOLDER'] = '/your/custom/path'
```

Then restart: `python3 server.py`

---

## Troubleshooting

### "Connection refused" or "Cannot connect to localhost:5000"

Make sure server is running:
```bash
python3 server.py
```

You should see:
```
📊 Open http://localhost:5000 in your browser
```

### "Module not found" error

Install dependencies:
```bash
pip3 install -r requirements.txt
```

### Port 5000 already in use

Kill the existing process:

**macOS/Linux:**
```bash
lsof -i :5000
kill -9 <PID>
```

**Windows:**
```bash
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

Then start again:
```bash
python3 server.py
```

### "Invalid JSON file"

Make sure you uploaded the correct `service_account.json`:
- Should start with: `{"type": "service_account"`
- Download fresh from Google Cloud Console
- Don't edit it

### Extraction hangs or stops

This is normal for large extractions. Just wait.

If stuck for 30+ minutes:
- Press `Ctrl+C` to stop
- Run `python3 server.py` again
- It will resume from where it stopped

### No output in progress bar

Give it 30-60 seconds to start. Downloading can take time.

### "Not enough disk space"

Check available space:
```bash
df -h
```

Need at least 50GB free.

---

## Tips & Tricks

### Tip 1: Extract Multiple Batches

Run extraction for some employees, then later for others:

```bash
# Day 1: Extract 5 employees
# Day 2: Extract another 5 employees
# Day 3: Extract the last 5 employees

# All data goes to /out/ - no conflicts
```

### Tip 2: Keep Browser Tab Open

You can close the browser tab and come back later. Just visit `http://localhost:5000` again.

### Tip 3: Check Progress in Terminal

The terminal shows detailed logs:
```
[PROGRESS] 23% - alice@company.com
[PROGRESS] 45% - Processing Gmail...
[PROGRESS] 67% - Downloading Drive files...
```

### Tip 4: Pause Between Extractions

If your computer is slow, wait between extractions:

```bash
# Extraction 1
# Wait 5 minutes
# Extraction 2
```

### Tip 5: Keep Computer Plugged In

Extraction can take hours. Keep your laptop plugged in and **don't let it sleep**:

**macOS:**
```bash
caffeinate -dimsu  # Prevent sleep while running
```

Then run:
```bash
python3 server.py
```

---

## Command Reference

### Start the server:
```bash
python3 server.py
```

### Check if running:
```bash
curl http://localhost:5000/health
```

Should return: `{"status":"ok"}`

### Stop the server:
Press `Ctrl+C` in the terminal

### View logs:
Logs appear automatically in the terminal

### Clear old data:
```bash
rm -rf ./out/*
```

---

## File Locations

| What | Where |
|------|-------|
| UI | http://localhost:5000 |
| Server | `./server.py` |
| Extracted data | `./out/` |
| Logs | Terminal output |
| Config | `.env` (optional) |

---

## Example Workflow

### Scenario: Extract 3 employees for April-June 2026

```
Step 1: Open terminal
  $ cd gws-workspace-exporter
  $ python3 server.py
  
Step 2: Open browser
  http://localhost:5000
  
Step 3: Fill form
  JSON: service_account.json
  Admin: suraj@clinikk.com
  Employees:
    - chaitrap@clinikk.com
    - umeshn@clinikk.com
    - santosh@clinikk.com
  From: 2026-04-01
  To: 2026-07-01
  
Step 4: Click START
  [Watch progress bar]
  
Step 5: Check results
  ./out/
  - chaitrap_at_clinikk_com/
  - umeshn_at_clinikk_com/
  - santosh_at_clinikk_com/
  
Step 6: Review data
  Open emails_metadata.csv in Excel
  Browse files in Finder
```

---

## Security & Privacy

✅ **Safe:**
- All data stays on your computer
- Nothing uploaded to internet
- Service account JSON only used locally
- No external API calls (except Google Drive/Gmail)
- Read-only access (nothing deleted from Google Workspace)

---

## Performance Tips

### Speed up extraction:

1. **Close other apps** - Free up RAM/CPU
2. **Use 2.4GHz WiFi** - Faster than 5GHz for stability
3. **Extract during off-peak hours** - Google API is faster
4. **Extract fewer emails** - Set date range to reduce data
5. **Disable other Chrome tabs** - Less resource competition

### Estimated times (per employee):

| Emails | Drive Files | Time |
|--------|------------|------|
| 1,000 | 100 | 10-15 min |
| 5,000 | 500 | 30-45 min |
| 10,000 | 1,000 | 1-2 hours |
| 50,000 | 5,000 | 5-8 hours |

---

## Getting Help

### Check the terminal output
Most errors are explained in the terminal logs.

### Restart everything
```bash
# Press Ctrl+C to stop
# Run again
python3 server.py
```

### Check logs file
Detailed logs are printed to the terminal.

### Test connection
```bash
curl http://localhost:5000/health
```

---

## What's Next After Extraction?

### Option 1: Review in Excel
```bash
open ./out/emails_metadata.csv
```

### Option 2: Zip everything
```bash
zip -r my-export.zip out/
```

### Option 3: Copy to external drive
```bash
cp -r ./out /Volumes/MyDrive/
```

### Option 4: Share with team
- Give them the extracted files
- Open emails_metadata.csv
- Browse the Drive files

---

## Keep It Running

### Option A: Keep terminal open (Simple)
Just leave the terminal window open.

### Option B: Run in background
```bash
nohup python3 server.py > server.log 2>&1 &
```

Then later:
```bash
tail -f server.log  # View logs
```

---

**You're all set!** Open http://localhost:5000 and start extracting 🚀
