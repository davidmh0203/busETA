import requests
from bs4 import BeautifulSoup
import  json
import os
url ="https://www.joongbu.ac.kr/menu.es?mid=a10107020000"  # 대상 URL

response = requests.get(url) # requset로 url 접근
soup = BeautifulSoup(response.text, "html.parser" ) # beautifulSoup 함수? 객체 생성? 수프에 담기
#수프를 그릇에 담듯이
# table = soup.find("table")
#HTML 태그를 찾는 함수, 파라미터 안에 html이 지원하는 모든  태그 <>를 "" 문자열 형식으로 넣으면 해당하는 태그 내용을 찾을수 있다. -> 단, 해당 문서에서 가장 첫번째 해당 태그만 반환한다.
# <>안에 들어가는 단순한 태그 뿐만 아니라, class='', id='' 같이  태그 안의 파라미터를 통해서도 찾을수 있다.
table = soup.find_all("table")
#find_all 은  내가원하는 태그에 대해 문서안의 해당 태그를 모두 찾고 싶을때 사용한다.

#
# caption = str(soup.find_all("caption"))
#
# if "삼송역" in caption:
#     print(caption) # 캡션 -> 텍스트 -> 삼송역 들어있는거 가져오기

td = soup.find_all("tr")
