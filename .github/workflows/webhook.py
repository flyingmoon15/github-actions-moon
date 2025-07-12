import os
import requests
from requests.auth import HTTPBasicAuth

# 시크릿 값 불러오기
client_id = os.environ.get('BLIZZARD_CLIENT_ID')
client_secret = os.environ.get('BLIZZARD_CLIENT_SECRET')
discord_webhook_url = os.environ.get('DISCORD_WEBHOOK_URL')

price_threshold = 160000  # 이 가격 이하일 때 알림

def get_access_token(client_id, client_secret):
    url = 'https://oauth.battle.net/token'
    data = {'grant_type': 'client_credentials'}
    response = requests.post(url, data=data, auth=HTTPBasicAuth(client_id, client_secret))
    if response.status_code == 200:
        return response.json()['access_token']
    return None

def get_wow_token_price(token, region='kr'):
    url = f"https://{region}.api.blizzard.com/data/wow/token/?namespace=dynamic-{region}&locale=ko_KR"
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()['price'] // 10000
    return None

def send_discord_alert(price):
    message = f"토큰 가격이 {price} 골드입니다! 지금 구매 고려하세요."
    data = {"content": message}
    requests.post(discord_webhook_url, json=data)

def main():
    if not (client_id and client_secret and discord_webhook_url):
        return  # 시크릿이 하나라도 없으면 실행 안 함

    token = get_access_token(client_id, client_secret)
    if not token:
        return

    price = get_wow_token_price(token)
    if price is None:
        return

    if price <= price_threshold:
        send_discord_alert(price)

main()
