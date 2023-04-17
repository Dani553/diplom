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
        case('Wi-Fi роутеры'):
            cursor.execute("""INSERT INTO charact_router (charact1, charact2, charact3, charact5) values (%s, %s, %s, %s)""", stack)
            cursor.execute("""SELECT id_charact FROM charact_router ORDER BY id_charact DESC LIMIT 1""")
            id = cursor.fetchall()
            base_inf+=id
            cursor.execute("""INSERT INTO router (name, link, id_charact) values (%s, %s, %s)""", base_inf)
        case('Маршрутизаторы'):
            cursor.execute("""INSERT INTO charact_marsh (charact1, charact2) values (%s, %s)""", stack)
            cursor.execute("""SELECT id_charact FROM charact_marsh ORDER BY id_charact DESC LIMIT 1""")
            id = cursor.fetchall()
            base_inf+=id
            cursor.execute("""INSERT INTO marsh (name, link, id_charact) values (%s, %s, %s)""", base_inf)
        case('Внутренние точки доступа'):
            cursor.execute("""INSERT INTO charact_toch (charact2, charact3, charact4, charact5) values (%s, %s, %s, %s)""", stack)
            cursor.execute("""SELECT id_charact FROM charact_toch ORDER BY id_charact DESC LIMIT 1""")
            id = cursor.fetchall()
            base_inf+=id
            cursor.execute("""INSERT INTO toch (name, link, id_charact) values (%s, %s, %s)""", base_inf)
        case('Внешние точки доступа'):
            cursor.execute("""INSERT INTO charact_toch (charact2, charact3, charact4, charact5) values (%s, %s, %s, %s)""", stack)
            cursor.execute("""SELECT id_charact FROM charact_toch ORDER BY id_charact DESC LIMIT 1""")
            id = cursor.fetchall()
            base_inf+=id
            cursor.execute("""INSERT INTO toch (name, link, id_charact) values (%s, %s, %s)""", base_inf)
        case('Управляемые коммутаторы'):
            cursor.execute("""INSERT INTO charact_com (charact2, charact3, charact4, charact5, charact6, charact7, charact8) values (%s, %s, %s, %s, %s, %s, %s)""", stack)
            cursor.execute("""SELECT id_charact FROM charact_com ORDER BY id_charact DESC LIMIT 1""")
            id = cursor.fetchall()
            base_inf+=id
            cursor.execute("""INSERT INTO com (name, link, id_charact) values (%s, %s, %s)""", base_inf)
        case('Неуправляемые коммутаторы'):
            cursor.execute("""INSERT INTO charact_com (charact2, charact3, charact4, charact5, charact6, charact7) values (%s, %s, %s, %s, %s, %s)""", stack)
            cursor.execute("""SELECT id_charact FROM charact_com ORDER BY id_charact DESC LIMIT 1""")
            id = cursor.fetchall()
            base_inf+=id
            cursor.execute("""INSERT INTO com (name, link, id_charact) values (%s, %s, %s)""", base_inf)
        case('Серверные платформы'):
            cursor.execute("""INSERT INTO charact_server (charact1, charact2, charact3, charact4, charact5, charact6) values (%s, %s, %s, %s, %s, %s)""", stack)
            cursor.execute("""SELECT id_charact FROM charact_server ORDER BY id_charact DESC LIMIT 1""")
            id = cursor.fetchall()
            base_inf+=id
            cursor.execute("""INSERT INTO server (name, link, id_charact) values (%s, %s, %s)""", base_inf)

def sniff_info_qtech(name_prode):
    time.sleep(3)
    if (name_prode=='Управляемые коммутаторы') | (name_prode=='Неуправляемые коммутаторы'):
        products_page = driver.find_elements(By.CSS_SELECTOR, 'div.product-compare-section')
        for category in products_page:
            sections=category.find_elements(By.CSS_SELECTOR, 'div.product-compare-list-item')
            for section in sections:
                name=section.find_elements(By.CSS_SELECTOR, 'h3.product__title')
                name_series=section.find_elements(By.TAG_NAME, 'a')[0]
                link = name_series.get_attribute('href')
                name=name[0].text
                base_inf=[name, link]
                driver.execute_script("window.open('{}', '_blank')".format(link))

                            # Switch to the new tab
                driver.switch_to.window(driver.window_handles[-1])

                wait.until(EC.visibility_of_element_located((By.LINK_TEXT, 'Характеристики'))).click()

                                #con_characts=driver.find_elements(By.CSS_SELECTOR, 'div.detail-props-wrap')
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
                name_series=section.find_elements(By.TAG_NAME, 'a')[0]
                link = name_series.get_attribute('href')
                name=name[0].text
                base_inf=[name, link]
                driver.execute_script("window.open('{}', '_blank')".format(link))

                            # Switch to the new tab
                driver.switch_to.window(driver.window_handles[-1])

                wait.until(EC.visibility_of_element_located((By.LINK_TEXT, 'Характеристики'))).click()

                                #con_characts=driver.find_elements(By.CSS_SELECTOR, 'div.detail-props-wrap')
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
                base_inf=[name, link]
                driver.execute_script("window.open('{}', '_blank')".format(link))

                            # Switch to the new tab
                driver.switch_to.window(driver.window_handles[-1])

                wait.until(EC.visibility_of_element_located((By.LINK_TEXT, 'Характеристики'))).click()

                                #con_characts=driver.find_elements(By.CSS_SELECTOR, 'div.detail-props-wrap')
                con_characts=driver.find_elements(By.CSS_SELECTOR, 'div.table-block')

                                
                sniff_charact_qtech(name_prode, con_characts, base_inf)

                driver.close()
                driver.switch_to.window(driver.window_handles[0])


    
def sniff_charact_qtech(name_prode, con_characts, base_inf):
    if (name_prode=='Управляемые коммутаторы'):
        ports1, ports2, speed, level, isp, height = ' '*6
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
                    case('Порты 10GbE SFP+'):
                        ports2=characts[1].text
                        ports2=ports2.split(' ')[0]
                    case('Порты 100/1000BASE-X SFP'):
                        ports2=characts[1].text
                        ports2=ports2.split(' ')[0]
                    case('Порты комбо 1000BASE-T\SFP'):
                        ports2=characts[1].text
                        ports2=ports2.split(' ')[0]
                    case('Пропускная способность'):
                        speed=characts[1].text
                    case('Уровень коммутатора'):
                        level=characts[1].text
                    case('Вариант исполнения'):
                        isp=characts[1].text
                    case('Высота, U'):
                        height=characts[1].text
        if (ports1!=' ') & (ports2!=' ') & (level!=' ') & (speed!=' '):
            stack_info=[ports1, ports2, level, speed, 'управляемый', isp, height]
            database_open(name_prode, stack_info, base_inf)
    elif (name_prode=='Неуправляемые коммутаторы'):
        ports1, ports2, speed, level, isp = ' '*5
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
                    case('Порты 10GbE SFP+'):
                        ports2=characts[1].text
                        ports2=ports2.split(' ')[0]
                    case('Пропускная способность'):
                        speed=characts[1].text
                    case('Уровень коммутатора'):
                        level=characts[1].text
                    case('Вариант исполнения'):
                        isp=characts[1].text
        stack_info=[ports1, ports2, level, speed, 'неуправляемый', isp]
        database_open(name_prode, stack_info, base_inf)
    elif (name_prode=='Маршрутизаторы'):
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
                        
        stack_info=[ports, ports1]
        database_open(name_prode, stack_info, base_inf)
    elif (name_prode=='Серверные платформы'):
        ports, ports21, ports22, proc, count_proc, height, count1, count2, count3=' '*9
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
                    case('Высота, U'):
                        height=characts[1].text
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
                        count2=int(count2[0])
                        count3=count1+count2
        if (count3==' '):
            count1=str(count1)      
            stack_info=[ports, ports21, proc, count_proc, count1, height]
            database_open(name_prode, stack_info, base_inf)
        else:
            count3=str(count3)
            stack_info=[ports, ports21, proc, count_proc, count3, height]
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
                stack_info=[lan, stand, 'вне помещения', var]
                database_open(name_prode, stack_info, base_inf)
        elif (wan!=' '):
                stack_info=[wan, stand, 'вне помещения', var]
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
                stack_info=[lan, stand, 'внутри помещения', var]
                database_open(name_prode, stack_info, base_inf)
        elif (wan!=' '):
                stack_info=[wan, stand, 'внутри помещения', var]
                database_open(name_prode, stack_info, base_inf)

    elif (name_prode=='Wi-Fi роутеры'):
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

        stack_info=[wan, lan, stand, ipv6]
        database_open(name_prode, stack_info, base_inf)

driver = webdriver.Chrome()

wait = WebDriverWait(driver, 100)
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