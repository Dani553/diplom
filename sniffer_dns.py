from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import time

def sniff_info_dns(name_prod):
    main = []

    while(driver.find_elements(By.CSS_SELECTOR, 'button.pagination-widget__show-more-btn')):
        time.sleep(2)
        driver.find_elements(By.CSS_SELECTOR, 'button.pagination-widget__show-more-btn')[0].click()

    products = driver.find_elements(By.CSS_SELECTOR, 'div.catalog-product.ui-button-widget')

    for product in products:
        time.sleep(2)
        name_element = product.find_element(By.CSS_SELECTOR, 'a.catalog-product__name.ui-link.ui-link_black')
        link = name_element.get_attribute('href')
        price_element = product.find_element(By.CSS_SELECTOR, 'div.product-buy__price')
        price = price_element.text

        print(f"Product price: {price}")
        print(f"Product link: {link}")
        print("="*50)

        driver.execute_script("window.open('{}', '_blank')".format(link))

        # Switch to the new tab
        driver.switch_to.window(driver.window_handles[-1])

        time.sleep(1)
        new_name = driver.find_element(By.CSS_SELECTOR, 'h1.product-card-top__title').text
        print(f"Name: {new_name}")

        expand_all_button = driver.find_element(By.CSS_SELECTOR, 'button.button-ui.button-ui_white.product-characteristics__expand')
        expand_all_button.click()

        time.sleep(2)
        connection_type_element = driver.find_element(By.CSS_SELECTOR, 'div.product-characteristics-content')
        connection_type = connection_type_element.text
        connection_type = connection_type.split("\n")

        prod_inform(name_prod, connection_type)

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    return main

def prod_inform(name_prode, connection_type):
    ipv6, stand, max, count, speed=' '*5
    interface, razm, setup, stand, frequency, onetime_work, speed, oper_mode, type, remove, count_ant, count_port, speed_eth, manage, supp_mesh, dhcp, supp_max, func, dop_sec, supp_poe, type_nap_pit, rozet=' '*22

    if (name_prode=='Wi-Fi роутеры'):
        for i in range(len(connection_type)):
            
            match connection_type[i]:
                case('Поддержка IPv6'):
                    ipv6=connection_type[i+1]
                case('Стандарт Wi-Fi'):
                    stand=connection_type[i+1]
                case('Максимальная скорость по частоте 2.4 ГГц'):
                    max=connection_type[i+1]
                case('Количество LAN портов'):
                    count=connection_type[i+1]
                case('Скорость передачи по проводному подключению'):
                    speed=connection_type[i+1]

        print(f"Connection type: {ipv6, stand, max, count, speed}")
    
    elif (name_prode=='Маршрутизаторы'):
        for i in range(len(connection_type)):
        
            match connection_type[i]:
                case('Поддержка IPv6'):
                    ipv6=connection_type[i+1]
                case('Количество/скорость WAN портов'):
                    max=connection_type[i+1]
                case('Количество/скорость LAN портов'):
                    sec=connection_type[i+1]
                case('Количество/скорость настраиваемых WAN/LAN'):
                    count=connection_type[i+1]
                case('Скорость передачи по проводному подключению'):
                    speed=connection_type[i+1]

        print(f"Connection type: {ipv6, max, sec, count, speed}")

    if (name_prode=='Точки доступа Wi-Fi'):
        for i in range(len(connection_type)):
        
            match connection_type[i]:
                case('Интерфейсы'):
                    interface=connection_type[i+1]
                case('Размещение'):
                    razm=connection_type[i+1]
                case('Установка'):
                    setup=connection_type[i+1]
                case('Стандарт Wi-Fi'):
                    stand=connection_type[i+1]
                case('Частота работы передатчика'):
                    frequency=connection_type[i+1]
                case('Одновременная работа в двух диапазонах'):
                    onetime_work=connection_type[i+1]
                case('Максимальная скорость беспроводного соединения'):
                    speed=connection_type[i+1]
                case('Режимы работы'):
                    oper_mode=connection_type[i+1]
                case('Тип антенны'):
                    type=connection_type[i+1]
                case('Съемная антенна'):
                    remove=connection_type[i+1]
                case('Количество антенн'):
                    count_ant=connection_type[i+1]
                case('Количество портов Ethernet'):
                    count_port=connection_type[i+1]
                case('Скорость передачи данных Ethernet'):
                    speed_eth=connection_type[i+1]
                case('Управление'):
                    manage=connection_type[i+1]
                case('Поддержка Mesh'):
                    supp_mesh=connection_type[i+1]
                case('DHCP'):
                    dhcp=connection_type[i+1]
                case('Поддержка WiMAX'):
                    supp_max=connection_type[i+1]
                case('Расширенные функции'):
                    func=connection_type[i+1]
                case('Дополнительная защита соединения'):
                    dop_sec=connection_type[i+1]
                case('Поддержка PoE'):
                    supp_poe=connection_type[i+1]
                case('Тип и напряжение питания'):
                    type_nap_pit=connection_type[i+1]
                case('Встроенная розетка'):
                    rozet=connection_type[i+1]

        print(f"Connection type: {interface, razm, setup, stand, frequency, onetime_work, speed, oper_mode, type, remove, count_ant, count_port, speed_eth, manage, supp_mesh, dhcp, supp_max, func, dop_sec, supp_poe, type_nap_pit, rozet}")

def sniff_info_citilink(name_prod):

    time.sleep(2)
    cookies=driver.find_element(By.CSS_SELECTOR, 'div.css-kan4x7.e1p9cxpz0')
    driver.execute_script("arguments[0].remove();", cookies)

    while(driver.find_elements(By.CSS_SELECTOR, 'button.e4uhfkv0.app-catalog-1ryoxjb.e4mggex0')):
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='e4uhfkv0 app-catalog-1ryoxjb e4mggex0']"))).click()
        time.sleep(2)

    products = driver.find_elements(By.CSS_SELECTOR, 'a.app-catalog-fjtfe3.e1lhaibo0')

    for product in products:
        link = product.get_attribute('href')

        driver.execute_script("window.open('{}', '_blank')".format(link))

        # Switch to the new tab
        driver.switch_to.window(driver.window_handles[-1])

        time.sleep(3)
        price = driver.find_elements(By.CSS_SELECTOR, 'span.e1j9birj0.e106ikdt0.app-catalog-1f8xctp.e1gjr6xo0')[0]
        price=price.text

        name = driver.find_elements(By.CSS_SELECTOR, 'h1.e1ubbx7u0.eml1k9j0.app-catalog-tn2wxd.e1gjr6xo0')[0]
        name=name.text

        print(f"Product price: {price}")
        print(f"Product link: {link}")
        print(f"Name: {name}")

        charact=wait.until(EC.visibility_of_element_located((By.LINK_TEXT, 'Характеристики')))
        charact_link=charact.get_attribute('href')
        
        driver.get(charact_link)
        time.sleep(3)
        characts=driver.find_elements(By.CLASS_NAME, 'app-catalog-15159qd.e1gf3j8k0')[0]
        characts=(characts.text).split('\n')

        prod_inform_citilink(name_prod, characts)

        driver.close()
        driver.switch_to.window(driver.window_handles[0])

def prod_inform_citilink(name_prode, connection_type):
    ipv6, stand, stand1, stand2, max, count, count1, dhcp, dyn, firewall=' '*10
    interface, setup, stand, stand1, stand2, stand3, frequency, onetime_work, speed, type, count_ant, count_port, supp_poe=' '*13
    if (name_prode=='Wi-Fi роутеры'):
        for i in range(len(connection_type)):
            
            match connection_type[i]:
                case('Поддержка протокола IPv6'):
                    ipv6=connection_type[i+1]
                case('Стандарт Wi-Fi 802.11b'):
                    if (connection_type[i+1]=='есть'):
                        output=(connection_type[i]).split(' ')
                        stand=output[1]+' '+output[2]
                case('Стандарт Wi-Fi 802.11g'):
                    if (connection_type[i+1]=='есть'):
                        output=(connection_type[i]).split(' ')
                        stand1=output[1]+' '+output[2]
                case('Стандарт Wi-Fi 802.11n, 2.4 ГГц'):
                    if (connection_type[i+1]=='есть'):
                        output=(connection_type[i]).split(' ')
                        output[2]=output[2].replace(',', '')
                        stand2=output[1]+' '+output[2]
                case('Скорость 802.11n, 2.4 ГГц'):
                    max=connection_type[i+1]
                case('Кол-во портов WAN'):
                    count=connection_type[i+1]
                case('Количество выходных портов 10/100BASE-TX'):
                    count1=connection_type[i+1]
                case('Количество выходных портов 10/100/1000BASE-TX'):
                    count1=connection_type[i+1]
                case('DHCP-сервер'):
                    dhcp=connection_type[i+1]
                case('Поддержка динамического DNS'):
                    dyn=connection_type[i+1]
                case('Межсетевой экран (FireWall)'):
                    firewall=connection_type[i+1]
    
        print(f"Connection type: {ipv6, stand+', '+stand1+', '+stand2, max, count, count1, dhcp, dyn, firewall}")

    if (name_prode=='Точки доступа'):
        for i in range(len(connection_type)):
        
            match connection_type[i]:
                case('Входной интерфейс'):
                    interface=connection_type[i+1]
                    print("Количество выходных портов", interface)
                case('Установка'):
                    setup=connection_type[i+1]
                case('Стандарт WEP'):
                    if (connection_type[i+1]=='есть'):
                        stand=connection_type[i].split(' ')
                        stand=stand[1]
                case('Стандарт WPA'):
                    if (connection_type[i+1]=='есть'):
                        stand1=connection_type[i].split(' ')
                        stand1=stand1[1]
                case('Стандарт WPA2'):
                    if (connection_type[i+1]=='есть'):
                        stand2=connection_type[i].split(' ')
                        stand2=stand2[1]
                case('Стандарт WPA3'):
                    if (connection_type[i+1]=='есть'):
                        stand3=connection_type[i].split(' ')
                        stand3=stand3[1]
                case('Диапазон 2.4 ГГц'):
                    if (connection_type[i+1]=='есть'):
                        frequency=connection_type[i].split(' ')
                        frequency=frequency[1]+' '+frequency[2]
                case('Количество диапазонов'):
                    if (connection_type[i+1]=='однодиапазонный'):
                        onetime_work='нет'
                    if (connection_type[i+1]=='двухдиапазонный'):
                        onetime_work='есть'
                case('Скорость 802.11n, 2.4 ГГц'):
                    speed=connection_type[i+1]
                case('Тип антенн'):
                    type=connection_type[i+1]
                case('Количество антенн'):
                    count_ant=connection_type[i+1]
                case('Количество выходных портов 10/100BASE-TX'):
                    count_port=connection_type[i+1]
                case('Количество выходных портов 10/100/1000BASE-TX'):
                    count_port=connection_type[i+1]
                case('Поддержка Power over Ethernet (PoE)'):
                    supp_poe=connection_type[i+1]

        print(f"Connection type: {interface, setup, stand+', '+stand1+', '+stand2+', '+stand3, frequency, onetime_work, speed, type, count_ant, count_port, supp_poe}")

def sniff_info_lanmart(name_prode):
    products = driver.find_elements(By.CSS_SELECTOR, 'div.item-area')

    for product in products:
        name_att = product.find_elements(By.CSS_SELECTOR, 'div.details-area')
        name_prod = product.find_elements(By.CSS_SELECTOR, 'h2.product-name')[0]
        name=name_prod.text
        name_att = name_prod.find_elements(By.CSS_SELECTOR, 'a')[0]
        link = name_att.get_attribute('href')
        price = product.find_elements(By.CSS_SELECTOR, 'span.price')[0]
        price=price.text

        print(f"Name: {name}")
        print(f"Product price: {price}")
        print(f"Product link: {link}")

        driver.execute_script("window.open('{}', '_blank')".format(link))

        # Switch to the new tab
        driver.switch_to.window(driver.window_handles[-1])

        time.sleep(4)

        dop_inf=driver.find_elements(By.CSS_SELECTOR, 'div.product-tabs.horizontal')[0]

        inf=driver.find_elements(By.CSS_SELECTOR, 'div.col-main.col-lg-9')[0]

        inff=inf.find_elements(By.CSS_SELECTOR, 'table.data-table')
        inff1=inff[1].text

        if (inff1!=''):
            sniff_charact_lanmart(name_prode, inff)
        else:
            expand_all_button = dop_inf.find_elements(By.LINK_TEXT, 'ДОПОЛНИТЕЛЬНАЯ ИНФОРМАЦИЯ')[0]
            expand_all_button.click()
            expand_all_button.click()

            characts = dop_inf.find_elements(By.CSS_SELECTOR, 'table#product-attribute-specs-table.data-table')[0]

            characts=characts.find_elements(By.TAG_NAME, 'tr')
        
            sniff_dop_charact_lanmart(name_prode, characts)
        
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

def sniff_charact_lanmart(name_prode, connection_type):
    count, stand, speed=' '*3
    ports, speed, arch, serial, proc=' '*5
    if (name_prode=='Беспроводные маршрутизаторы'):
        for i in range(len(connection_type)):
            
            #print(connection_type[i].text)
            charact=connection_type[i].find_elements(By.TAG_NAME, 'tr')[1:]

            for k in charact:
                charact_att=k.find_elements(By.TAG_NAME, 'th')
                charact_val=k.find_elements(By.TAG_NAME, 'td')

                for m in range(len(charact_att)):

                    match charact_att[m].text:
                        case ('Интерфейс'):
                                count=charact_val[m].text
                        case ('Порты'):
                                count=charact_val[m].text
                        case ('Стандарты беспроводных сетей'):
                                stand=charact_val[m].text
                        case ('Скороcть передачи'):
                                speed=charact_val[m].text

        print(f"Connection: {count, stand, speed}")

def sniff_dop_charact_lanmart(name_prode, connection_type):
    count, stand, speed=' '*3
    ports, speed, arch, serial, proc=' '*5
    if (name_prode=='Беспроводные маршрутизаторы'):
        for i in range(len(connection_type)):

            charact=connection_type[i]
            charact_att=charact.find_elements(By.TAG_NAME, 'th')[0].text
            charact_val=charact.find_elements(By.TAG_NAME, 'td')[0].text

            match charact_att:
                case ('Сетевые порты'):
                    count=charact_val
                case ('Встроенный Wireless'):
                    stand=charact_val
                case ('Скорости передачи данных'):
                    speed=charact_val

        print(f"Connection type: {count, stand, speed}")

    elif (name_prode=='Маршрутизаторы'):
            for i in range(len(connection_type)):

                charact=connection_type[i]
                try:
                    charact_att=charact.find_elements(By.CSS_SELECTOR, 'th.label')[0].text
                    charact_val=charact.find_elements(By.TAG_NAME, 'td')[0].text
                except IndexError:
                    pass

                match charact_att:
                        case('Сетевые порты'):
                            ports=charact_val
                        case('Наличие Гигабитного порта'):
                            nal=charact_val
                            if (nal=='ДА'):
                                speed='1 Гб'
                        case('Архитектура'):
                            arch=charact_val
                        case('Serial port'):
                            serial=charact_val
                        case('Процессор'):
                            proc=charact_val

            print(f"Connection type: {ports, speed, arch, serial, proc}")
     
driver = webdriver.Chrome()

driver.get('https://www.dns-shop.ru/')

wait = WebDriverWait(driver, 10)
network_equipment_link = wait.until(EC.visibility_of_element_located((By.LINK_TEXT, 'Сетевое оборудование')))
network_equipment_link.click()

wait.until(EC.visibility_of_element_located((By.LINK_TEXT, 'Wi-Fi роутеры и оборудование для малых сетей'))).click()

wait.until(EC.visibility_of_element_located((By.LINK_TEXT, 'Wi-Fi роутеры'))).click()

sniff_info_dns(driver, 'Wi-Fi роутеры')

driver.back()
wait.until(EC.visibility_of_element_located((By.LINK_TEXT, 'Маршрутизаторы'))).click()

sniff_info_dns(driver, 'Маршрутизаторы')

driver.back()
wait.until(EC.visibility_of_element_located((By.LINK_TEXT, 'Wi-Fi оборудование'))).click()
wait.until(EC.visibility_of_element_located((By.LINK_TEXT, 'Точки доступа Wi-Fi'))).click()

sniff_info_dns(driver, 'Точки доступа Wi-Fi')

driver.back()

driver.get('https://www.citilink.ru/catalog/wi-fi-routery-marshrutizatory/')
sniff_info_citilink('Wi-Fi роутеры')

driver.get('https://www.citilink.ru/catalog/tochki-dostupa/')
sniff_info_citilink('Точки доступа')

driver.get('https://www.lanmart.ru/besprovodnye-marshrutizatory-4.html?limit=all')
sniff_info_lanmart('Беспроводные маршрутизаторы')

driver.get('https://www.lanmart.ru/marshrutizatory.html')
sniff_info_lanmart('Маршрутизаторы')

driver.quit()
