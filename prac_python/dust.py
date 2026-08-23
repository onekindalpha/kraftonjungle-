import requests # requests 라이브러리 설치 필요

# 서울시 대기 OpenAPI에서 미세먼지 정보 받기
r = requests.get('http://openapi.seoul.go.kr:8088/6d4d776b466c656533356a4b4b5872/json/RealtimeCityAir/1/99')
rjson = r.json()

gus = rjson['RealtimeCityAir']['row'] 

# PM값이 60 미만인 구의 이름과 PM값 프린트하기
for gu in gus:
  if gu['PM'] < 60:
    print(gu['MSRSTN_NM'], gu['PM'])


