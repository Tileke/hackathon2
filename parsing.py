import requests
from bs4 import BeautifulSoup as BS
import csv

def get_html(url):
    response = requests.get(url)
    return response.text

def get_soup(html):
    soup = BS(html, 'lxml')
    return soup

def get_data(soup):
    catalog = soup.find('div', class_='search-results-table')
    cars = catalog.find_all('div', class_='list-item list-label')
    for car in cars:
        try:
            title = car.find('h2', class_='name').text.strip()
        except AttributeError:
            title = ''
        try:
            price = car.find('div', class_='block price').text.strip().split('\n')
            price = [i.strip() for i in price][:-1]
            price = '\n'.join([i for i in price if i])
        except AttributeError:
            price = ''
        try:
            image = car.find_all('img', class_='lazy-image')
            image = '\n'.join([img.get('data-src') for img in image])
        except AttributeError:
            image = ''
        try:
            description = car.find('div', class_='block info-wrapper item-info-wrapper').text.strip().split('\n')
            description = [i.strip() for i in description]
            description = ', '.join([i for i in description if i])
        except AttributeError:
            description = ''
        write_csv({
            'title': title,
            'price': price,
            'description': description,
            'image': image
        })

def write_csv(data):
    with open('cars.csv', 'a') as file:
        names = ['title', 'price', 'description', 'image']
        write = csv.DictWriter(file, delimiter='\n', fieldnames=names)
        write.writerow(data)

def main():
    try:
        for i in range(1,1050):
            BASE_URL = f'https://www.mashina.kg/search/all/?page={i}'
            html = get_html(BASE_URL)
            soup = get_soup(html)
            get_data(soup)
            print(f'Вы спарсили {i} страницу')
    except AttributeError:
        print('Конец! Это была последняя страница')

if __name__ == '__main__':
    main()


