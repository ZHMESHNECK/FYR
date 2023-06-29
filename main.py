from fake_useragent import UserAgent
import requests
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

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

    data_rieltor = []

    response = requests.get(
        url=url,
        headers={'user-agent': f'{ua.random}'},
        params=params
    )

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
            data_rieltor.append(
                {
                    "Цена": price,
                    "Район": area,
                    "Адрес": addres,
                    "Ссылка": link,
                }
            )
            dublicate.append(addres)
    return data_rieltor


# парсинг olx

def call_data_olx():

    ua = UserAgent()
    options = Options()
    options.set_preference("general.useragent.override", f'{ua.random}')
    options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
    options.add_argument('--headless')

    driver = webdriver.Firefox(options=options)

    url = f'https://www.olx.ua/d/uk/nedvizhimost/kvartiry/dolgosrochnaya-arenda-kvartir/?currency=UAH&search%5Border%5D=filter_float_price:asc'

    # Читаем страницу olx
    try:
        driver.get(url=url)
        time.sleep(8)
        ## проверка браузера на совместимость с сайтом
        try:
            da = driver.find_element(
                By.CLASS_NAME, "c-container__title").text == 'Ми великі шанувальники вінтажних речей, але ваш браузер занадто старомодний'
            if da:
                return 'Old version'
        except:
            pass
    except Exception as _ex:
        print(_ex)
    finally:
        # ищем объявления
        soup = BeautifulSoup(driver.page_source, 'lxml')

        # 8 объявлений без "рекламы"
        items_divs = soup.find_all('div', class_='css-1sw7q4x')[3:11]
        driver.close()
        driver.quit()

    data_olx = []
    for item in items_divs:
        try:
            price = item.find('p', class_='css-10b0gli er34gjf0').text
        except:
            price = 'No price'
        try:
            addres = item.find('div', class_="css-u2ayx9").find('h6').text
        except:
            addres = 'No address'
        try:
            link = item.find('a').get('href')
        except:
            link = 'no url'
        try:
            area = item.find('p', class_='css-veheph er34gjf0').text.split()
        except:
            area = 'No area'

        data_olx.append(
            {
                "Цена": price,
                "Район": area[0],
                "Название": addres,
                "Ссылка": f'https://www.olx.ua{link}',
            }
        )
    return data_olx


# def main():
#     call_data_rieltor()
#     call_data_olx()


# if __name__ == '__main__':
#     main()
