
import requests
from xml.etree import ElementTree

import urllib.parse

raw_key = "gFJ8RIV/tPoVyrS0iNMJJynEuapGx+tiKUgTB2CTvZG0uoyr/mC6PgAXCsE8uR+9CZjkKMn5+C29jGvQXzfXqQ=="
encoded_key = urllib.parse.quote(raw_key, safe="")

# 사용 예
url = f"http://apis.data.go.kr/6410000/busarrivalservice/getBusArrivalItem?serviceKey={encoded_key}&stationId=57078&routeId=241328006"


route_id_033 = 241328006
route_id_85 = 241415003

start_stations_033 = [
    {"name": "중부대학교입구", "stationId": "57078"},
    {"name": "중부대학교입구", "stationId": "57079"},
]

start_stations_85 = [
    {"name": "중부대학교입구", "stationId": "57078"},
    {"name": "중부대학교입구", "stationId": "57079"},
]


def get_arrival_info(station_id, route_id):
    url = "http://apis.data.go.kr/6410000/busarrivalservice/getBusArrivalItem"
    params = {
        "serviceKey": raw_key,
        "stationId": station_id,
        "routeId": route_id
    }
    response = requests.get(url, params=params)

    print("\n📡 요청 URL:", response.url)
    print("📄 응답 본문:", response.text[:500])  # 긴 응답 일부만 출력

    try:
        root = ElementTree.fromstring(response.content)
    except Exception as e:
        print("❌ XML 파싱 실패:", e)
        return {"message": "XML 파싱 오류"}

    item = root.find(".//busArrivalItem")
    if item is not None:
        print("✅ 도착 정보 있음")
        return {
            "도착예상시간(분)": item.findtext("predictTime1"),
            "버스위치": item.findtext("locationNo1"),
            "남은좌석": item.findtext("remainSeatCnt1")
        }
    else:
        print("⚠️ <busArrivalItem> 없음")
        return {"message": "도착 정보 없음"}


def get_fastest_bus(stations, route_id, bus_name):
    fastest = None
    for station in stations:
        info = get_arrival_info(station["stationId"], route_id)
        if "도착예상시간(분)" in info and info["도착예상시간(분)"]:
            try:
                time = int(info["도착예상시간(분)"])
                if (fastest is None) or (time < fastest["time"]):
                    fastest = {
                        "bus": bus_name,
                        "station": station["name"],
                        "time": time,
                        "info": info
                    }
            except ValueError:
                continue
    return fastest

def get_recommendation():
    result_033 = get_fastest_bus(start_stations_033, route_id_033, "033")
    result_85 = get_fastest_bus(start_stations_85, route_id_85, "85")
    return [result_033, result_85]



