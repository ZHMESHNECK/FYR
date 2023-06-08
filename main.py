from fake_useragent import UserAgent
import requests
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from selenium import webdriver

# парсинг rieltor.ua


def call_data_rieltor():

    ua = UserAgent()
    city = 'kiev'
    price_min = ''
    price_max = ''
    sort = "byprice"

    room = ''

    params = {
        "price_min": price_min,
        "price_max": price_max,
        "sort": sort
    }

    url = 'https://rieltor.ua/{}/flats-rent/{}'.format(city, room)

    data = []

    response = requests.get(
        url=url,
        headers={'user-agent': f'{ua.random}'},
        params=params
    )

    # записываем страницу в файл
    # with open('text.html', 'w', encoding='utf-8') as file:
    #     file.write(response.text)

    # читаем страницу с файла
    # with open('text.html', encoding='utf-8') as file:
    #     response = file.read()

    soup = BeautifulSoup(response.text, 'lxml')
    mdiv = soup.find_all(class_='catalog-card')
    dublicate = []

    # 8 объявлений
    for div in mdiv[:8]:
        try:
            price = div.find('div', class_='catalog-card-price').text.strip()
        except:
            price = 'No price'
        try:
            addres = div.find('div', class_="catalog-card-address").text
        except:
            addres = 'No address'
        try:
            link = div.find('a', class_='catalog-card-media').get('href')
        except:
            link = 'No link'
        try:
            area = div.find(
                'div', class_='catalog-card-region').find_all('a')[1].text.strip()
        except:
            area = 'No area'

        if addres not in dublicate:
            data.append(
                {
                    "Цена": price,
                    "Район": area,
                    "Адрес": addres,
                    "Ссылка": link,
                }
            )
            dublicate.append(addres)
    return data

    # with open('data.json', 'w', encoding='utf-8') as file:
    #     json.dump(data, file, indent=4, ensure_ascii=False)


def call_data_olx():

    options = Options()
    options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
    options.add_argument('--headless')

    driver = webdriver.Firefox(options=options)

    url = f'https://www.olx.ua/d/uk/nedvizhimost/kvartiry/dolgosrochnaya-arenda-kvartir/?currency=UAH&search%5Border%5D=filter_float_price:asc'

    try:
        driver.get(url=url)

        # with open("index2.html", 'w', encoding='utf-8') as file:
        #     file.write(driver.page_source)
    except Exception as _ex:
        print(_ex)
    finally:
        driver.close()
        driver.quit()

    response = requests.get(
        url=url
    )
    
    with open("index.html",'w',encoding='utf-8') as file:
        file.write(response.text)

    pull_olx()

def pull_olx():
    pass


def main():
    # call_data_rieltor()
    call_data_olx()


if __name__ == '__main__':
    main()
