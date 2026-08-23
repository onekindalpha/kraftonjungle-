import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}

data = requests.get(
    'https://www.imdb.com/chart/top/?ref_=nv_mv_250',
    headers=headers
)

print("status code:", data.status_code)
print("html 길이:", len(data.text))
print("html 내용:", repr(data.text[:300]))