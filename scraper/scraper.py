from bs4 import BeautifulSoup
import requests


def scrap_horoscope_today_by_sign(sign_id):
    request_url = f'https://www.horoscope.com/us/horoscopes/general/horoscope-general-daily-today.aspx?sign={sign_id}'
    page = requests.get(request_url).text
    print(page)
    scraper = BeautifulSoup(page, features='html.parser')
