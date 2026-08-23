import requests

data = requests.get("https://example.com")

print("status code:", data.status_code)
print("html 길이:", len(data.text))
print("html 내용:", repr(data.text[:100]))