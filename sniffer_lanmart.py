from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import time

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
                        case ('Сетевые порты'):
                                count_set=charact_val[m].text
                        case ('Порты'):
                                count=charact_val[m].text
                                count=count.split(' ')
                                count=count[0]
                        case ('Стандарты беспроводных сетей'):
                                stand=charact_val[m].text
                        case ('Скорости передачи данных'):
                                speed=charact_val[m].text
                        case ('RouterOS License'):
                                ipv6=charact_val[m].text
                                ipv6=ipv6.replace('Level', ' ')

        print(f"Connection: {count, count_set, stand, speed, ipv6}")
    if (name_prode=='Wi-Fi роутеры'):
        for i in range(len(connection_type)):
            match connection_type[i]:
                case('Поддержка протокола IPv6'):
                    ipv6=connection_type[i+1]
                case('Стандарт Wi-Fi 802.11b'):
                    if (connection_type[i+1]=='есть'):
                        output=(connection_type[i]).split(' ')
                        stand=output[1]+' '+output[2]
                    else:
                        stand='-'
                case('Стандарт Wi-Fi 802.11g'):
                    if (connection_type[i+1]=='есть'):
                        output=(connection_type[i]).split(' ')
                        stand1=output[1]+' '+output[2]
                    else:
                        stand1='-'
                case('Стандарт Wi-Fi 802.11n, 2.4 ГГц'):
                    if (connection_type[i+1]=='есть'):
                        output=(connection_type[i]).split(' ')
                        output[2]=output[2].replace(',', '')
                        stand2=output[1]+' '+output[2]
                    else: 
                        stand2='-'
                case('Стандарт Wi-Fi 802.11a, 5 ГГц'):
                    if (connection_type[i+1]=='есть'):
                        output=(connection_type[i]).split(' ')
                        stand3=output[1]+' '+output[2]
                    else:
                        stand3='-'
                case('Стандарт Wi-Fi 802.11ac, 5 ГГц'):
                    if (connection_type[i+1]=='есть'):
                        output=(connection_type[i]).split(' ')
                        output[2]=output[2].replace(',', '')
                        stand4=output[1]+' '+output[2]
                    else: 
                        stand4='-'
                case('Скорость 802.11n, 2.4 ГГц'):
                    max=connection_type[i+1]
                case('Кол-во портов WAN'):
                    count=connection_type[i+1]
                case('Количество выходных портов 10/100BASE-TX'):
                    count1=connection_type[i+1]
                case('Количество выходных портов 10/100/1000BASE-TX'):
                    count1=connection_type[i+1]
  
    
        print(f"Connection type: {ipv6, stand+', '+stand1+', '+stand2+', '+stand3+', '+stand4, max, count, count1}")

    if (name_prode=='Точки доступа'):
        setup, stand, stand1, stand2, stand3, stand4, count_port=' '*7
        for i in range(len(connection_type)):
            match connection_type[i]:
                case('Установка'):
                    setup=connection_type[i+1]
                case('Количество выходных портов 10/100BASE-TX'):
                    count_port=connection_type[i+1]
                case('Количество выходных портов 10/100/1000BASE-TX'):
                    count_port=connection_type[i+1]
                case('Стандарт Wi-Fi 802.11b'):
                    if (connection_type[i+1]=='есть'):
                        output=(connection_type[i]).split(' ')
                        stand=output[1]+' '+output[2]
                    else:
                        stand='-'
                case('Стандарт Wi-Fi 802.11g'):
                    if (connection_type[i+1]=='есть'):
                        output=(connection_type[i]).split(' ')
                        stand1=output[1]+' '+output[2]
                    else:
                        stand1='-'
                case('Стандарт Wi-Fi 802.11n, 2.4 ГГц'):
                    if (connection_type[i+1]=='есть'):
                        output=(connection_type[i]).split(' ')
                        output[2]=output[2].replace(',', '')
                        stand2=output[1]+' '+output[2]
                    else: 
                        stand2='-'
                case('Стандарт Wi-Fi 802.11a, 5 ГГц'):
                    if (connection_type[i+1]=='есть'):
                        output=(connection_type[i]).split(' ')
                        output[2]=output[2].replace(',', '')
                        stand3=output[1]+' '+output[2]
                    else:
                        stand3='-'
                case('Стандарт Wi-Fi 802.11ac, 5 ГГц'):
                    if (connection_type[i+1]=='есть'):
                        output=(connection_type[i]).split(' ')
                        output[2]=output[2].replace(',', '')
                        stand4=output[1]+' '+output[2]
                    else: 
                        stand4='-'

        print(f"Connection type: {setup, stand+', '+stand1+', '+stand2+', '+stand3+', '+stand4, count_port}")
    if (name_prode=='Коммутаторы'):
        setup, type, level, speed, port=' '*5
        for i in range(len(connection_type)):
            match connection_type[i]:
                case('Установка'):
                    setup=connection_type[i+1]
                case('Тип'):
                    type=connection_type[i+1]
                case('Уровень коммутатора'):
                    level=connection_type[i+1]
                case('Базовая скорость передачи данных'):
                    speed=connection_type[i+1]
                case('Внутренняя пропускная способность'):
                    speed=connection_type[i+1]
                case('Порты 10-100-1000Base-T (Gigabit Ethernet)'):
                    port=connection_type[i+1]
                case('Комбо-порты 1/2.5/5/10G/SFP+'):
                    port=connection_type[i+1]
                case('Порты 10-100Base-TX'):
                    port=connection_type[i+1]
                    

        print(f"Connection type: {setup, type, level, speed, port}")
    if (name_prode=='Серверные платформы'):
        proc, set_proc, max_proc, count=' '*4
        for i in range(len(connection_type)):
            match connection_type[i]:
                case('Для процессоров'):
                    proc=connection_type[i+1]
                case('Установлено процессоров'):
                    set_proc=connection_type[i+1]
                case('Максимально процессоров'):
                    max_proc=connection_type[i+1]
                case('Монтаж в стойку'):
                    count=connection_type[i+1]                   

        print(f"Connection type: {proc, set_proc, max_proc, count}")
    if (name_prode=='Серверные шкафы'):
        razm, height, sec=' '*3
        for i in range(len(connection_type)):
            match connection_type[i]:
                case('Размещение'):
                    razm=connection_type[i+1]
                case('Высота'):
                    height=connection_type[i+1]
                case('Степень защиты IP'):
                    sec=connection_type[i+1]               

        print(f"Connection type: {razm, height, sec}")
    if (name_prode=='Сетевые хранилища'):
        count_hdd, max, speed, ports=' '*4
        for i in range(len(connection_type)):
            match connection_type[i]:
                case('Количество отсеков для HDD'):
                    count_hdd=connection_type[i+1]
                case('Поддержка HDD большого объема'):
                    max=connection_type[i+1]
                case('Скорость передачи данных'):
                    speed=connection_type[i+1]   
                case('Количество портов RJ-45'):
                    ports=connection_type[i+1]              

        print(f"Connection type: {count_hdd, max, speed, ports}")

def sniff_dop_charact_lanmart(name_prode, connection_type):
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
                case ('Скорости передачи данных'):
                    speed=charact_val
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
                        stand=''
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

        print(f"Connection type: {count_set, stand, speed, ipv6}")

    elif (name_prode=='Маршрутизаторы'):
            ports, speed=' '*2
            for i in range(len(connection_type)):

                charact=connection_type[i]
                try:
                    charact_att=charact.find_elements(By.CSS_SELECTOR, 'th.label')[0].text
                    charact_val=charact.find_elements(By.TAG_NAME, 'td')[0].text

                    match charact_att:
                            case('Сетевые порты'):
                                ports=charact_val
                                ports=ports.split(' ')[0]
                            case('Наличие Гигабитного порта'):
                                nal=charact_val
                                if (nal=='ДА'):
                                    speed='<1 Гб'

                except IndexError:
                    pass

            print(f"Connection type: {ports, speed}")
    elif (name_prode=='Коммутаторы'):
            ports, speed, arch, serial, proc=' '*5
            for i in range(len(connection_type)):

                charact=connection_type[i]
                try:
                    charact_att=charact.find_elements(By.CSS_SELECTOR, 'th.label')[0].text
                    charact_val=charact.find_elements(By.TAG_NAME, 'td')[0].text

                    match charact_att:
                            case('Сетевые порты'):
                                ports=charact_val
                                ports=ports.split(' ')[0]
                            case('Наличие Гигабитного порта'):
                                nal=charact_val
                                if (nal=='ДА'):
                                    speed='<1 Гб'

                except IndexError:
                    pass

            print(f"Connection type: {ports, speed}")

driver = webdriver.Chrome()

driver.get('https://www.lanmart.ru/besprovodnye-marshrutizatory-4.html?limit=all')
sniff_info_lanmart('Беспроводные маршрутизаторы')

driver.get('https://www.lanmart.ru/marshrutizatory.html')
sniff_info_lanmart('Маршрутизаторы')

driver.quit()