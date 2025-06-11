from datetime import datetime
from appmain.routeBus.bus_api import get_fastest_bus, start_stations_033, start_stations_85
from appmain.shuttle.shuttle_loader import load_shuttle_json

def parse_shuttle_time(shuttle_time_str):
    """HH:MM 포맷의 시간을 datetime 객체로 변환"""
    now = datetime.now()
    hour, minute = map(int, shuttle_time_str.split(":"))
    return datetime(now.year, now.month, now.day, hour, minute)

def get_next_shuttle_info(shuttle_list, time_col_index):
    now = datetime.now()
    for entry in shuttle_list:
        if len(entry) <= time_col_index:
            continue
        time_str = entry[time_col_index]
        if not time_str:
            continue
        shuttle_time = parse_shuttle_time(time_str)
        if shuttle_time > now:
            minutes_left = int((shuttle_time - now).total_seconds() / 60)
            return {
                "time": time_str,
                "minutes_left": minutes_left
            }
    return {"time": None, "minutes_left": None}

def get_recommendation_summary():
    result_033 = get_fastest_bus(start_stations_033, 241328006, "033")
    result_85 = get_fastest_bus(start_stations_85, 241415003, "85")
    shuttle_info = load_shuttle_json()

    # ✅ 등교용 시간은 백석역: index 1 / 삼송역: index 1
    next_baekseok = get_next_shuttle_info(shuttle_info["baekseok"], time_col_index=1)

    next_samsong = get_next_shuttle_info(shuttle_info["samsong"], time_col_index=1)

    # 버스 도착 시간 파싱
    try:
        bus_minutes = int(result_033.get("arriveTime", "999").replace("분", "").strip())
    except:
        bus_minutes = 999

    shuttle_minutes = next_baekseok.get("minutes_left") or 999

    # 추천 조건: 더 빠른 쪽을 선택
    if bus_minutes < shuttle_minutes:
        recommended = {
            "type": "bus",
            "route": "033",
            "info": result_033
        }
    else:
        recommended = {
            "type": "shuttle",
            "route": "백석역 셔틀",
            "info": next_baekseok
        }

    return {
        "result_033": result_033,
        "result_85": result_85,
        "shuttle": shuttle_info,
        "summary": {
            "baekseok": next_baekseok,
            "samsong": next_samsong
        },
        "recommended": recommended
    }
