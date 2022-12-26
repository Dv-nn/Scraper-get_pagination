import requests
from bs4 import BeautifulSoup


headers = {'user-agent': ''}
url = 'https://'
response = requests.get(url, headers=headers)
print('Ответ сервера:', response.status_code)
html = response.text

soup = BeautifulSoup()
pagination = soup.find('div', class_='bx-pagination-container').find_all('li')
pages = pagination[-2].text
print('Всего страниц: ' + pages)

data = []
for page in range(1, int(pages) + 1):
    response = requests.get(url, headers=headers, params={'PAGEN_1': page})
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    blocks = soup.find('div', class_='page-content-wrapper').find_all('div', class_='b-goods-item')
    print(f'Парсинг страницы {page} из {pages}...')

    for block in blocks:
        data.append({
            'Название': block.find('div', class_='b-goods-item-link').get_text(strip=True),
            'Код товара': block.find('div', class_='info-a').text.split(' ')[-1].strip(),
            'Цена': block.find('div', class_='left').get_text(strip=True).replace('\xa0', ''),
            'Ссылка': 'https://eldvor.ru' + block.find('div', class_='b-goods-item-link').find('a').get(
                'href')
        })

print('Получили ' + str(len(data)) + ' позиций')