import urllib.request
import urllib.error
import urllib.parse
import json
import time
import os
import sys
from pathlib import Path

BASE_URL = "http://localhost:5001"

def make_request(url, method='GET', data=None):
    try:
        req = urllib.request.Request(url, method=method)
        if data:
            json_data = json.dumps(data).encode('utf-8')
            req.add_header('Content-Type', 'application/json')
            req.data = json_data
            
        with urllib.request.urlopen(req) as response:
            content = response.read().decode('utf-8')
            try:
                data = json.loads(content)
            except json.JSONDecodeError:
                data = content
            
            return {
                'status': response.status,
                'data': data
            }
    except urllib.error.URLError as e:
        if hasattr(e, 'read'):
            try:
                 err_data = json.loads(e.read().decode('utf-8'))
                 return {'status': e.code, 'error': err_data}
            except:
                return {'status': e.code, 'error': str(e)}
        return {'status': 0, 'error': str(e)}
    except Exception as e:
        return {'status': 0, 'error': str(e)}

def check_server_health():
    res = make_request(BASE_URL)
    return res['status'] == 200

def verify_generation():
    print("🔍 Checking server health...")
    if not check_server_health():
        print("❌ Server is not running. Please start the server (python app.py) in a separate terminal.")
        return

    print("✅ Server is running.")

    # 1. Trigger generation for a Grade 2 Narrative assessment (Sample 2 equivalent)
    payload = {
        'grade': '2',
        'assessment_type': 'comprehension',
        'genre': 'narrative'
    }

    print(f"\n🚀 Triggering generation for: {payload}")
    response = make_request(f"{BASE_URL}/api/generate", method='POST', data=payload)
    
    if response['status'] == 200:
        data = response['data']
        if data.get('success'):
            print(f"✅ Generation started successfully. PID: {data.get('pid')}")
            log_file = data.get('log_file')
            print(f"📂 Log file: {log_file}")
            
            # Monitor log file for a few seconds
            if log_file and os.path.exists(log_file):
                print("\n📄 Monitoring log file (first 10 seconds)...")
                for _ in range(10):
                    with open(log_file, 'r') as f:
                        content = f.read()
                        if content:
                            print(content[-500:]) # Print last 500 chars
                        else:
                            print("(Log file empty so far...)")
                    time.sleep(1)
            else:
                print("❌ Log file was not created immediately.")
        else:
            print(f"❌ Generation failed to start: {data.get('error')}")
    else:
        print(f"❌ API call failed: {response.get('error')}")

if __name__ == "__main__":
    verify_generation()
