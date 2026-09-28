# GWS Exporter - Quick Start (2 Minutes)

## TL;DR - 3 Commands

```bash
# 1. Install dependencies
pip3 install -r requirements.txt

# 2. Start server
python3 server.py

# 3. Open browser
# Go to: http://localhost:5000
```

---

## That's it!

Then:
1. Upload `service_account.json`
2. Add employee emails
3. (Optional) Set date range
4. Click **🚀 START EXTRACTION**
5. Done!

---

## Troubleshooting

**"Command not found" on `pip3` or `python3`?**
- Install Python 3.10+ from [python.org](https://python.org)

**"Module not found" error?**
- Run: `pip3 install -r requirements.txt`

**"Port already in use"?**
- Run: `lsof -i :5000 | kill -9 <PID>`
- Then run `python3 server.py` again

**Extraction taking forever?**
- This is normal! Keep the terminal open.
- Press Ctrl+C to stop, then run again to resume.

---

## Files

- **UI**: http://localhost:5000
- **Server**: `server.py`
- **Data**: `/Users/anuj/workspace-classifier/out/`

---

## Need More Help?

See `LOCAL-SETUP.md` for detailed guide.

---

**Start extracting!** 🚀
