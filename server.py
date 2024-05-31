from fastapi import APIRouter, HTTPException, Query
import requests
import globals
import subscribe
import base64
from urllib.parse import quote

router = APIRouter()

def decode_base64_url(encoded_url: str) -> str:
    """解码 base64 编码的 URL"""
    try:
        decoded_bytes = base64.urlsafe_b64decode(encoded_url.encode('utf-8'))
        decoded_url = decoded_bytes.decode('utf-8')
        return decoded_url
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid base64 encoded URL: {str(e)}")

@router.get("/send_token")
def send_token(encoded_url: str):
    bark_send_url = decode_base64_url(encoded_url)
    url = f"{bark_send_url}{quote(globals.url_data['title'])}/{quote(globals.url_data['text'])}?icon={globals.url_data['icon']}"
    print(f"url: {url}")
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return {"message": "Request to external API successful", "status_code": response.status_code}
        else:
            raise HTTPException(status_code=response.status_code, detail="Failed to reach external API")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get_full_data")
def get_full_data():
    return globals.full_data

@router.post("/bark_subscribe")
def bark_subscribe(encoded_url: str, enable_quote_notif: bool = Query(...), quote_threshold: float = Query(...)):
    new_subscribe_url = decode_base64_url(encoded_url)
    subscription_exists = False

    for sub in globals.subscriptions:
        if sub.url == new_subscribe_url:
            # 更新现有订阅的参数
            sub.enable_quote_notif = enable_quote_notif
            sub.quote_threshold = quote_threshold
            subscription_exists = True
            break

    if not subscription_exists:
        # 添加新的订阅
        subscription = globals.Subscription(new_subscribe_url, enable_quote_notif, quote_threshold)
        globals.subscriptions.append(subscription)

    # 试着访问一下订阅url 如返回200则加入订阅
    try:
        response = requests.get(f"{new_subscribe_url}{quote('Successfully subscribe!')}/url:{quote(new_subscribe_url, safe='')}")
        if response.status_code == 200:
            subscribe.save_subscriptions()
            return {"message": "Request to external API successful", "status_code": response.status_code}

        else:
            print(f"failed to subscribe! URL: {new_subscribe_url}, Code: {response.status_code}")
            raise HTTPException(status_code=response.status_code, detail="Failed to subscribe!")

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.post("/bark_unsubscribe")
def bark_unsubscribe(encoded_url: str):
    url = decode_base64_url(encoded_url)
    for sub in globals.subscriptions:
        if sub.url == url:
            globals.subscriptions.remove(sub)
            subscribe.save_subscriptions()
            return {"message": "Unsubscribed successfully", "url": url}
    raise HTTPException(status_code=404, detail="URL not found in subscriptions")

@router.get("/get_subscribe_data")
def get_subscribe_data():
    return globals.subscriptions
