
from datetime import datetime

from appmain.shuttle.shuttle_scraper import save_schedule_if_updated

#
# 배포후 주기적 크롤링 적용 -> 매 학기 시작, 한달에 한번(수요에 따른 수정 발생 상황)

# now = datetime.now()
# print(f"[{now}] 셔틀 스케줄 체크 중...")
#
# targets = ["삼송역", "백석역", "원흥역"]
# for name in targets:
#     save_schedule_if_updated(name, f"static/data/{name}_schedule.json")
