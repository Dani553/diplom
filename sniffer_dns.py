from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
import time
import psycopg2
import os
from dotenv import load_dotenv

def database_open(name_prod, stack_info, base_inf):
    load_dotenv()
    db_password = os.getenv("DB_PASSWORD")
    conn = psycopg2.connect(dbname='postgres', user='postgres', 
                        password=db_password, host='localhost')
    cursor = conn.cursor()
    
    database_input(name_prod, cursor, stack_info, base_inf)

    conn.commit()
    cursor.close()
    conn.close()

def database_input(name_prod, cursor, stack, base_inf):
    match name_prod:
        case('Wi-Fi роутеры'):
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
        case('Точки доступа Wi-Fi'):
            cursor.execute("""INSERT INTO "Характеристики точек доступа Wi-Fi" ("Порты WAN/LAN", "Стандарты Wi-Fi", "Размещение", "Варианты крепления") values (%s, %s, %s, %s)""", stack)
            cursor.execute("""SELECT "ID_характеристики" FROM "Характеристики точек доступа Wi-Fi" ORDER BY "ID_характеристики" DESC LIMIT 1""")
            id = cursor.fetchall()
            base_inf+=id
            cursor.execute("""INSERT INTO "Точки доступа Wi-Fi" ("Название", "Ссылки", "Цена", "ID_характеристики") values (%s, %s, %s, %s)""", base_inf)
        case('Коммутаторы'):
            cursor.execute("""INSERT INTO "Характеристики коммутаторов" ("Порты WAN/LAN", "Уровень", "Пропускная способность(Скорость)", "Вид", "Размещение") values (%s, %s, %s, %s, %s)""", stack)
            cursor.execute("""SELECT "ID_характеристики" FROM "Характеристики коммутаторов" ORDER BY "ID_характеристики" DESC LIMIT 1""")
            id = cursor.fetchall()
            base_inf+=id
            cursor.execute("""INSERT INTO "Коммутаторы" ("Название", "Ссылки", "Цена", "ID_характеристики") values (%s, %s, %s, %s)""", base_inf)
        case('Шкафы и стойки'):
            cursor.execute("""INSERT INTO "Характеристики шкафов" ("Установка", "Число секций", "Защита", "Высота", "Тип шкафа") values (%s, %s, %s, %s, %s)""", stack)
            cursor.execute("""SELECT "ID_характеристики" FROM "Характеристики шкафов" ORDER BY "ID_характеристики" DESC LIMIT 1""")
            id = cursor.fetchall()
            base_inf+=id
            cursor.execute("""INSERT INTO "Шкафы и стойки" ("Название", "Ссылки", "Цена", "ID_характеристики") values (%s, %s, %s, %s)""", base_inf)
        case('Сетевые хранилища'):
            cursor.execute("""INSERT INTO "Характеристики сетевых хранилищ" ("Количество отсеков", "Максимально поддерживаемый объем", "Количество портов Ethernet") values (%s, %s, %s)""", stack)
            cursor.execute("""SELECT "ID_характеристики" FROM "Характеристики сетевых хранилищ" ORDER BY "ID_характеристики" DESC LIMIT 1""")
            id = cursor.fetchall()
            base_inf+=id
            cursor.execute("""INSERT INTO "Сетевые хранилища" ("Название", "Ссылки", "Цена", "ID_характеристики") values (%s, %s, %s, %s)""", base_inf)


def sniff_info_dns(name_prod):
    main = []

    # if (name_prod=='Шкафы и стойки'):
    #     for i in range(7):
    #         time.sleep(5)
    #         try:
    #             driver.find_elements(By.CSS_SELECTOR, 'button.pagination-widget__show-more-btn')[0].click()
    #         except IndexError:
    #             pass
    # elif (name_prod=='Сетевые хранилища'):
    #     for i in range(6):
    #         time.sleep(5)
    #         try:
    #             driver.find_elements(By.CSS_SELECTOR, 'button.pagination-widget__show-more-btn')[0].click()
    #         except IndexError:
    #             pass
    # else:
    #     while(driver.find_elements(By.CSS_SELECTOR, 'button.pagination-widget__show-more-btn')):
    #         time.sleep(5)
    #         try:
    #             driver.find_elements(By.CSS_SELECTOR, 'button.pagination-widget__show-more-btn')[0].click()
    #         except IndexError:
    #             pass
    
    products = driver.find_elements(By.CSS_SELECTOR, 'div.catalog-product.ui-button-widget')[:10]

    for product in products:
        name_element = product.find_element(By.CSS_SELECTOR, 'a.catalog-product__name.ui-link.ui-link_black')
        link = name_element.get_attribute('href')
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.product-buy__price')))
        price_element = product.find_element(By.CSS_SELECTOR, 'div.product-buy__price')
        price = price_element.text

        driver.execute_script("window.open('{}', '_blank')".format(link))

        # Switch to the new tab
        driver.switch_to.window(driver.window_handles[-1])

        time.sleep(2)
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'h1.product-card-top__title')))
        name = driver.find_element(By.CSS_SELECTOR, 'h1.product-card-top__title').text

        expand_all_button = driver.find_element(By.CSS_SELECTOR, 'button.button-ui.button-ui_white.product-characteristics__expand')
        expand_all_button.click()

        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.product-characteristics-content')))
        time.sleep(2)
        connection_type_element = driver.find_element(By.CSS_SELECTOR, 'div.product-characteristics-content')
        connection_type = connection_type_element.text
        connection_type = connection_type.split("\n")

        base_inf=[name, link, price]

        sniff_charact_dns(name_prod, connection_type, base_inf)

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    return main

def sniff_charact_dns(name_prode, connection_type, base_inf):
    
    if (name_prode=='Wi-Fi роутеры'):
        lan, stand, speed, ipv6=' '*4
        for i in range(len(connection_type)):
            
            match connection_type[i]:
                case('Количество LAN портов'):
                    lan=connection_type[i+1]
                case('Стандарт Wi-Fi'):
                    stand=connection_type[i+1]
                    stand=stand.split(' ')[1]
                    stand=stand[1:8]
                case('Скорость передачи по проводному подключению'):
                    speed=connection_type[i+1]
                case('Поддержка IPv6'):
                    ipv6=connection_type[i+1]

        if lan!=" ":
            stack_info=[lan, stand, speed, ipv6]

            database_open(name_prode, stack_info, base_inf)
    
    elif (name_prode=='Маршрутизаторы'):
        lan, wan, lan_wan, ipv6 = ' '*4
        all_ports=0
        for i in range(len(connection_type)):
        
            match connection_type[i]:
                case('Количество/скорость LAN портов'):
                    lan_count_speed=connection_type[i+1].split('x')
                    lan=lan_count_speed[0]
                case('Количество/скорость WAN портов'):
                    wan_count_speed=connection_type[i+1].split('x')
                    wan=wan_count_speed[0]
                case('Количество/скорость настраиваемых WAN/LAN'):
                    if(len(connection_type[i+1].split('х'))>1):
                        lan_wan_count_speed=connection_type[i+1].split('х')
                        lan_wan=lan_wan_count_speed[0]
                    else:
                        lan_wan_count_speed=connection_type[i+1].split('x')
                        lan_wan=lan_wan_count_speed[0]
                case('Поддержка IPv6'):
                    ipv6=connection_type[i+1]

        if lan!=" ":
            all_ports+=int(lan)
        if wan!=" ":
            all_ports+=int(wan)
        if lan_wan!=" ":
            all_ports+=int(lan_wan)

        if all_ports!=0:
            stack_info=[str(all_ports), ipv6]

            database_open(name_prode, stack_info, base_inf)

    if (name_prode=='Точки доступа Wi-Fi'):
        lan, stand, razm, setup = ' '*4
        for i in range(len(connection_type)):
        
            match connection_type[i]:
                case('Количество портов Ethernet'):
                    lan=connection_type[i+1]
                case('Стандарт Wi-Fi'):
                    stand=connection_type[i+1]
                    stand=stand.split(' ')[1]
                    stand=stand[1:8]
                case('Размещение'):
                    razm=connection_type[i+1]
                case('Установка'):
                    setup=connection_type[i+1]

        if lan!=" ":
            stack_info=[lan, stand, razm, setup]

            database_open(name_prode, stack_info, base_inf)

    if(name_prode=='Коммутаторы'):
        level, speed, vid, razm, all_ports=' '*5
        for i in range(len(connection_type)):
        
            match connection_type[i]:
                case('Уровень коммутатора'):
                    level=connection_type[i+1]
                case('Базовая скорость передачи данных'):
                    speed=connection_type[i+1]
                case('Внутренняя пропускная способность'):
                    speed=connection_type[i+1]
                case('Вид'):
                    vid=connection_type[i+1]
                case('Размещение'):
                    razm=connection_type[i+1]
                case('Общее количество портов коммутатора'):
                    all_ports=connection_type[i+1]

        if all_ports!=" ":
            stack_info=[all_ports, level, speed, vid, razm]

            database_open(name_prode, stack_info, base_inf)

    if(name_prode=='Шкафы и стойки'):
        yst, count, defen, height, type = ' '*5
        for i in range(len(connection_type)):
        
            match connection_type[i]:
                case('Установка'):
                    yst=connection_type[i+1]
                case('Число секций'):
                    count=connection_type[i+1]
                case('Защита'):
                    defen=connection_type[i+1]
                case('Высота'):
                    height=connection_type[i+1]
                    height=height.split(' ')[0]
                case('Тип'):
                    type=connection_type[i+1]

        if count!=" ":
            stack_info=[yst, count, defen, height, type]

            database_open(name_prode, stack_info, base_inf)

    if(name_prode=='Сетевые хранилища'):
        count_nakop, max, count, speed = ' '*4
        for i in range(len(connection_type)):
        
            match connection_type[i]:
                case('Количество отсеков для накопителей'):
                    count_nakop=connection_type[i+1]
                    count_nakop=count_nakop.split(' ')[0]
                case('Максимально поддерживаемый объем одного накопителя'):
                    max=connection_type[i+1]
                    max=max.split(' ')[0]
                case('Количество портов Ethernet'):
                    count=connection_type[i+1]
                    count=count.split(' ')[0]

        if max!=" ":
            stack_info=[count_nakop, max, count]

            database_open(name_prode, stack_info, base_inf)

driver = webdriver.Chrome()

try:
    driver.get('https://www.dns-shop.ru/')

    wait = WebDriverWait(driver, 100)
    # network_equipment_link = wait.until(EC.visibility_of_element_located((By.LINK_TEXT, 'Сетевое оборудование')))
    # network_equipment_link.click()

    # wait.until(EC.visibility_of_element_located((By.LINK_TEXT, 'Wi-Fi роутеры и оборудование для малых сетей'))).click()
    # wait.until(EC.visibility_of_element_located((By.LINK_TEXT, 'Wi-Fi роутеры'))).click()

    # sniff_info_dns('Wi-Fi роутеры')

    # driver.back()
    # wait.until(EC.visibility_of_element_located((By.LINK_TEXT, 'Маршрутизаторы'))).click()

    # sniff_info_dns('Маршрутизаторы')

    # driver.back()

    # wait.until(EC.visibility_of_element_located((By.LINK_TEXT, 'Wi-Fi оборудование'))).click()
    # wait.until(EC.visibility_of_element_located((By.LINK_TEXT, 'Точки доступа Wi-Fi'))).click()

    # sniff_info_dns('Точки доступа Wi-Fi')

    # driver.get('https://www.dns-shop.ru/')

    # network_equipment_link = wait.until(EC.visibility_of_element_located((By.LINK_TEXT, 'Сетевое оборудование')))
    # network_equipment_link.click()

    # wait.until(EC.visibility_of_element_located((By.LINK_TEXT, 'Профессиональное сетевое оборудование'))).click()
    # wait.until(EC.visibility_of_element_located((By.LINK_TEXT, 'Коммутаторы'))).click()

    # sniff_info_dns('Коммутаторы')

    # driver.back()

    # wait.until(EC.visibility_of_element_located((By.LINK_TEXT, 'Коммутационные шкафы и стойки'))).click()
    # wait.until(EC.visibility_of_element_located((By.LINK_TEXT, 'Коммутационные и серверные шкафы'))).click()

    # sniff_info_dns('Шкафы и стойки')

    driver.get('https://www.dns-shop.ru/')
    network_equipment_link = wait.until(EC.visibility_of_element_located((By.LINK_TEXT, 'ПК, ноутбуки, периферия')))
    network_equipment_link.click()

    wait.until(EC.visibility_of_element_located((By.LINK_TEXT, 'Периферия и аксессуары'))).click()
    wait.until(EC.visibility_of_element_located((By.LINK_TEXT, 'Внешние накопители данных'))).click()
    wait.until(EC.visibility_of_element_located((By.LINK_TEXT, 'Сетевые хранилища (NAS)'))).click()

    sniff_info_dns('Сетевые хранилища')

except WebDriverException as e:
    driver.quit()

driver.quit()