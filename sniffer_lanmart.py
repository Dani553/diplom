from selenium import webdriver
from selenium.webdriver.common.by import By
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
        case('Беспроводные маршрутизаторы'):
            cursor.execute("""INSERT INTO "Характеристики Wi-Fi роутеров" ("Порты WAN/LAN", "Стандарты Wi-Fi", "Скорость передачи", "Поддержка IPv6") values (%s, %s, %s, %s)""", stack)
            cursor.execute("""SELECT "ID_характеристики" FROM "Характеристики Wi-Fi роутеров" ORDER BY "ID_характеристики" DESC LIMIT 1""")
            id = cursor.fetchall()
            base_inf+=id
            cursor.execute("""INSERT INTO "Wi-Fi роутеры" ("Название", "Ссылки", "Цена", "ID_характеристики") values (%s, %s, %s, %s)""", base_inf)
        case('Маршрутизаторы'):
            cursor.execute("""INSERT INTO "Характеристики маршрутизаторов" ("Порты WAN/LAN", "Поддержка IPv6") values (%s, %s)""", stack)
            cursor.execute("""SELECT "ID_характеристики" FROM "Характеристики маршрутизаторов" ORDER BY "ID_характеристики" DESC LIMIT 1""")
            id = cursor.fetchall()
            base_inf+=id
            cursor.execute("""INSERT INTO "Маршрутизаторы" ("Название", "Ссылки", "Цена", "ID_характеристики") values (%s, %s, %s, %s)""", base_inf)
        case('Коммутаторы'):
            cursor.execute("""INSERT INTO "Характеристики коммутаторов" ("Порты WAN/LAN", "Уровень", "Пропускная способность(Скорость)", "Размещение") values (%s, %s, %s, %s)""", stack)
            cursor.execute("""SELECT "ID_характеристики" FROM "Характеристики коммутаторов" ORDER BY "ID_характеристики" DESC LIMIT 1""")
            id = cursor.fetchall()
            base_inf+=id
            cursor.execute("""INSERT INTO "Коммутаторы" ("Название", "Ссылки", "Цена", "ID_характеристики") values (%s, %s, %s, %s)""", base_inf)

# Поиск на странице, содержащей сетевые оборудования основной информации: "Цена", "Название", "Ссылка"
def sniff_info_lanmart(name_prode):
    products = driver.find_elements(By.CSS_SELECTOR, 'div.item-area')[:10]

    for product in products:
# Поиск по CSS_SELECTOR элементов для получения данных о сетевом оборудовании
        name_att = product.find_elements(By.CSS_SELECTOR, 'div.details-area')
        name_prod = product.find_elements(By.CSS_SELECTOR, 'h2.product-name')[0]
        name=name_prod.text
        name_att = name_prod.find_elements(By.CSS_SELECTOR, 'a')[0]
        link = name_att.get_attribute('href')
        price = product.find_elements(By.CSS_SELECTOR, 'span.price')[0]
        price=price.text

        base_inf=[name, link, price]
# Открытие новой вкладки по полученной из CSS_SELECTOR ссылке
        driver.execute_script("window.open('{}', '_blank')".format(link))

# Переход на новую вкладку
        driver.switch_to.window(driver.window_handles[-1])
# Установка времени сна, для того, чтобы страница успела прогрузиться, до того как в ней будет происходить поиск
        time.sleep(4)

        dop_inf=driver.find_elements(By.CSS_SELECTOR, 'div.product-tabs.horizontal')[0]
# Нажатие на найденную по надписи кнопку, для перехода к характеристикам
        expand_all_button = dop_inf.find_elements(By.LINK_TEXT, 'ДОПОЛНИТЕЛЬНАЯ ИНФОРМАЦИЯ')[0]
        expand_all_button.click()
        expand_all_button.click()

        characts = dop_inf.find_elements(By.CSS_SELECTOR, 'table#product-attribute-specs-table.data-table')[0]

        characts=characts.find_elements(By.TAG_NAME, 'tr')
        
        sniff_dop_charact_lanmart(name_prode, characts, base_inf)
        
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
# Поиск на странице выбранного сетевого оборудования информации о характеристиках
def sniff_dop_charact_lanmart(name_prode, connection_type, base_inf):
    count_set, stand, speed, ipv6=' '*4
    if (name_prode=='Беспроводные маршрутизаторы'):
        for i in range(len(connection_type)):

            charact=connection_type[i]
            charact_att=charact.find_elements(By.TAG_NAME, 'th')[0].text
            charact_val=charact.find_elements(By.TAG_NAME, 'td')[0].text

            match charact_att:
                case ('Сетевые порты'):
                    count_set=charact_val
                    count_set=count_set.split(' ')
                    count_set=count_set[0].replace('x', '')
                    if (count_set=='10/100'):
                        count_set=1
                case ('Скорости передачи данных'):
                    speed=charact_val.split(' ')
                    if (speed[1]=='Мбит/с'):
                        speed=speed[0]+' '+speed[1]+', '+speed[3]+' '+speed[4]
                    else:
                        speed=speed[1]+' '+speed[2]
                case ('Встроенный Wireless'):
                    stand=charact_val.split(' ')
                    standa=stand[0]
                    if(standa=='2,4') | (standa=='2.4'):
                        if (len(stand)>5):
                            stand=stand[2]+', '+stand[5]
                        else:
                            stand=stand[2]
                    elif(standa=='802.11'):
                        stand=stand[0]+' '+stand[1]
                    elif(standa=='IEEE'):
                        stand=stand[1]+' '+stand[2]+', '+stand[5]+' '+stand[6]
                    else:
                        stand=stand[0]
                case ('Службы'):
                    ipv6=charact_val
                    ipv6_list=ipv6.split(', ')
                    for i in ipv6_list:
                        if(i=='IPv6'):
                            ipv6='есть'
                    if(ipv6!='есть'):
                        ipv6='нет'

        if count_set!=' ':
            stack=[int(count_set), stand, speed, ipv6]
            database_open(name_prode, stack, base_inf)

    elif (name_prode=='Маршрутизаторы'):
            ports, ipv6=' '*2
            for i in range(len(connection_type)):

                charact=connection_type[i]
                try:
                    charact_att=charact.find_elements(By.CSS_SELECTOR, 'th.label')[0].text
                    charact_val=charact.find_elements(By.TAG_NAME, 'td')[0].text

                    match charact_att:
                            case('Сетевые порты'):
                                ports=charact_val
                                ports=ports.split(' ')[0]
                            case ('Службы'):
                                ipv6=charact_val
                                ipv6_list=ipv6.split(', ')
                                for i in ipv6_list:
                                    if(i=='IPv6'):
                                        ipv6='есть'
                                if(ipv6!='есть'):
                                    ipv6='нет'

                except IndexError:
                    pass

            if ports!=' ':
                stack=[int(ports), ipv6]
                database_open(name_prode, stack, base_inf)
    elif (name_prode=='Коммутаторы'):
            ports, speed, level, size=' '*4
            for i in range(len(connection_type)):

                charact=connection_type[i]
                try:
                    charact_att=charact.find_elements(By.CSS_SELECTOR, 'th.label')[0].text
                    charact_val=charact.find_elements(By.TAG_NAME, 'td')[0].text

                    match charact_att:
                            case('Сетевые порты'):
                                ports=charact_val
                                ports=ports.split(' ')[0]
                                ports=ports.replace('x', '')
                            case('Наличие Гигабитного порта'):
                                nal=charact_val
                                if (nal=='ДА'):
                                    speed='1 Гб'
                            case('Коммутатор уровня'):
                                level=charact_val
                            case('Исполнение'):
                                isp=charact_val

                except IndexError:
                    pass
            if (ports!=' '):
                stack=[int(ports), level, speed, isp]
                database_open(name_prode, stack, base_inf)
try:
# Создание webdriver используя Google Chrome
    driver = webdriver.Chrome()

# Получение страницы, содержащей Wi-Fi роутеры и обращение к функции поиска основной информации о выбранном сетевом оборудовании
    driver.get('https://www.lanmart.ru/besprovodnye-marshrutizatory-4.html?limit=all')
    sniff_info_lanmart('Беспроводные маршрутизаторы')

    driver.get('https://www.lanmart.ru/marshrutizatory.html')
    sniff_info_lanmart('Маршрутизаторы')

    driver.get('https://www.lanmart.ru/kommutatory-tp-link.html')
    sniff_info_lanmart('Коммутаторы')
# Закрытие webdriver
    driver.quit()

except WebDriverException:
    driver.quit()