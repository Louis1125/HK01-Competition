import json, urllib.request, urllib.error, base64

# Tiny 1x1 PNG base64 (used as a safe test payload)
png_b64 = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8Xw8AAoMBgP9sR3sAAAAASUVORK5CYII='

data_url = 'data:image/png;base64,' + png_b64

payload = json.dumps({'image': data_url}).encode('utf-8')
req = urllib.request.Request('http://127.0.0.1:8000/detect', data=payload, headers={'Content-Type': 'application/json'})

try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        body = resp.read().decode('utf-8')
        print('Response:', body)
except urllib.error.HTTPError as e:
    print('HTTP Error:', e.code, e.read().decode('utf-8'))
except Exception as e:
    print('Error:', e)
