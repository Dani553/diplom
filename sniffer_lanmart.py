from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import time
import psycopg2

def database_open(name_prod, stack_info, base_inf):
    conn = psycopg2.connect(dbname='postgres', user='postgres', 
                        password='14789635', host='localhost')
    cursor = conn.cursor()
    
    database_input(name_prod, cursor, stack_info, base_inf)

    conn.commit()
    cursor.close()
    conn.close()

def database_input(name_prod, cursor, stack, base_inf):
    match name_prod:
        case('Беспроводные маршрутизаторы'):
            cursor.execute("""INSERT INTO charact_router (charact1, charact3, charact4, charact5) values (%s, %s, %s, %s)""", stack)
            cursor.execute("""SELECT id_charact FROM charact_router ORDER BY id_charact DESC LIMIT 1""")
            id = cursor.fetchall()
            base_inf+=id
            cursor.execute("""INSERT INTO router (name, link, price, id_charact) values (%s, %s, %s, %s)""", base_inf)
        case('Маршрутизаторы'):
            cursor.execute("""INSERT INTO charact_marsh (charact2, charact4) values (%s, %s)""", stack)
            cursor.execute("""SELECT id_charact FROM charact_marsh ORDER BY id_charact DESC LIMIT 1""")
            id = cursor.fetchall()
            base_inf+=id
            cursor.execute("""INSERT INTO marsh (name, link, price, id_charact) values (%s, %s, %s, %s)""", base_inf)
        case('Коммутаторы'):
            cursor.execute("""INSERT INTO charact_com (charact2, charact3, charact4, charact5, charact7, charact8) values (%s, %s, %s, %s, %s, %s)""", stack)
            cursor.execute("""SELECT id_charact FROM charact_com ORDER BY id_charact DESC LIMIT 1""")
            id = cursor.fetchall()
            base_inf+=id
            cursor.execute("""INSERT INTO com (name, link, price, id_charact) values (%s, %s, %s, %s)""", base_inf)

def sniff_info_lanmart(name_prode):
    products = driver.find_elements(By.CSS_SELECTOR, 'div.item-area')[:10]

    for product in products:
        name_att = product.find_elements(By.CSS_SELECTOR, 'div.details-area')
        name_prod = product.find_elements(By.CSS_SELECTOR, 'h2.product-name')[0]
        name=name_prod.text
        name_att = name_prod.find_elements(By.CSS_SELECTOR, 'a')[0]
        link = name_att.get_attribute('href')
        price = product.find_elements(By.CSS_SELECTOR, 'span.price')[0]
        price=price.text

        base_inf=[name, link, price]

        driver.execute_script("window.open('{}', '_blank')".format(link))

        # Switch to the new tab
        driver.switch_to.window(driver.window_handles[-1])

        time.sleep(4)

        dop_inf=driver.find_elements(By.CSS_SELECTOR, 'div.product-tabs.horizontal')[0]

        expand_all_button = dop_inf.find_elements(By.LINK_TEXT, 'ДОПОЛНИТЕЛЬНАЯ ИНФОРМАЦИЯ')[0]
        expand_all_button.click()
        expand_all_button.click()

        characts = dop_inf.find_elements(By.CSS_SELECTOR, 'table#product-attribute-specs-table.data-table')[0]

        characts=characts.find_elements(By.TAG_NAME, 'tr')
        
        sniff_dop_charact_lanmart(name_prode, characts, base_inf)
        
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

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

        stack=[count_set, stand, speed, ipv6]
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

            stack=[ports, ipv6]
            database_open(name_prode, stack, base_inf)
    elif (name_prode=='Коммутаторы'):
            ports, ports1, speed, level, size=' '*5
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
                            case('SFP+ порт'):
                                if (len(charact_val.split(' '))>1):
                                    ports1=charact_val.split(' ')[0]
                                else:
                                    ports1=charact_val
                            case('SFP порт'):
                                if (len(charact_val.split(' '))>1):
                                    ports1=charact_val.split(' ')[0]
                                    ports1=ports1.replace('x', '')
                                else:
                                    ports1=charact_val
                            case('Наличие Гигабитного порта'):
                                nal=charact_val
                                if (nal=='ДА'):
                                    speed='1 Гб'
                            case('Коммутатор уровня'):
                                level=charact_val
                            case('Установка в стойку'):
                                if(len(charact_val.split(' '))>1):
                                    size=charact_val.split(' ')[2]
                                    size=size.replace('U', '')
                                else:
                                    size='нет'
                            case('Исполнение'):
                                isp=charact_val

                except IndexError:
                    pass
            if (speed!=' '):
                stack=[ports, ports1, level, speed, isp, size]
                database_open(name_prode, stack, base_inf)

driver = webdriver.Chrome()

driver.get('https://www.lanmart.ru/besprovodnye-marshrutizatory-4.html?limit=all')
sniff_info_lanmart('Беспроводные маршрутизаторы')

driver.get('https://www.lanmart.ru/marshrutizatory.html')
sniff_info_lanmart('Маршрутизаторы')

# driver.get('https://www.lanmart.ru/kommutatory-tp-link.html')
# sniff_info_lanmart('Коммутаторы')



driver.quit()