import json
import os
import datetime
import urllib.request

def send_line_message(message_text, access_token, user_id):
    """ส่งข้อความ Push Message เข้า LINE ผ่าน Messaging API"""
    url = "https://api.line.me/v2/bot/message/push"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    
    payload = {
        "to": user_id,
        "messages": [
            {
                "type": "text",
                "text": message_text
            }
        ]
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers=headers)
    
    try:
        with urllib.request.urlopen(req) as response:
            print("✅ ส่งข้อความเข้า LINE เรียบร้อยแล้ว!")
            return response.read()
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาดในการส่งข้อความ: {e}")

def main():
    # 1. ดึง Token และ User ID จาก Environment Variables
    LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
    LINE_USER_ID = os.getenv("LINE_USER_ID")
    
    if not LINE_CHANNEL_ACCESS_TOKEN or not LINE_USER_ID:
        print("❌ ไม่พบ LINE_CHANNEL_ACCESS_TOKEN หรือ LINE_USER_ID ในระบบ")
        return

    # 2. อ่านไฟล์ตารางงาน
    try:
        with open("schedule.json", "r", encoding="utf-8") as f:
            schedules = json.load(f)
    except FileNotFoundError:
        print("❌ ไม่พบไฟล์ schedule.json")
        return

    # 3. เช็กวันปัจจุบัน (แปลงเวลาเป็น UTC+7 สำหรับเวลาไทย)
    utc_now = datetime.datetime.now(datetime.timezone.utc)
    th_now = utc_now + datetime.timedelta(hours=7)
    
    day_name = th_now.strftime("%A").lower()
    date_str = th_now.strftime("%d/%m/%Y")

    # 4. ดึงรายการตารางงานของวันนี้
    today_tasks = schedules.get(day_name, [])

    # 5. จัดรูปแบบข้อความ
    message = f"📌 ตารางประจำวันนี้ ({date_str})\n\n"
    if today_tasks:
        for task in today_tasks:
            message += f"• {task}\n"
    else:
        message += "🎉 วันนี้ไม่มีกิจกรรมในตารางงานครับ!"

    print("--- ข้อความที่จะส่ง ---")
    print(message)
    print("---------------------")

    # 6. ส่งเข้า LINE
    send_line_message(message, LINE_CHANNEL_ACCESS_TOKEN, LINE_USER_ID)

if __name__ == "__main__":
    main()
  
