from bs4 import BeautifulSoup
import requests
from datetime import datetime


def scrap_horoscope_by_sign_num_en(sign_num: int, interval: str):
    request_url = f'https://www.horoscope.com/us/horoscopes/general/horoscope-general-daily-{interval}.aspx?sign={sign_num}'
    if interval in ('weekly', 'monthly'):
        request_url = f'https://www.horoscope.com/us/horoscopes/general/horoscope-general-{interval}.aspx?sign={sign_num}'
    page = requests.get(request_url).text
    scraper = BeautifulSoup(page, features='html.parser')
    main_horoscope = scraper.find('div', {'class': 'main-horoscope'}).find('p')
    if main_horoscope.select_one('a'):
        main_horoscope.select_one('a').decompose()
    for br in main_horoscope.find_all('br'):
        br.replace_with('\n')
    matches = scraper.find('div', {'class': 'module-skin module-matches text-center'}).find_all('a')
    matches_text = '*Matches*\n'
    for match in matches:
        matches_text += f'{match.find("h4").text} - {match.find("p").text}\n'
    mood_blocks = scraper.find('div', {'class': 'ratings flex-center-inline'}).find_all('a')
    mood_text = '*Mood*\n'
    for block in mood_blocks:
        title = block.find('h4').text
        rating = len(block.find_all('i', {'class': 'icon-star-filled highlight'}))
        mood_text += f'{title} - {rating}\n'
    return main_horoscope.text, matches_text, mood_text


def scrap_horoscope_by_sign_name_ru(sign_name: str, interval: str):
    request_url = f'https://www.thevoicemag.ru/horoscope/daily/{sign_name.lower()}/{interval}/'
    today = datetime.today().strftime("%d-%m-%Y")
    if interval == today:
        request_url = f'https://www.thevoicemag.ru/horoscope/daily/{sign_name.lower()}/'
    page = requests.get(request_url).text
    scraper = BeautifulSoup(page, features='html.parser')
    date = scraper.find('div', {'class': 'sign__description-date'}).find_all('span')
    date = ' '.join([span.text for span in date])
    main_horoscope = scraper.find('div', {'class': 'sign__description-text'}).text
    return date, main_horoscope


def scrap_ch_horoscope_by_sign_num_en(sign_num: int, interval: str):
    request_url = f'https://www.horoscope.com/us/horoscopes/chinese/horoscope-chinese-daily-{interval}.aspx?sign={sign_num}'
    if interval in ('weekly', 'monthly'):
        request_url = f'https://www.horoscope.com/us/horoscopes/chinese/horoscope-chinese-{interval}.aspx?sign={sign_num}'
    print(request_url)
    page = requests.get(request_url).text
    scraper = BeautifulSoup(page, features='html.parser')
    main_horoscope = scraper.find('div', {'class': 'main-horoscope'}).find('p')
    for br in main_horoscope.find_all('br'):
        br.replace_with('\n')
    return main_horoscope.text


def scrap_ch_horoscope_by_sign_name_ru(sign_name: str, interval: str):
    names = {'Monkey': 'monk', 'Rooster': 'cock', 'Rabbit': 'hare'}
    request_url = f'https://orakul.com/horoscope/chinese/general/{names[sign_name] if sign_name in names else sign_name}/{interval}.html'
    page = requests.get(request_url).text
    scraper = BeautifulSoup(page, features='html.parser')
    title = scraper.find('h2', {'class': 'typehead'}).text.strip()
    main_horoscope = scraper.find('div', {'class': 'horoBlock'}).text.strip()
    return title, main_horoscope
