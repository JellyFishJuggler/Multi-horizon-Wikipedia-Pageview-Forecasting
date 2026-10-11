import requests
import json 
from pathlib import Path

article = "Python_(programming language)"

url = ( "https://wikimedia.org/api/rest_v1/metrics/pageviews/"
    f"per-article/en.wikipedia.org/all-access/all-agents/"
    f"{article}/daily/2025010100/2026010100")

headers = {
    "User-Agent": "WikipediaForecastingProject/1.0 (guptasrijan85@gmail.com)"
}

response = requests.get(url=url,headers=headers)


print("Status:", response.status_code)
print("Content-Type:", response.headers.get("content-type"))
print("Response:", response.text[:1000])

data = response.json()
print(data)

FILE_NAME = 'data.json'
FILE_PATH = Path('data/') / FILE_NAME

with open(FILE_PATH, 'w', encoding='utf-8') as f:
    json.dump(data,f,indent=4)