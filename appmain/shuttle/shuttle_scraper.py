import requests
from bs4 import BeautifulSoup
import pandas as pd
import os



def find_shuttle_table(target):
    url = "https://www.joongbu.ac.kr/menu.es?mid=a10107020000"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    tables = soup.find_all("table")

    # 대상 테이블 찾기
    target_table = None
    for table in tables:
        caption = table.find("caption")
        if caption and target in caption.get_text(strip=True):
            target_table = table
            break

    parsed_rows = []

    if not target_table:
        print(f" '{target}'에 해당하는 테이블을 찾을 수 없습니다.")
        return None

    print(f" '{target}' 테이블 찾음")

    # 헤더 추출
    select_col = [th.get_text(strip=True) for th in target_table.find("thead").find_all("th")]

    # row 추출 및 보정
    current_up = "등교"
    current_down = "하교"
    for row in target_table.find("tbody").find_all("tr"):
        cells = row.find_all(["td", "th"])
        values = [cell.get_text(strip=True) for cell in cells]

        # 👇 구조별로 보정
        if len(values) == 7:
            # 완전한 행 (삼송역 첫 행)
            current_up = values[0]
            current_down = values[4]
            parsed_rows.append(values)

        elif len(values) == 5:
            # 비고(등교/하교) 생략된 삼송역 행
            filled = [current_up] + values[:3] + [current_down] + values[3:]
            parsed_rows.append(filled)

        elif len(values) == 6:
            # 백석역 첫 행
            current_up = values[0]
            current_down = values[3]
            parsed_rows.append(values)

        elif len(values) == 4:
            # 비고(등교/하교) 생략된 백석역  행
            filled = [current_up, values[0], values[1], current_down, values[2], values[3]]
            parsed_rows.append(filled)

        else:
            print(f"예상치 못한 열 수: {len(values)}개 → {values}")

    # DataFrame 생성
    try:
        table_df = pd.DataFrame(data=parsed_rows, columns=select_col)
    except Exception as e:
        print(f"DataFrame 생성 실패: {e}")
        return None

    return table_df


def save_schedule_if_updated(target, save_path):
    df = find_shuttle_table(target)
    if df is None:
        print(f"{target} 테이블 없음 또는 내용 비어있음. 저장 생략")
        return

    if os.path.exists(save_path):
        old = pd.read_json(save_path)
        if df.equals(old):
            print("변경사항 없음. 저장 생략.")
            return

    df.to_json(save_path, orient="split", force_ascii=False, indent=2)
    print(f"{target} 스케줄 갱신됨 → {save_path}")

save_schedule_if_updated("삼송역", "/Users/iminhyeong/DevMH/busAlert/appmain/static/data/shuttle_samsong.json")
save_schedule_if_updated("백석역", "/Users/iminhyeong/DevMH/busAlert/appmain/static/data/shuttle_backseck.json")