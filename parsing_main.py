from database import clear_database
from parsing.rsb import scrape_rsb_news
from parsing.gazprombank import scrape_gazprombank_news

def parsing():
    #clear_database()# Очищение базы данных на всякий случай
    scrape_rsb_news()
    scrape_gazprombank_news()
parsing()