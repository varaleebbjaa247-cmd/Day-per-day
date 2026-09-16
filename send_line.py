import os
import json
import urllib.request
import urllib.error

url = "https://api.line.me/v2/bot/message/push"
token = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
user_id = os.environ.get("LINE_USER_ID")

# โหลดข้อมูลตาราง
with open("schedule.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# ปรับรูปแบบข้อความที่จะส่ง
message_text = "📅 ตารางเวลาประจำวัน:\n" + json.dumps(data, ensure_ascii=False, indent=2)

payload = {
    "to": user_id,
    "messages": [
        {
            "type": "text",
            "text": message_text
        }
    ]
}

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}

req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)

try:
    with urllib.request.urlopen(req) as response:
        print("ส่งข้อความสำเร็จ! Status:", response.status)
except urllib.error.HTTPError as e:
    print("ส่งไม่ผ่าน! Error Code:", e.code)
    print("รายละเอียด:", e.read().decode("utf-8"))
    raise e
