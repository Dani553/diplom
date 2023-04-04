from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import time

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

        print(f"Product price: {price}")
        print(f"Product link: {link}")
        print("="*50)

        driver.execute_script("window.open('{}', '_blank')".format(link))

        # Switch to the new tab
        driver.switch_to.window(driver.window_handles[-1])

        time.sleep(2)
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'h1.product-card-top__title')))
        new_name = driver.find_element(By.CSS_SELECTOR, 'h1.product-card-top__title').text
        print(f"Name: {new_name}")

        expand_all_button = driver.find_element(By.CSS_SELECTOR, 'button.button-ui.button-ui_white.product-characteristics__expand')
        expand_all_button.click()

        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.product-characteristics-content')))
        time.sleep(2)
        connection_type_element = driver.find_element(By.CSS_SELECTOR, 'div.product-characteristics-content')
        connection_type = connection_type_element.text
        connection_type = connection_type.split("\n")

        sniff_charact_dns(name_prod, connection_type)

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    return main

def sniff_charact_dns(name_prode, connection_type):
    
    if (name_prode=='Wi-Fi роутеры'):
        lan, stand, speed, ipv6, ikr=' '*5
        for i in range(len(connection_type)):
            
            match connection_type[i]:
                case('Количество LAN портов'):
                    lan=connection_type[i+1]
                case('Стандарт Wi-Fi'):
                    stand=connection_type[i+1]
                case('Скорость передачи по проводному подключению'):
                    speed=connection_type[i+1]
                case('Поддержка IPv6'):
                    ipv6=connection_type[i+1]
                case('Межсетевой экран (Firewall)'):
                    ikr=connection_type[i+1]

        print(f"Connection type: {lan, stand, speed, ipv6, ikr}")
    
    elif (name_prode=='Маршрутизаторы'):
        lan, wan, lan_wan, ipv6, speed = ' '*5
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
                        print(lan_wan_count_speed)
                        lan_wan=lan_wan_count_speed[0]
                    else:
                        lan_wan_count_speed=connection_type[i+1].split('x')
                        print(lan_wan_count_speed)
                        lan_wan=lan_wan_count_speed[0]
                case('Поддержка IPv6'):
                    ipv6=connection_type[i+1]
                case('Скорость передачи по проводному подключению'):
                    speed=connection_type[i+1]

        print(f"Connection type: {lan, wan, lan_wan, ipv6, speed}")

    if (name_prode=='Точки доступа Wi-Fi'):
        lan, stand, razm, setup = ' '*4
        for i in range(len(connection_type)):
        
            match connection_type[i]:
                case('Количество портов Ethernet'):
                    lan=connection_type[i+1]
                case('Стандарт Wi-Fi'):
                    stand=connection_type[i+1]
                case('Размещение'):
                    razm=connection_type[i+1]
                case('Установка'):
                    setup=connection_type[i+1]

        print(f"Connection type: {lan, stand, razm, setup}")

    if(name_prode=='Коммутаторы'):
        level, sfp, speed, vid, razm, all_ports=' '*6
        for i in range(len(connection_type)):
        
            match connection_type[i]:
                case('Уровень коммутатора'):
                    level=connection_type[i+1]
                case('Количество SFP-портов'):
                    sfp=connection_type[i+1]
                case('Внутренняя пропускная способность'):
                    speed=connection_type[i+1]
                case('Вид'):
                    vid=connection_type[i+1]
                case('Размещение'):
                    razm=connection_type[i+1]
                case('Общее количество портов коммутатора'):
                    all_ports=connection_type[i+1]

        print(f"Connection type: {level, sfp, speed, vid, razm, all_ports}")

    if(name_prode=='Шкафы и стойки'):
        yst, count, defen, height = ' '*4
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

        print(f"Connection type: {yst, count, defen, height}")

    if(name_prode=='Сетевые хранилища'):
        count_nakop, max, count, speed, wifi = ' '*5
        for i in range(len(connection_type)):
        
            match connection_type[i]:
                case('Количество отсеков для накопителей'):
                    count_nakop=connection_type[i+1]
                case('Максимально поддерживаемый объем одного накопителя'):
                    max=connection_type[i+1]
                case('Количество портов Ethernet'):
                    count=connection_type[i+1]
                case('Скорость сетевого интерфейса'):
                    speed=connection_type[i+1]
                case('Wi-Fi'):
                    wifi=connection_type[i+1]

        print(f"Connection type: {count_nakop, max, count, speed, wifi}")

driver = webdriver.Chrome()

try:
    driver.get('https://www.dns-shop.ru/')

    wait = WebDriverWait(driver, 100)
    network_equipment_link = wait.until(EC.visibility_of_element_located((By.LINK_TEXT, 'Сетевое оборудование')))
    network_equipment_link.click()

    wait.until(EC.visibility_of_element_located((By.LINK_TEXT, 'Wi-Fi роутеры и оборудование для малых сетей'))).click()
    wait.until(EC.visibility_of_element_located((By.LINK_TEXT, 'Wi-Fi роутеры'))).click()

    sniff_info_dns('Wi-Fi роутеры')

    driver.back()

    #wait.until(EC.visibility_of_element_located((By.LINK_TEXT, 'Wi-Fi роутеры и оборудование для малых сетей'))).click()
    wait.until(EC.visibility_of_element_located((By.LINK_TEXT, 'Маршрутизаторы'))).click()

    sniff_info_dns('Маршрутизаторы')

    wait.until(EC.visibility_of_element_located((By.LINK_TEXT, 'Wi-Fi роутеры и оборудование для малых сетей'))).click()
    wait.until(EC.visibility_of_element_located((By.LINK_TEXT, 'Wi-Fi оборудование'))).click()
    wait.until(EC.visibility_of_element_located((By.LINK_TEXT, 'Точки доступа Wi-Fi'))).click()

    sniff_info_dns('Точки доступа Wi-Fi')

    driver.get('https://www.dns-shop.ru/')

    network_equipment_link = wait.until(EC.visibility_of_element_located((By.LINK_TEXT, 'Сетевое оборудование')))
    network_equipment_link.click()

    wait.until(EC.visibility_of_element_located((By.LINK_TEXT, 'Профессиональное сетевое оборудование'))).click()
    wait.until(EC.visibility_of_element_located((By.LINK_TEXT, 'Коммутаторы'))).click()

    sniff_info_dns('Коммутаторы')

    driver.back()

    wait.until(EC.visibility_of_element_located((By.LINK_TEXT, 'Коммутационные шкафы и стойки'))).click()
    wait.until(EC.visibility_of_element_located((By.LINK_TEXT, 'Коммутационные и серверные шкафы'))).click()

    sniff_info_dns('Шкафы и стойки')

    driver.get('https://www.dns-shop.ru/')
    network_equipment_link = wait.until(EC.visibility_of_element_located((By.LINK_TEXT, 'ПК, ноутбуки, периферия')))
    network_equipment_link.click()

    wait.until(EC.visibility_of_element_located((By.LINK_TEXT, 'Периферия и аксессуары'))).click()
    wait.until(EC.visibility_of_element_located((By.LINK_TEXT, 'Внешние накопители данных'))).click()
    wait.until(EC.visibility_of_element_located((By.LINK_TEXT, 'Сетевые хранилища (NAS)'))).click()

    sniff_info_dns('Сетевые хранилища')

except StaleElementReferenceException:
    driver.refresh()

driver.quit()