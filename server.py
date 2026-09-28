#!/usr/bin/env python3
"""
Flask server for Google Workspace Exporter UI
Handles file uploads, extraction requests, and progress tracking
"""

import json
import os
import subprocess
import threading
import time
from flask import Flask, request, jsonify
from pathlib import Path
from datetime import datetime

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
app.config['UPLOAD_FOLDER'] = '/tmp/gws-uploads'

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Store extraction status
extraction_status = {
    'active': False,
    'progress': 0,
    'current_user': '',
    'status': 'Idle',
    'errors': [],
    'start_time': None
}

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok'})

@app.route('/api/extract', methods=['POST'])
def start_extraction():
    """Start extraction with uploaded files and parameters"""
    try:
        # Check if extraction is already running
        if extraction_status['active']:
            return jsonify({'error': 'Extraction already in progress'}), 409

        # Get form data
        if 'json_file' not in request.files:
            return jsonify({'error': 'No JSON file provided'}), 400

        json_file = request.files['json_file']
        admin_email = request.form.get('admin_email', '').strip()
        employee_emails = json.loads(request.form.get('employee_emails', '[]'))
        date_from = request.form.get('date_from', '')
        date_to = request.form.get('date_to', '')

        # Validate inputs
        if not admin_email or '@' not in admin_email:
            return jsonify({'error': 'Invalid admin email'}), 400

        if not employee_emails:
            return jsonify({'error': 'No employee emails provided'}), 400

        for email in employee_emails:
            if '@' not in email:
                return jsonify({'error': f'Invalid email: {email}'}), 400

        # Save JSON file
        json_path = os.path.join(app.config['UPLOAD_FOLDER'], 'service_account.json')
        json_file.save(json_path)

        # Validate JSON
        try:
            with open(json_path) as f:
                json.load(f)
        except json.JSONDecodeError:
            return jsonify({'error': 'Invalid JSON file'}), 400

        # Start extraction in background thread
        thread = threading.Thread(
            target=run_extraction,
            args=(admin_email, employee_emails, date_from, date_to, json_path)
        )
        thread.daemon = True
        thread.start()

        return jsonify({
            'status': 'started',
            'message': f'Extraction started for {len(employee_emails)} employee(s)'
        }), 202

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def run_extraction(admin_email, employee_emails, date_from, date_to, json_path):
    """Run extraction command in background"""
    try:
        extraction_status['active'] = True
        extraction_status['progress'] = 0
        extraction_status['start_time'] = datetime.now()
        extraction_status['errors'] = []

        # Build command
        cmd = [
            'python3', 'run_org_classify.py',
            '--admin', admin_email,
            '--export-only',
            '--local-only'
        ]

        # Add employee emails
        for email in employee_emails:
            cmd.extend(['--only', email])

        # Add date range if provided
        if date_from:
            cmd.extend(['--modified-after', date_from])
        if date_to:
            cmd.extend(['--modified-before', date_to])

        # Run extraction
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd='/Users/anuj/workspace-classifier'
        )

        # Monitor progress
        total_lines = 0
        for line in iter(process.stdout.readline, ''):
            if line:
                total_lines += 1
                parse_progress_line(line, employee_emails)

                # Update progress based on output
                progress = min(95, (total_lines / 1000) * 100)
                extraction_status['progress'] = progress

                print(f"[PROGRESS] {progress:.0f}% - {line.strip()}")

        # Wait for completion
        stdout, stderr = process.communicate()

        if process.returncode == 0:
            extraction_status['status'] = 'Complete'
            extraction_status['progress'] = 100
            print(f"[SUCCESS] Extraction completed in {time.time() - extraction_status['start_time'].timestamp():.1f}s")
        else:
            extraction_status['status'] = 'Failed'
            extraction_status['errors'].append(stderr if stderr else 'Unknown error')
            print(f"[ERROR] Extraction failed: {stderr}")

    except Exception as e:
        extraction_status['status'] = 'Error'
        extraction_status['errors'].append(str(e))
        print(f"[ERROR] {e}")
    finally:
        extraction_status['active'] = False

def parse_progress_line(line, employee_emails):
    """Parse progress from log line"""
    line_lower = line.lower()

    # Check which user is being processed
    for email in employee_emails:
        if email in line:
            extraction_status['current_user'] = email.split('@')[0]
            break

    # Update status based on keywords
    if 'gmail' in line_lower and 'exported' in line_lower:
        extraction_status['status'] = 'Downloading Gmail...'
    elif 'dump' in line_lower or 'download' in line_lower:
        extraction_status['status'] = 'Downloading Drive files...'
    elif 'scan' in line_lower:
        extraction_status['status'] = 'Scanning files...'
    elif 'zip' in line_lower:
        extraction_status['status'] = 'Creating archive...'

@app.route('/api/status', methods=['GET'])
def get_status():
    """Get current extraction status"""
    elapsed = None
    if extraction_status['start_time']:
        elapsed = time.time() - extraction_status['start_time'].timestamp()

    return jsonify({
        'active': extraction_status['active'],
        'progress': extraction_status['progress'],
        'current_user': extraction_status['current_user'],
        'status': extraction_status['status'],
        'errors': extraction_status['errors'],
        'elapsed_seconds': elapsed
    })

@app.route('/api/cancel', methods=['POST'])
def cancel_extraction():
    """Cancel ongoing extraction"""
    if extraction_status['active']:
        extraction_status['active'] = False
        extraction_status['status'] = 'Cancelled'
        return jsonify({'status': 'cancelled'}), 200
    return jsonify({'error': 'No extraction in progress'}), 400

@app.route('/')
def index():
    """Serve the UI"""
    with open('/Users/anuj/workspace-classifier/gws-exporter-ui.html', 'r') as f:
        return f.read()

if __name__ == '__main__':
    print("🚀 GWS Exporter Server starting...")
    print("📊 Open http://localhost:5000 in your browser")
    app.run(debug=False, host='127.0.0.1', port=5000)
