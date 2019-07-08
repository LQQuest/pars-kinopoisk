# -*- coding: utf-8 -*-
import urllib.request
from bs4 import BeautifulSoup
import csv


def get_url(url):

    response = urllib.request.urlopen(url)
    return response.read()


def parse(html):
    soup = BeautifulSoup(html)
    table = soup.find('table')
    projects = []
    row = table.find('tr')
    col = row.find('td', id="block_left")
    low_table = col.find('table')
    new_table = low_table.find_all('table')[2:3]
    another_table = new_table[0].find('table')

    for tr in another_table.find_all('tr')[1:]:
        cols = tr.find_all('td')
        span = cols[1].find('span', class_="text-grey")

        if not span is None:
            projects.append({
                'Ru_title': cols[1].a.text,
                'Eng_title': span.text,
                'Rate': cols[2].find('div').a.text
            })
        else:
            projects.append({
                'Ru_title': cols[1].a.text,
                'Eng_title': "-",
                'Rate': cols[2].find('div').a.text
            })

    return projects


def save(projects, path):
    with open(path, 'w', encoding="utf-8") as csvfile:
        writen = csv.writer(csvfile)
        writen.writerow(('Русское название', 'Английское название', 'Рейтинг'))

        for project in projects:
            writen.writerow((project['Ru_title'], project['Eng_title'], project['Rate']))


def main():
    save(parse(get_url("https://www.kinopoisk.ru/top/")), 'projects.csv')


if __name__ == '__main__':
    main()