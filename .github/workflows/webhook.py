import requests
import os
from datetime import datetime, timedelta, timezone

# KST 설정
KST = timezone(timedelta(hours=9))
now_kst = datetime.now(KST).strftime("%Y-%m-%d %H:%M:%S")

# 환경변수에서 Webhook URL 불러오기
WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

if not WEBHOOK_URL:
    raise ValueError("DISCORD_WEBHOOK_URL 환경변수가 설정되지 않았습니다.")

# 디스코드 메시지 내용
payload = {
    "content": f"[KST] 자동 메시지 전송 시간: {now_kst}"
}

# 전송
response = requests.post(WEBHOOK_URL, json=payload)

# 결과 출력
print("Status Code:", response.status_code)
print("Response:", response.text)
