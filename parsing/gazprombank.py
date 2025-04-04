from bs4 import BeautifulSoup
import time
from datetime import datetime, timedelta
import fake_useragent
import requests
import json
from month import months_dict
from database import c, db
import smtplib
from email.mime.text import MIMEText

name_bank = 'Газпромбанк' 
page = 1
days_ago = datetime.now() - timedelta(days=730)
url_main = 'https://www.gazprombank.ru'
error_log = []  # Список для хранения ошибок
err = "Ошибок при парсинге банка Газпромбанк не обнаружено"

def send_error_report(errors):
    if not errors:
        return
    # Настройки для отправки почты
    sender_email = "example.com"
    receiver_email = "example.com"
    subject = "Отчет об ошибках парсинга новостей"
    body = "\n".join(errors)
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email
    try:
        with smtplib.SMTP('smtp.example.com', 587) as server:
            server.starttls()
            server.login(sender_email, "password")
            server.sendmail(sender_email, receiver_email, msg.as_string())
            print("Отчет об ошибках отправлен на почту.")
    except Exception as e:
        print(f"Не удалось отправить отчет об ошибках: {e}")

def scrape_gazprombank_news():
    random_user_agent = fake_useragent.UserAgent().random
    header = {'user-agent': random_user_agent}
    global page
    global url_main
    while True:
        url_json = f'https://www.gazprombank.ru/rest/page/press-center/list?ab_segment=segment12&categoryCode=press&cityId=617&page={page}&lang=ru'
        try:
            response = requests.get(url_json, headers=header)
            response.raise_for_status()
        except requests.RequestException as e:
            error_log.append(f"{name_bank}.Ошибка при получении JSON данных: {e}")
            break
        try:
            data = response.json()
        except json.JSONDecodeError as e:
            error_log.append(f"{name_bank}.Ошибка при декодировании JSON: {e}")
            break
        if "blocks" not in data or not data["blocks"]:
            print("Больше нет новостей для получения, выход.")
            break
        for item in data["blocks"][0]["block"]["items"]:
            date = item['date'].replace(',', '').split(' ')
            date[1] = months_dict[date[1]]
            date = '.'.join(date)
            date_object = datetime.strptime(date, "%d.%m.%Y")
            formatted_date = date_object.strftime("%d.%m.%Y")  
            if date_object >= days_ago:
                name = item['name'] 
                url = item['url']
                full_url = url_main + url
                try:
                    response_news = requests.get(full_url, headers=header, timeout=30)
                    response_news.raise_for_status()
                except requests.RequestException as e:
                    error_log.append(f"{name_bank}.{name}.{formatted_date}.Ошибка при получении статьи: {e}")
                    continue

                soup = BeautifulSoup(response_news.text, 'html.parser')
                news_items = soup.find_all('div', class_="article_text-93e article_text_default-93e")
                
                if not news_items:
                    error_log.append(f"{name_bank}.{name}.{formatted_date}.Текст статьи не найден.")
                    continue

                now = datetime.now()
                now_date = now.strftime("%d.%m.%Y") 
                now_time = now.strftime("%H:%M:%S")  
                texts = [element.get_text(strip=True) for element in news_items]
                normal_text = ''.join(texts).replace('\n', ' ') 

                # Проверка, существует ли новость уже в базе данных
                c.execute("SELECT COUNT(*) FROM parser_db WHERE bank = ? AND title = ? AND data = ?", (name_bank, name, formatted_date))
                count_result = c.fetchone()
                count = count_result[0]
                
                if count == 0:
                    c.execute("INSERT INTO parser_db(bank, title, news, data, data_parsing, time_parsing) VALUES (?, ?, ?, ?, ?, ?)", (name_bank, name, normal_text, formatted_date, now_date, now_time))
                    db.commit()
                    print(f"Добавлена новая новость: {name} ({formatted_date})")
                else:
                    print(f"Новость уже существует в базе данных: {name} ({formatted_date})")
            else:
                print(f"Новость старше 2 лет: {formatted_date}, остановка парсинга.")
                return # Выход из цикла, так как даты будут только старее

        page += 1
    # Отправка отчета об ошибках после завершения парсинга
    if error_log:
        send_error_report(error_log)
    else:
        send_error_report(err)



    