import sys
import os
import hashlib
import hmac
import base64
import requests #pip install requests
import time
import json


# unix timestamp 설정
timestamp = int(time.time() * 1000)
timestamp = str(timestamp)

# Ncloud API Key 설정
ncloud_accesskey = "NCP 계정 accesskey"
ncloud_secretkey = "NCP 계정 secretkey"

# 암호화 문자열 생성을 위한 기본값 설정
apicall_method = "GET"
space = " "
new_line = "\n"

# API 서버 정보
api_server = "https://ncloud.apigw.ntruss.com"

# API URL 
api_url = "/vserver/v2/getServerInstanceList?responseFormatType=json"
#api_url = api_url +"?regionCode=KR&productCode=SPCF000000000001&responseFormatType=json"

# hmac으로 암호화할 문자열 생성
message = apicall_method + space + api_url + new_line + timestamp + new_line + ncloud_accesskey
message = bytes(message, 'UTF-8')

# hmac_sha256 암호화
ncloud_secretkey = bytes(ncloud_secretkey, 'UTF-8')
signingKey = base64.b64encode(hmac.new(ncloud_secretkey, message, digestmod=hashlib.sha256).digest())

# http 호출 헤더값 설정
http_header = {
    'x-ncp-apigw-timestamp': timestamp,
    'x-ncp-iam-access-key': ncloud_accesskey,
    'x-ncp-apigw-signature-v2': signingKey
}

# api 호출
response = requests.get(api_server + api_url, headers=http_header)

#print (response.text)


# 응답받은 response를 출력
#print(response.text)

#현재 응답받은 데이터의 타입 확인 -> 현재 데이터는 정확하게 json 데이터가 아닌 request의 응답 데이터라는 클레스로 출력됨(<class 'requests.models.Response'>)
#print(type(response))

# 데이터를 파이썬 딕션어리 데이터 타입으로 저장
real_data = json.loads(response.text)

# 변환 확인 및 출력

#print(type(real_data))
#<class 'dict'> 확인 -> 즉 api응답 데이터가 파이선 dic 데이터 타입으로 변환된 것을 확인.

#print(real_data)

#응답데이터 내용 중 전체는 dictionary 자료형으로 되어 있고 그 안에 serverinstancelist는 리스트로 되어있음.
#serverinstancelist를 변수에 넣고 for문을 이용하여 이름 및 상태만 출력
list = real_data["getServerInstanceListResponse"]["serverInstanceList"]

for name in list:
    print(name['serverName'] + " / " + name["serverInstanceStatusName"])
