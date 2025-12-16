import urllib.request
import json
import sys
import os

BASE_URL = "http://localhost:8081/api"
OUTPUT_FILE = "test_results.txt"

def log(message):
    with open(OUTPUT_FILE, "a") as f:
        f.write(str(message) + "\n")
    print(message)

def test_chat():
    url = f"{BASE_URL}/chat"
    data = {
        "userId": "test_user_py",
        "message": "I am Rajdeep, I need a loan of 50000"
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            log(f"Chat Response: {result}")
            return result
    except Exception as e:
        log(f"Chat Failed: {e}")
        return None

def test_upload():
    # Simple multipart upload using boundary
    url = f"{BASE_URL}/upload"
    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    
    # File content
    file_content = b"Dummy loan document content."
    filename = "dummy_doc.txt"
    
    # Build body
    body = []
    body.append(f"--{boundary}".encode('utf-8'))
    body.append(f'Content-Disposition: form-data; name="userId"'.encode('utf-8'))
    body.append(b'')
    body.append(b'test_user_py')
    
    body.append(f"--{boundary}".encode('utf-8'))
    body.append(f'Content-Disposition: form-data; name="file"; filename="{filename}"'.encode('utf-8'))
    body.append(b'Content-Type: text/plain')
    body.append(b'')
    body.append(file_content)
    
    body.append(f"--{boundary}--".encode('utf-8'))
    body.append(b'')
    
    body_bytes = b'\r\n'.join(body)
    
    req = urllib.request.Request(
        url,
        data=body_bytes,
        headers={
            'Content-Type': f'multipart/form-data; boundary={boundary}',
            'Content-Length': len(body_bytes)
        }
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            log(f"Upload Response: {result}")
            return result
    except Exception as e:
        log(f"Upload Failed: {e}")
import urllib.request
import json
import sys
import os

BASE_URL = "http://localhost:8081/api"
OUTPUT_FILE = "test_results.txt"

def log(message):
    with open(OUTPUT_FILE, "a") as f:
        f.write(str(message) + "\n")
    print(message)

def test_chat():
    url = f"{BASE_URL}/chat"
    data = {
        "userId": "test_user_py",
        "message": "My name is Rajdeep and I need a loan of 50000"
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            log(f"Chat Response: {result}")
            return result
    except Exception as e:
        log(f"Chat Failed: {e}")
        return None

def test_upload():
    # Simple multipart upload using boundary
    url = f"{BASE_URL}/upload"
    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    
    # File content
    file_content = b"Dummy loan document content."
    filename = "dummy_doc.txt"
    
    # Build body
    body = []
    body.append(f"--{boundary}".encode('utf-8'))
    body.append(f'Content-Disposition: form-data; name="userId"'.encode('utf-8'))
    body.append(b'')
    body.append(b'test_user_py')
    
    body.append(f"--{boundary}".encode('utf-8'))
    body.append(f'Content-Disposition: form-data; name="file"; filename="{filename}"'.encode('utf-8'))
    body.append(b'Content-Type: text/plain')
    body.append(b'')
    body.append(file_content)
    
    body.append(f"--{boundary}--".encode('utf-8'))
    body.append(b'')
    
    body_bytes = b'\r\n'.join(body)
    
    req = urllib.request.Request(
        url,
        data=body_bytes,
        headers={
            'Content-Type': f'multipart/form-data; boundary={boundary}',
            'Content-Length': len(body_bytes)
        }
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            log(f"Upload Response: {result}")
            return result
    except Exception as e:
        log(f"Upload Failed: {e}")
        return None

if __name__ == "__main__":
    # Clear file
    with open(OUTPUT_FILE, "w") as f:
        f.write("Starting Tests...\n")
     # 1. Chat API
    print("Testing Chat...")
    chat_res = test_chat() # Call test_chat to use the updated message
    
    if chat_res:
        log("\nTesting Upload...")
        test_upload()
