import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from datetime import datetime

def get_price():
    # 設定 User-Agent 來模擬瀏覽器請求
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    url = "https://tw.stock.yahoo.com/quote/1229.TW"
    
    try:
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'  # 確保正確處理中文編碼
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 使用新的選擇器來匹配 Yahoo 股市的價格元素
        price_element = soup.find('span', {'class': ['Fz(32px)', 'Fw(b)', 'Lh(1)', 'Mend(16px)', 'D(f)', 'Ai(c)']})
        
        if price_element:
            # 移除可能的貨幣符號並轉換為浮點數
            price = float(price_element.text.strip().replace('$', '').replace(',', ''))
            print(f"成功抓取價格: {price}")  # 添加調試輸出
            return price
        else:
            # 如果找不到元素，將頁面內容儲存以供調試
            with open('debug.html', 'w', encoding='utf-8') as f:
                f.write(soup.prettify())
            raise Exception("無法找到價格元素，已將頁面內容儲存到 debug.html")
    
    except Exception as e:
        print(f"錯誤: {str(e)}")
        return None

def send_email(subject, body):
    # Gmail 設定
    sender_email = "chenboan1130@gmail.com"  # 替換成你的 Gmail
    receiver_email = "brichrlit@gmail.com"  # 替換成接收通知的信箱
    password = "bchn ndyl nuyr epbm"  # 替換成你的應用程式密碼
    
    # 建立郵件
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    
    message.attach(MIMEText(body, "plain"))
    
    try:
        # 建立 SMTP 連線
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(sender_email, password)
        server.send_message(message)
        server.quit()
        print("郵件發送成功！")
    except Exception as e:
        print(f"郵件發送失敗: {str(e)}")

def main():
    price = get_price()
    
    if price is not None:
        print(f"當前價格: {price}")
        
        if price < 40:
            send_email(
                "聯華實業(1229)價格警告 - 請盡速賣出",
                f"""當前價格 ({price}) 已低於 40！\n\n
購入價格62.38 (持有79股)
                
時間: {datetime.now()}
                
            """)
        elif price > 55:
            send_email(
                "聯華實業(1229)價格警告 - 高於預期",
                f"當前價格 ({price}) 已高於 55！\n\n時間: {datetime.now()}"
            )

if __name__ == "__main__":
    main()