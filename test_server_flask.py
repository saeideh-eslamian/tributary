# Using requests version 2.31.0
import requests

url = "http://127.0.0.1:8000/record"

payload = {"engine_temperature": 0.3}
response = requests.post(url, json=payload)

# Check the response status code
if response.status_code == 200:
    print("Request successful!")
else:
    print(f"Request failed with status code: {response.status_code}")