from bs4 import BeautifulSoup
import requests

url = "https://www.joongbu.ac.kr/menu.es?mid=a10107020000"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# 모든 테이블 탐색
tables = soup.find_all("table")

target_table = None
for table in tables:
    caption = table.find("caption")
    if caption and "삼송역" in caption.get_text(strip=True): # caption and "삼송역" -> 왜? captioneh rkxdlgka?
        target_table = table
        break
parsed_rows=[]
if target_table:
    print("삼송역 셔틀 테이블 찾음!")

    current_up = "등교"
    current_down = "하교"
    for row in target_table.find("tbody").find_all("tr"):
        cells = row.find_all(["td", "th"])
        values = [cell.get_text(strip=True) for cell in cells]

        if len(values) == 7:
            current_up = values[0]
            current_down= values[4]
            parsed_rows.append(values)
        elif len(values) ==5:
            filled = [current_up] + values[:3] + [current_down] + values[3:]
            parsed_rows.append(filled)
        else:
            print(f"예상외 열수: {len(values)}-{values}")
    print("\n 파싱결과")
    # for row in parsed_rows:
    #     print(row)



else:
    print("삼송역 관련 테이블을 찾을 수 없습니다.")

school_idx, home_idx = None, None
for i, cell in enumerate(parsed_rows[0]):
    if cell == '등교':
        school_idx = i
    elif cell == '하교':
        home_idx = i

if school_idx is None or home_idx is None:
    print("'등교' 또는 '하교' 위치를 찾을 수 없습니다.")
    exit()

# 등교/하교 데이터 나누기
go_school = []
go_home = []

for row in parsed_rows:
    if len(row) > max(school_idx + 2, home_idx + 2):
        time_school = row[school_idx + 1]
        remark_school = row[school_idx + 2]
        time_home = row[home_idx + 1]
        remark_home = row[home_idx + 2]
        go_school.append({"time": time_school, "remark": remark_school})
        go_home.append({"time": time_home, "remark": remark_home})
result = {
    "삼송역": {
        "등교": go_school,
        "하교": go_home
    }
}

print(result)

# 구분이 잘못됨 , remark에 시간이 들어간 것도 읶음. 등교는 원흥역 출발시간, 삼송역 출발시간 , 캠퍼스 도착시간 나누고 하교는  캠퍼스 승차시간, 비고로 나눈다