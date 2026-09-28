# Google Workspace Exporter UI Setup Guide

## Quick Start

### 1. Install Dependencies
```bash
pip3 install flask
```

### 2. Start the Server
```bash
cd /Users/anuj/workspace-classifier
python3 server.py
```

You'll see:
```
🚀 GWS Exporter Server starting...
📊 Open http://localhost:5000 in your browser
```

### 3. Open the UI
Open your browser and go to: **http://localhost:5000**

---

## How to Use the UI

### Step 1: Upload Service Account JSON
- Click **"Upload service_account.json"** area
- Select your Google service account JSON key file
- You should see: ✓ `service_account.json`

### Step 2: Enter Admin Email
- Type your Google Workspace admin email (e.g., `admin@company.com`)

### Step 3: Add Employee Emails
- Type an employee email in the input field
- Click **"+ Add"** (or press Enter)
- Repeat for each employee you want to extract
- You can remove any email with the **"Remove"** button

### Step 4: (Optional) Set Date Range
- **From**: Start date (e.g., 2024-01-01)
- **To**: End date (e.g., 2024-03-31)
- Leave empty to extract all data

### Step 5: Start Extraction
- Click **🚀 START EXTRACTION**
- Watch the progress bar as data downloads
- See real-time status updates
- When done, you'll see the completion message

---

## What Happens

The UI will:
1. Upload your service account JSON securely
2. Run the extraction command in the background
3. Track progress and show:
   - Overall percentage (0-100%)
   - Current employee being processed
   - Estimated time remaining
4. Save data to: `/Users/anuj/workspace-classifier/out/`
5. Create a zip archive when complete

---

## Important Notes

- **Keep the terminal running** while the UI is open
- The extraction may take **several hours** for large organizations
- Your data stays **on your computer** - nothing is sent elsewhere
- The service account JSON is **safe** and only used locally
- You can **close the browser** if needed; the extraction continues in the background

---

## Troubleshooting

### "Connection refused"
- Make sure the server is running (`python3 server.py`)
- Check if port 5000 is available

### "Invalid JSON file"
- Make sure you uploaded the correct `service_account.json` from Google Cloud
- The file should start with `{"type": "service_account"...`

### "Extraction failed"
- Check that admin email is correct and a super administrator
- Verify employee emails are spelled correctly
- Ensure the service account is authorized in Google Admin Console

### "No output in progress bar"
- This can happen on first run while dependencies load
- Give it 30-60 seconds to start

---

## For Developers

The UI is built with:
- **Frontend**: HTML5, CSS3, JavaScript (no frameworks)
- **Backend**: Python Flask
- **Communication**: REST API (fetch)

To modify, edit:
- `gws-exporter-ui.html` - Change the UI design/layout
- `server.py` - Change extraction logic/API endpoints

---

## What Gets Extracted

For each employee:
- **Google Drive**: All files (original folder structure preserved)
- **Gmail**: All messages in date range (with attachments)
- **Output format**:
  - `emails_all.json` - Complete email data
  - `emails_metadata.csv` - Email summary (Excel-friendly)
  - `email_XXXXX.txt` - Individual email files
  - `attachments/` - Downloaded attachments
  - `files/` - Drive files organized by folder

---

## Security

✅ Service account JSON uploaded to local `/tmp` only
✅ No data sent to external servers
✅ Read-only access (nothing deleted from Google Workspace)
✅ HTTPS not required (runs locally on `localhost:5000`)
✅ All credentials stay on your machine

---

## Need Help?

If the server won't start, try:
```bash
# Kill any existing process on port 5000
lsof -ti:5000 | xargs kill -9

# Then start again
python3 server.py
```

Or check the terminal output for error messages.
