import os

import requests
from bs4 import BeautifulSoup
import lxml

URL = 'https://volpi.ru/timetable'


def get_html(url):
    html_text = requests.get(url).text
    return html_text


def get_links():
    html = get_html(URL)
    soup = BeautifulSoup(html, 'lxml')
    main_content = soup.find(class_='main-content')
    tables = main_content.find_all(class_='timetable-list')[:2]
    all_links = []

    # Проходим по каждому элементу ttable-row
    for schedule in tables:
        # Находим все элементы ttable-elem внутри текущего элемента ttable-row
        schedule_elements = schedule.find_all(class_='ttable-elem')
        # Проходим по каждому элементу ttable-elem
        for element in schedule_elements:
            # Находим все ссылки внутри текущего элемента ttable-elem
            links = element.find_all('a', href=True)
            # Добавляем найденные ссылки в список all_links
            for link in links:
                all_links.append('volpi.ru' + link['href'])

    all_links = list(set(all_links))
    return all_links


def download_pdf(links: list[str]):
    for link in links:
        r = requests.get(link)
        filename = link.split('/')[-1]
        with open(f'static/schedule/schedule_pdf/{filename}.pdf', 'wb') as f:
            f.write(r.content)
    print('OK')

download_pdf(get_links())
