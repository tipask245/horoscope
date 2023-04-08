from bs4 import BeautifulSoup
import requests


def scrap_horoscope_by_sign_en(sign_id, interval):
    request_url = f'https://www.horoscope.com/us/horoscopes/general/horoscope-general-daily-{interval}.aspx?sign={sign_id}'
    if interval in ('weekly', 'monthly'):
        request_url = f'https://www.horoscope.com/us/horoscopes/general/horoscope-general-{interval}.aspx?sign={sign_id}'
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
    return main_horoscope.get_text(), matches_text, mood_text


def scrap_horoscope_today_by_sign_ru(sign_name):
    request_url = f'https://horo.mail.ru/prediction/{sign_name}/today/'
    page = requests.get(request_url).text
    scraper = BeautifulSoup(page, features='html.parser')
    # main_horoscope = scraper.find('div', {'class': 'article__item article__item_alignment_left article__item_html'}).text
    # matches = scraper.find('div', {'class': 'module-skin module-matches text-center'}).find_all('a')
    # matches = [match.find.text for match in matches]
    # print(matches)
