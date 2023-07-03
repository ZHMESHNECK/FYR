from fake_useragent import UserAgent
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup


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

        # проверка браузера на совместимость с сайтом
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "c-wrapper-inside")))
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
            area = item.find('p', class_='css-veheph er34gjf0').text.split('-')
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
