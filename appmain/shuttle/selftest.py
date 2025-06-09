import requests
from bs4 import BeautifulSoup
import  json
import os
url ="https://www.joongbu.ac.kr/menu.es?mid=a10107020000"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser" )
table = soup.find("table")


columns = [th.get_text(strip=True) for th in table.find("thead").find_all("th")]
tbody = table.find('tbody')
# 파싱 대상 tbody
rows = []
# 현재 구분 저장 변수
current = {"up": "", "down": ""}

for tr in tbody.find_all("tr"):
    cells = tr.find_all(["td", "th"])
    texts = [td.get_text(strip=True) for td in cells]

    if len(texts) == 7:
        current["up"] = texts[0]
        current["down"] = texts[4]
        rows.append(texts)
    elif len(texts) == 5:
        filled = [
            current["up"],           # 등교 구분
            texts[0],                # 원흥역
            texts[1],                # 삼송역
            texts[2],                # 캠퍼스 하차
            current["down"],         # 하교 구분
            texts[3],                # 캠퍼스 승차
            texts[4]                 # 비고
        ]
        rows.append(filled)

# JSON 구조로 정리
result = {
    "삼송역": {
        "columns": columns,
        "rows": rows
    }
}
print(result)