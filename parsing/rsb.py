from email.mime.text import MIMEText
import smtplib
import fake_useragent
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re
from database import c, db, clear_database

url = 'https://www.rsb.ru/press-center/news/2024/'
url_main = 'https://www.rsb.ru'
name_bank = 'Банк Русский Стандарт'
error_log = []
err = "Ошибок при парсинге Банка Русский Стандарт не обнаружено"

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


def scrape_rsb_news():
    # Создание fake useragent, чтобы избегать ошибки <Response [403]>
    random_user_agent = fake_useragent.UserAgent().random
    header = {'user-agent': random_user_agent}

    # Получение ответа от сайта
    response = requests.get(url, headers=header)

    # Проверка на успешный ответ
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Получаем все блоки новостей
        news_items = soup.find_all('div', class_='info-block__date-item')

        # Определяем дату 720 дней назад
        days_ago = datetime.now() - timedelta(days=720)
        for item in news_items:
            data = item.find('time').text.strip()
            news_date = datetime.strptime(data, '%d.%m.%Y')  # Предполагаем, что дата в формате 'дд.мм.гггг'
        
            # Проверяем, если новость за последние 720 дней
            if news_date >= days_ago:
                # Получаем заголовок новости и ссылку
                title_link = item.find('a', class_='info-block__date-item-link').text.strip()
                href = item.find('a', class_='info-block__date-item-link')['href']  # Извлечение href
                #формирование ссылки на саму новость
                href_real = url_main + href
                #Получение из нее текста
                response_text = requests.get(href_real, headers=header)
                #Узнаем время и дату парсинга
                now = datetime.now()
                formatted_date = now.strftime("%d.%m.%Y")
                formatted_time = now.strftime("%H:%M:%S")
                soup_text = BeautifulSoup(response_text.text, 'html.parser')
                text_news = soup_text.find('div', class_ = 'detail_text press_detail_text').text.strip()
                text_news = re.sub(r'\s+', ' ', text_news)

                # Проверка наличия новости в БД
                c.execute("SELECT COUNT(*) FROM parser_db WHERE bank = ? AND title = ? AND data = ?", (name_bank, title_link, data))
                result = c.fetchone()
                count = result[0]  # Получаем количество записей с таким bank, title и data

                if count == 0:  # Если такой записи нет
                    c.execute("INSERT INTO parser_db(bank, title, news, data, data_parsing, time_parsing) VALUES (?, ?, ?, ?, ?, ?)", (name_bank, title_link, text_news, data, formatted_date, formatted_time, ))
                    db.commit()
                    print(f"Добавлена новость: {title_link} ({data})")  # Сообщение о добавлении
                else:
                    print(f"Новость уже существует в базе: {title_link} ({data})")  # Сообщение, что новость уже есть
    else:
        print(f"Ошибка при запросе страницы: {response.status_code}")
        error_log.append(f"{name_bank}Ошибка при запросе страницы")
    
    if error_log:
        send_error_report(error_log)
    else:
        send_error_report(err)

if __name__ == '__main__':
    scrape_rsb_news()
    db.close()
