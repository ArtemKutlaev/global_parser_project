from database import clear_database
from parsing.rsb import scrape_rsb_news
from parsing.gazprombank import scrape_gazprombank_news

def parsing():
    """
    Функция одновременно запускает парсинг двух сайтов
    """
    scrape_rsb_news()
    scrape_gazprombank_news()
