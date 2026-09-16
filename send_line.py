import os
import json
import datetime
import urllib.request
import urllib.error

url = "https://api.line.me/v2/bot/message/push"
token = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN", "").strip()
user_id = os.environ.get("LINE_USER_ID", "").strip()

# โหลดข้อมูลตารางเวลา
with open("schedule.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# แปลงเวลา UTC ของ GitHub ให้เป็นเวลาประเทศไทย (UTC+7)
thailand_tz = datetime.timezone(datetime.timedelta(hours=7))
now_in_thailand = datetime.datetime.now(thailand_tz)

# ดึงชื่อวันปัจจุบันตามเวลาไทย
days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
today_name = days[now_in_thailand.weekday()]

# จัดฟอร์แมตข้อความ
if today_name in data:
    tasks = "\n".join([f"• {item}" for item in data[today_name]])
    message_text = f"📌 ตารางเวลาประจำวัน ({today_name.upper()}):\n\n{tasks}"
else:
    message_text = f"📌 ตารางเวลาประจำวัน ({today_name.upper()}):\n\nวันนี้ไม่มีตารางเรียนครับ! 🎉"

payload = {
    "to": user_id,
    "messages": [{"type": "text", "text": message_text}]
}

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + token
}

req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)

try:
    with urllib.request.urlopen(req) as response:
        print("ส่งข้อความสำเร็จ! Status:", response.status)
except urllib.error.HTTPError as e:
    print("ส่งไม่ผ่าน! Error Code:", e.code)
    raise e
    
