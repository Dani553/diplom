from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
import time
import psycopg2
import os
from dotenv import load_dotenv
# Функция для подключения к БД PostgreSQL
def database_open(name_prod, stack_info, base_inf):
    load_dotenv()
    db_password = os.getenv("DB_PASSWORD")
    db_host = 'localhost'
    db_name = 'postgres'
    db_user = 'postgres'

    conn = psycopg2.connect(host=db_host, database=db_name, user=db_user, password=db_password)
    cursor = conn.cursor()
    
    database_input(name_prod, cursor, stack_info, base_inf)

    conn.commit()
    cursor.close()
    conn.close()
# Функция для вставки новых данных в таблицы соответствующих сетевых оборудований
def database_input(name_prod, cursor, stack, base_inf):
    match name_prod:
        case('Wi-Fi роутеры'):
            cursor.execute("""INSERT INTO "Характеристики Wi-Fi роутеров" ("Порты WAN/LAN", "Стандарты Wi-Fi", "Поддержка IPv6") values (%s, %s, %s)""", stack)
            cursor.execute("""SELECT "ID_характеристики" FROM "Характеристики Wi-Fi роутеров" ORDER BY "ID_характеристики" DESC LIMIT 1""")
            id = cursor.fetchall()
            base_inf+=id
            cursor.execute("""INSERT INTO "Wi-Fi роутеры" ("Ссылки", "Название", "ID_характеристики") values (%s, %s, %s)""", base_inf)
        case('Маршрутизаторы'):
            cursor.execute("""INSERT INTO "Характеристики маршрутизаторов" ("Порты WAN/LAN") values (%s)""", stack)
            cursor.execute("""SELECT "ID_характеристики" FROM "Характеристики маршрутизаторов" ORDER BY "ID_характеристики" DESC LIMIT 1""")
            id = cursor.fetchall()
            base_inf+=id
            cursor.execute("""INSERT INTO "Маршрутизаторы" ("Ссылки", "Название", "ID_характеристики") values (%s, %s, %s)""", base_inf)
        case('Внутренние точки доступа'):
            cursor.execute("""INSERT INTO "Характеристики точек доступа Wi-Fi" ("Порты WAN/LAN", "Стандарты Wi-Fi", "Размещение", "Варианты крепления") values (%s, %s, %s, %s)""", stack)
            cursor.execute("""SELECT "ID_характеристики" FROM "Характеристики точек доступа Wi-Fi" ORDER BY "ID_характеристики" DESC LIMIT 1""")
            id = cursor.fetchall()
            base_inf+=id
            cursor.execute("""INSERT INTO "Точки доступа Wi-Fi" ("Ссылки", "Название", "ID_характеристики") values (%s, %s, %s)""", base_inf)
        case('Внешние точки доступа'):
            cursor.execute("""INSERT INTO "Характеристики точек доступа Wi-Fi" ("Порты WAN/LAN", "Стандарты Wi-Fi", "Размещение", "Варианты крепления") values (%s, %s, %s, %s)""", stack)
            cursor.execute("""SELECT "ID_характеристики" FROM "Характеристики точек доступа Wi-Fi" ORDER BY "ID_характеристики" DESC LIMIT 1""")
            id = cursor.fetchall()
            base_inf+=id
            cursor.execute("""INSERT INTO "Точки доступа Wi-Fi" ("Ссылки", "Название", "ID_характеристики") values (%s, %s, %s)""", base_inf)
        case('Управляемые коммутаторы'):
            cursor.execute("""INSERT INTO "Характеристики коммутаторов" ("Порты WAN/LAN", "Уровень", "Пропускная способность(Скорость)", "Вид", "Размещение") values (%s, %s, %s, %s, %s)""", stack)
            cursor.execute("""SELECT "ID_характеристики" FROM "Характеристики коммутаторов" ORDER BY "ID_характеристики" DESC LIMIT 1""")
            id = cursor.fetchall()
            base_inf+=id
            print(base_inf)
            cursor.execute("""INSERT INTO "Коммутаторы" ("Ссылки", "Название", "ID_характеристики") values (%s, %s, %s)""", base_inf)
        case('Неуправляемые коммутаторы'):
            cursor.execute("""INSERT INTO "Характеристики коммутаторов" ("Порты WAN/LAN", "Уровень", "Пропускная способность(Скорость)", "Вид", "Размещение") values (%s, %s, %s, %s, %s)""", stack)
            cursor.execute("""SELECT "ID_характеристики" FROM "Характеристики коммутаторов" ORDER BY "ID_характеристики" DESC LIMIT 1""")
            id = cursor.fetchall()
            base_inf+=id
            cursor.execute("""INSERT INTO "Коммутаторы" ("Ссылки", "Название", "ID_характеристики") values (%s, %s, %s)""", base_inf)
        case('Серверные платформы'):
            cursor.execute("""INSERT INTO "Характеристики серверных платформ" ("Порты WAN/LAN", "Порты USB", "Процессор", "Количество процессоров", "Дисковая корзина") values (%s, %s, %s, %s, %s)""", stack)
            cursor.execute("""SELECT "ID_характеристики" FROM "Характеристики серверных платформ" ORDER BY "ID_характеристики" DESC LIMIT 1""")
            id = cursor.fetchall()
            base_inf+=id
            cursor.execute("""INSERT INTO "Серверные платформы" ("Ссылки", "Название", "ID_характеристики") values (%s, %s, %s)""", base_inf)
# Поиск на странице, содержащей сетевые оборудования основной информации: "Цена", "Название", "Ссылка"
def sniff_info_qtech(name_prode):
    time.sleep(3)
    if (name_prode=='Управляемые коммутаторы') | (name_prode=='Неуправляемые коммутаторы'):
# Поиск по CSS_SELECTOR элементов для получения данных о сетевом оборудовании
        products_page = driver.find_elements(By.CSS_SELECTOR, 'div.product-compare-section')
        for category in products_page:
            sections=category.find_elements(By.CSS_SELECTOR, 'div.product-compare-list-item')
            for section in sections:
                name=section.find_elements(By.CSS_SELECTOR, 'h3.product__title')
                name_series=section.find_elements(By.TAG_NAME, 'a')[0]
                link = name_series.get_attribute('href')
                name=name[0].text
                base_inf=[link]
# Открытие новой вкладки по полученной из CSS_SELECTOR ссылке
                driver.execute_script("window.open('{}', '_blank')".format(link))

# Переход на новую вкладку
                driver.switch_to.window(driver.window_handles[-1])
# Нажатие на найденную по надписи кнопку, для перехода к характеристикам
                wait.until(EC.visibility_of_element_located((By.LINK_TEXT, 'Характеристики'))).click()

                con_characts=driver.find_elements(By.CSS_SELECTOR, 'div.table-block')
                
                sniff_charact_qtech(name_prode, con_characts, base_inf)

                driver.close()
                driver.switch_to.window(driver.window_handles[0])
    
    elif (name_prode=='Маршрутизаторы'):
        products_page = driver.find_elements(By.CSS_SELECTOR, 'div.products-section')[:2]
        for category in products_page:
            sections=category.find_elements(By.CSS_SELECTOR, 'div.product')
            for section in sections:
                name=section.find_elements(By.CSS_SELECTOR, 'div.product__title')
                name_series=section.find_elements(By.TAG_NAME, 'a')
                link = name_series.get_attribute('href')
                name=name_series[0].text
                base_inf=[name, link]
# Открытие новой вкладки по полученной из CSS_SELECTOR ссылке
                driver.execute_script("window.open('{}', '_blank')".format(link))
# Переход на новую вкладку
                driver.switch_to.window(driver.window_handles[-1])
# Нажатие на найденную по надписи кнопку, для перехода к характеристикам
                wait.until(EC.visibility_of_element_located((By.LINK_TEXT, 'Характеристики'))).click()

                con_characts=driver.find_elements(By.CSS_SELECTOR, 'div.table-block')
                
                sniff_charact_qtech(name_prode, con_characts, base_inf)

                driver.close()
                driver.switch_to.window(driver.window_handles[0])

    elif (name_prode=='Серверные платформы') | (name_prode=='Внешние точки доступа') | (name_prode=='Внутренние точки доступа') | (name_prode=='Wi-Fi роутеры'):
        products_page = driver.find_elements(By.CSS_SELECTOR, 'div.products-section')
        for category in products_page:
            sections=category.find_elements(By.CSS_SELECTOR, 'div.product')
            for section in sections:
                name=section.find_elements(By.CSS_SELECTOR, 'div.product__title')
                name_series=section.find_elements(By.TAG_NAME, 'a')[0]
                link = name_series.get_attribute('href')
                name=name[0].text
                base_inf=[link]
# Открытие новой вкладки по полученной из CSS_SELECTOR ссылке
                driver.execute_script("window.open('{}', '_blank')".format(link))
# Переход на новую вкладку
                driver.switch_to.window(driver.window_handles[-1])
# Нажатие на найденную по надписи кнопку, для перехода к характеристикам
                wait.until(EC.visibility_of_element_located((By.LINK_TEXT, 'Характеристики'))).click()

                con_characts=driver.find_elements(By.CSS_SELECTOR, 'div.table-block')

                sniff_charact_qtech(name_prode, con_characts, base_inf)

                driver.close()
                driver.switch_to.window(driver.window_handles[0])
# Поиск на странице выбранного сетевого оборудования информации о характеристиках
def sniff_charact_qtech(name_prode, con_characts, base_inf):
    product_name=driver.find_elements(By.CSS_SELECTOR, 'div.element-title-wrap')[0]
    name=product_name.find_elements(By.CSS_SELECTOR, 'h1')[0].text
    base_inf+=[name]
    if (name_prode=='Управляемые коммутаторы'):
        ports1, speed, level, isp = ' '*4
        for container in con_characts:
            attributes=container.find_elements(By.TAG_NAME, 'tr')
            for attribute in attributes:
                characts=attribute.find_elements(By.TAG_NAME, 'td')
                match characts[0].text:
                    case('Порты 10/100/1000BASE-T PoE'):
                        ports1=characts[1].text
                        ports1=ports1.split(' ')[0]
                    case('Порты 10/100/1000BASE-T'):
                        ports1=characts[1].text
                        ports1=ports1.split(' ')[0]
                    case('Пропускная способность'):
                        speed=characts[1].text
                    case('Уровень коммутатора'):
                        level=characts[1].text
                    case('Вариант исполнения'):
                        isp=characts[1].text
        if (ports1!=' '):
            stack_info=[int(ports1), level, speed, 'управляемый', isp]
            database_open(name_prode, stack_info, base_inf)
    elif (name_prode=='Неуправляемые коммутаторы'):
        product_name=driver.find_elements(By.CSS_SELECTOR, 'div.element-title-wrap')[0]
        name=product_name.find_elements(By.CSS_SELECTOR, 'h1')[0].text
        base_inf=[name]
        ports1, speed, level, isp = ' '*4
        for container in con_characts:
            attributes=container.find_elements(By.TAG_NAME, 'tr')
            for attribute in attributes:
                characts=attribute.find_elements(By.TAG_NAME, 'td')
                match characts[0].text:
                    case('Порты 10/100BASE-T'):
                        ports1=characts[1].text
                        ports1=ports1.split(' ')[0]
                    case('Порты 10/100BASE-T PoE'):
                        ports1=characts[1].text
                        ports1=ports1.split(' ')[0]
                    case('Пропускная способность'):
                        speed=characts[1].text
                    case('Уровень коммутатора'):
                        level=characts[1].text
                    case('Вариант исполнения'):
                        isp=characts[1].text
        if ports1!=' ':
            stack_info=[int(ports1), level, speed, 'неуправляемый', isp]
            database_open(name_prode, stack_info, base_inf)
    elif (name_prode=='Маршрутизаторы'):
        all_ports=0
        ports, ports1=' '*2
        for container in con_characts:
            attributes=container.find_elements(By.TAG_NAME, 'tr')
            for attribute in attributes:
                characts=attribute.find_elements(By.TAG_NAME, 'td')
                match characts[0].text:
                    case('Порты 10/100/1000BASE-T (LAN)'):
                        ports1=characts[1].text
                        ports1=ports1.split(' ')[0]
                    case('Порты 10/100/1000BASE-T (WAN)'):
                        ports=characts[1].text
                        ports=ports.split(' ')[0]
                    case('Порты комбо 1000BASE-T\SFP (WAN)'):
                        ports=characts[1].text
                        ports=ports.split(' ')[0]
        if ports!=' ':
            all_ports+=int(ports)
        if ports1!=' ':
            all_ports+=int(ports1)
        if all_ports!=0:
            stack_info=[all_ports]
            database_open(name_prode, stack_info, base_inf)
    elif (name_prode=='Серверные платформы'):
        ports, ports21, proc, count_proc, count1, count2, count3=' '*7
        for container in con_characts:
            attributes=container.find_elements(By.TAG_NAME, 'tr')
            for attribute in attributes:
                characts=attribute.find_elements(By.TAG_NAME, 'td')
                match characts[0].text:
                    case('Порты 10/100/1000BASE-T'):
                        ports=characts[1].text
                        ports=ports.split(' ')[0]
                    case('Процессор'):
                        proc=characts[1].text
                        proc=proc.split(', ')[0]
                        proc=proc.split('* ')[1]
                    case('Количество процессоров'):
                        count_proc=characts[1].text
                    case('USB интерфейс'):
                        ports2=characts[1].text
                        ports2=ports.split(', ')
                        ports21=ports2[0]
                        ports21=ports21.split(' ')[0]
                    case('Дисковая корзина (front)'):
                        count1=(characts[1].text).split('*')
                        count1=int(count1[0])
                    case('Дисковая корзина (back)'):
                        count2=(characts[1].text).split('*')
                        if len(count2)>1:
                            count2=int(count2[0])
                            count3=count1+count2
        if (count3==' '):
            if count1!=0:    
                stack_info=[int(ports), int(ports21), proc, int(count_proc), int(count1)]
                database_open(name_prode, stack_info, base_inf)
        else:
            count3=str(count3)
            stack_info=[int(ports), int(ports21), proc, int(count_proc), int(count3)]
            database_open(name_prode, stack_info, base_inf)
    elif (name_prode=='Внешние точки доступа'):
        wan, lan, stand, var=' '*4
        for container in con_characts:
            attributes=container.find_elements(By.TAG_NAME, 'tr')
            for attribute in attributes:
                characts=attribute.find_elements(By.TAG_NAME, 'td')
                match characts[0].text:
                    case('Порты 10/100/1000BASE-T (WAN)'):
                        wan=characts[1].text
                        wan=wan.split(' ')[0]
                    case('Порты 10/100/1000/2500BASE-T (WAN)'):
                        wan=characts[1].text
                        wan=wan.split(' ')[0]
                    case('Порты 10/100/1000BASE-T'):
                        wan=characts[1].text
                        wan=wan.split(' ')[0]
                    case('Порты 10/100/1000BASE-T (LAN)'):
                        lan=characts[1].text
                        lan=lan.split(' ')[0]
                    case('Стандарт Wi-Fi'):
                        stand=characts[1].text
                    case('Варианты крепления'):
                        var=characts[1].text
        if (lan!=' '):
            if (wan!=' '):
                lan_wan=int(lan)+int(wan)
                stack_info=[lan_wan, stand, 'вне помещения', var]
                database_open(name_prode, stack_info, base_inf)
            else:
                stack_info=[int(lan), stand, 'вне помещения', var]
                database_open(name_prode, stack_info, base_inf)
        else:
            if (wan!=' '):
                stack_info=[int(wan), stand, 'вне помещения', var]
                database_open(name_prode, stack_info, base_inf)
    elif (name_prode=='Внутренние точки доступа'):
        wan, lan, stand, var=' '*4
        for container in con_characts:
            attributes=container.find_elements(By.TAG_NAME, 'tr')
            for attribute in attributes:
                characts=attribute.find_elements(By.TAG_NAME, 'td')
                match characts[0].text:
                    case('Порты 10/100/1000/2500BASE-T (LAN)'):
                        lan=characts[1].text
                        lan=lan.split(' ')[0]
                    case('Порты 10/100/1000BASE-T (LAN)'):
                        lan=characts[1].text
                        lan=lan.split(' ')[0]
                    case('Порты 10/100/1000/2500BASE-T (WAN)'):
                        wan=characts[1].text
                        wan=wan.split(' ')[0]
                    case('Порты 10/100/1000BASE-T (WAN)'):
                        wan=characts[1].text
                        wan=wan.split(' ')[0]
                    case('Стандарт Wi-Fi'):
                        stand=characts[1].text
                    case('Варианты крепления'):
                        var=characts[1].text
                        var=var.split(' (')[0]

        if (lan!=' '):
            if (wan!=' '):
                lan_wan=int(lan)+int(wan)
                stack_info=[lan_wan, stand, 'внутри помещения', var]
                database_open(name_prode, stack_info, base_inf)
            else:
                stack_info=[int(lan), stand, 'внутри помещения', var]
                database_open(name_prode, stack_info, base_inf)
        else:
            if (wan!=' '):
                stack_info=[int(wan), stand, 'внутри помещения', var]
                database_open(name_prode, stack_info, base_inf)

    elif (name_prode=='Wi-Fi роутеры'):
        all_ports=0
        wan, lan, stand, ipv6=' '*4
        for container in con_characts:
            attributes=container.find_elements(By.TAG_NAME, 'tr')
            for attribute in attributes:
                characts=attribute.find_elements(By.TAG_NAME, 'td')
                match characts[0].text:
                    case('Порты 10/100BASE-T (LAN)'):
                        lan=characts[1].text
                        lan=lan.split(' ')[0]
                    case('Порты 10/100/1000BASE-T (LAN)'):
                        lan=characts[1].text
                        lan=lan.split(' ')[0]
                    case('Порты 10/100BASE-T (WAN)'):
                        wan=characts[1].text
                        wan=wan.split(' ')[0]
                    case('Порты 10/100/1000BASE-T (WAN)'):
                        wan=characts[1].text
                        wan=wan.split(' ')[0]
                    case('Стандарт Wi-Fi'):
                        stand=characts[1].text
                    case('Сетевые протоколы'):
                        ipv6=characts[1].text
                        ipv6=ipv6.split(', ')
                        if(ipv6[0]=='IPv4/IPv6'):
                            ipv6='есть'
                        else:
                            ipv6='нет'
        
        if lan!=' ':
            if wan!=' ':
                all_ports+=int(lan)+int(wan)
                stack_info=[all_ports, stand, ipv6]
                database_open(name_prode, stack_info, base_inf)
            else:
                stack_info=[int(lan), stand, ipv6]
                database_open(name_prode, stack_info, base_inf)
        else:
            if wan!=' ':
                stack_info=[int(wan), stand, ipv6]
                database_open(name_prode, stack_info, base_inf)

try:
# Создание webdriver используя Google Chrome
    driver = webdriver.Chrome()

    wait = WebDriverWait(driver, 100)
# Получение страницы, содержащей сетевое оборудование и обращение к функции поиска основной информации о выбранном нем
    driver.get('https://www.qtech.ru/catalog/switches/access')
    sniff_info_qtech('Управляемые коммутаторы')

    driver.get('https://www.qtech.ru/catalog/switches/unmanaged/')
    sniff_info_qtech('Неуправляемые коммутаторы')

    driver.get('https://www.qtech.ru/catalog/routers_corporate_networks/')
    sniff_info_qtech('Маршрутизаторы')

    driver.get('https://www.qtech.ru/catalog/servers/servery_rossiyskogo_proizvodstva/')
    sniff_info_qtech('Серверные платформы')

    driver.get('https://www.qtech.ru/catalog/wireless/outdoor_access_points/')
    sniff_info_qtech('Внешние точки доступа')

    driver.get('https://www.qtech.ru/catalog/wireless/indoor_access_points/')
    sniff_info_qtech('Внутренние точки доступа')

    driver.get('https://www.qtech.ru/catalog/cpe/wi-fi_routers/')
    sniff_info_qtech('Wi-Fi роутеры')

    driver.quit()

except WebDriverException:
    driver.quit()