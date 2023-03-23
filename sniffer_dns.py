from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import time

def sniff_info(driver, name_prod):
    main = []
    products = driver.find_elements(By.CSS_SELECTOR, 'div.catalog-product.ui-button-widget')

    for product in products:
        time.sleep(5)
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

        time.sleep(3)
        new_name = driver.find_element(By.CSS_SELECTOR, 'h1.product-card-top__title').text
        print(f"Name: {new_name}")

        # Click the expand all button
        expand_all_button = driver.find_element(By.CSS_SELECTOR, 'button.button-ui.button-ui_white.product-characteristics__expand')
        expand_all_button.click()

        time.sleep(5)
        # Display the Connection type
        connection_type_element = driver.find_element(By.CSS_SELECTOR, 'div.product-characteristics-content')
        connection_type = connection_type_element.text
        connection_type = connection_type.split("\n")

        prod_inform(name_prod, connection_type)

        # Close the new tab and switch back to the original tab
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    return main

def prod_inform(name_prode, connection_type):
    type_conn, ipv6, stand, max, sec, count, speed, dhcp, stat, dyn, firewall, nat, filter=' '*13
    interface, razm, setup, stand, frequency, onetime_work, speed, oper_mode, type, remove, count_ant, count_port, speed_eth, manage, supp_mesh, dhcp, supp_max, func, dop_sec, supp_poe, type_nap_pit, rozet=' '*22

    if (name_prode=='Wi-Fi роутеры'):
        for i in range(len(connection_type)):
            
            match connection_type[i]:
                case('Тип подключения'):
                    type_conn=connection_type[i+1]
                case('Поддержка IPv6'):
                    ipv6=connection_type[i+1]
                case('Стандарт Wi-Fi'):
                    stand=connection_type[i+1]
                case('Максимальная скорость по частоте 2.4 ГГц'):
                    max=connection_type[i+1]
                case('Безопасность соединения'):
                    sec=connection_type[i+1]
                case('Количество LAN портов'):
                    count=connection_type[i+1]
                case('Скорость передачи по проводному подключению'):
                    speed=connection_type[i+1]
                case('Поддержка DHCP'):
                    dhcp=connection_type[i+1]
                case('Статическая маршрутизация'):
                    stat=connection_type[i+1]
                case('Dynamic DNS (DDNS)'):
                    dyn=connection_type[i+1]
                case('Межсетевой экран (Firewall)'):
                    firewall=connection_type[i+1]
                case('NAT'):
                    nat=connection_type[i+1]
                case('Фильтрация'):
                    filter=connection_type[i+1]

        print(f"Connection type: {type_conn, ipv6, stand, max, sec, count, speed, dhcp, stat, dyn, firewall, nat, filter}")
    
    elif (name_prode=='Маршрутизаторы'):
        for i in range(len(connection_type)):
        
            match connection_type[i]:
                case('Тип подключения'):
                    type_conn=connection_type[i+1]
                case('Поддержка IPv6'):
                    ipv6=connection_type[i+1]
                case('Общее количество портов'):
                    stand=connection_type[i+1]
                case('Количество/скорость LAN портов'):
                    max=connection_type[i+1]
                case('Количество/скорость WAN портов'):
                    sec=connection_type[i+1]
                case('Количество/скорость настраиваемых WAN/LAN'):
                    count=connection_type[i+1]
                case('Скорость передачи по проводному подключению'):
                    speed=connection_type[i+1]
                case('Поддержка DHCP'):
                    dhcp=connection_type[i+1]
                case('Статическая маршрутизация'):
                    stat=connection_type[i+1]
                case('Dynamic DNS (DDNS)'):
                    dyn=connection_type[i+1]
                case('Межсетевой экран (Firewall)'):
                    firewall=connection_type[i+1]
                case('NAT'):
                    nat=connection_type[i+1]
                case('Фильтрация'):
                    filter=connection_type[i+1]

        print(f"Connection type: {type_conn, ipv6, stand, max, sec, count, speed, dhcp, stat, dyn, firewall, nat, filter}")

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

     
driver = webdriver.Chrome()

driver.get('https://www.dns-shop.ru/')

wait = WebDriverWait(driver, 10)
network_equipment_link = wait.until(EC.visibility_of_element_located((By.LINK_TEXT, 'Сетевое оборудование')))
network_equipment_link.click()

wait.until(EC.visibility_of_element_located((By.LINK_TEXT, 'Wi-Fi роутеры и оборудование для малых сетей'))).click()

wait.until(EC.visibility_of_element_located((By.LINK_TEXT, 'Wi-Fi роутеры'))).click()

sniff_info(driver, 'Wi-Fi роутеры')

driver.back()
wait.until(EC.visibility_of_element_located((By.LINK_TEXT, 'Маршрутизаторы'))).click()

sniff_info(driver, 'Маршрутизаторы')

driver.back()
wait.until(EC.visibility_of_element_located((By.LINK_TEXT, 'Wi-Fi оборудование'))).click()
wait.until(EC.visibility_of_element_located((By.LINK_TEXT, 'Точки доступа Wi-Fi'))).click()

sniff_info(driver, 'Точки доступа Wi-Fi')

driver.back()

driver.quit()