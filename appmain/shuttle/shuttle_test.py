import requests
from bs4 import BeautifulSoup
import json
import os

# ✅ 현재 파일 기준 디렉토리
current_dir = os.path.dirname(os.path.abspath(__file__))

# ✅ 셔틀 시간표 페이지 요청
url = "https://www.joongbu.ac.kr/menu.es?mid=a10107020000"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
tables = soup.find_all("table")

# ✅ 삼송역 테이블: 뒤에서 두 번째
samsong_table = tables[-2]
samsong_headers = [th.get_text(strip=True) for th in samsong_table.find("thead").find_all("th")]
samsong_parsed = []
current_updown = {"등교": "", "하교": ""}

for row in samsong_table.find("tbody").find_all("tr"):
    cols = [td.get_text(strip=True) for td in row.find_all(["td", "th"])]
    if len(cols) == 7:
        current_updown["등교"] = cols[0]
        current_updown["하교"] = cols[4]
        samsong_parsed.append(cols)
    elif len(cols) == 5:
        filled = [
            current_updown["등교"],
            cols[0], cols[1], cols[2],
            current_updown["하교"],
            cols[3], cols[4]
        ]
        samsong_parsed.append(filled)

# ✅ 백석역 테이블: 마지막
baekseok_table = tables[-1]
baekseok_headers = [th.get_text(strip=True) for th in baekseok_table.find("thead").find_all("th")]
baekseok_parsed = []
current_updown = {"등교": "", "하교": ""}

for row in baekseok_table.find("tbody").find_all("tr"):
    cols = [td.get_text(strip=True) for td in row.find_all(["td", "th"])]
    if len(cols) == 6:
        current_updown["등교"] = cols[0]
        current_updown["하교"] = cols[3]
        baekseok_parsed.append(cols)
    elif len(cols) == 4:
        filled = [
            current_updown["등교"],
            cols[0], cols[1],
            current_updown["하교"],
            cols[2], cols[3]
        ]
        baekseok_parsed.append(filled)

# ✅ 병합 JSON 저장
shuttle_all = {
    "삼송역": {
        "columns": samsong_headers,
        "rows": samsong_parsed
    },
    "백석역": {
        "columns": baekseok_headers,
        "rows": baekseok_parsed
    }
}
combined_path = os.path.join(current_dir, "shuttle_schedule_combined.json")
with open(combined_path, "w", encoding="utf-8") as f:
    json.dump(shuttle_all, f, ensure_ascii=False, indent=2)
print(f"✅ 병합 저장 완료: {combined_path}")

# ✅ 분할된 JSON 저장
converted = {}
for station, info in shuttle_all.items():
    columns = info["columns"]
    rows = info["rows"]
    up_list, down_list = [], []

    for row in rows:
        if station == "백석역" and len(row) >= 6:
            up_list.append({"time": row[1], "remark": row[2]})
            down_list.append({"time": row[4], "remark": row[5]})
        elif station == "삼송역" and len(row) >= 7:
            up_list.append({"time": row[2], "remark": row[3]})
            down_list.append({"time": row[5], "remark": row[6]})

    converted[station] = {
        "등교": up_list,
        "하교": down_list
    }

split_path = os.path.join(current_dir, "shuttle_schedule_split.json")
with open(split_path, "w", encoding="utf-8") as f:
    json.dump(converted, f, ensure_ascii=False, indent=2)
print(f"✅ 분할 저장 완료: {split_path}")
