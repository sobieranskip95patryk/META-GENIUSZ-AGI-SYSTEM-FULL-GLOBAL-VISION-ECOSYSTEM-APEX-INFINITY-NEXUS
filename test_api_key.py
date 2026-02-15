import requests
import json

key = "AIzaSyDw_FJlG3N5oP9AtefKKNvIArPqhbeBq1A"
url = f"https://generativelanguage.googleapis.com/v1beta/models?key={key}"

print(f"Testing API Key: {key}...")
print(f"URL: {url}")

try:
    # Use verify=False to rule out SSL issues for a quick test (not recommended for prod)
    response = requests.get(url, timeout=10)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        print("SUCCESS! API Key is valid. Available models:")
        models = response.json().get('models', [])
        for m in models:
            if 'flash' in m['name'] or 'pro' in m['name']:
                print(f" - {m['name']}")
    else:
        print(f"FAILURE. Response: {response.text}")
        
except Exception as e:
    print(f"EXCEPTION: {e}")
