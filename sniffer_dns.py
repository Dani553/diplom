from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import time

driver = webdriver.Chrome()

driver.get('https://www.dns-shop.ru/')

wait = WebDriverWait(driver, 10)
network_equipment_link = wait.until(EC.visibility_of_element_located((By.LINK_TEXT, 'Сетевое оборудование')))
network_equipment_link.click()

wait.until(EC.visibility_of_element_located((By.LINK_TEXT, 'Wi-Fi роутеры и оборудование для малых сетей'))).click()

wait.until(EC.visibility_of_element_located((By.LINK_TEXT, 'Wi-Fi роутеры'))).click()

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

    # Close the new tab and switch back to the original tab
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

driver.quit()

# driver = webdriver.Chrome()

# driver.get('https://www.dns-shop.ru/')

# wait = WebDriverWait(driver, 10)
# network_equipment_link = wait.until(EC.visibility_of_element_located((By.LINK_TEXT, 'Сетевое оборудование')))
# network_equipment_link.click()

# wait.until(EC.visibility_of_element_located((By.LINK_TEXT, 'Wi-Fi роутеры и оборудование для малых сетей'))).click()

# wait.until(EC.visibility_of_element_located((By.LINK_TEXT, 'Wi-Fi оборудование'))).click()

# wait.until(EC.visibility_of_element_located((By.LINK_TEXT, 'Точки доступа Wi-Fi'))).click()

# products = driver.find_elements(By.CSS_SELECTOR, 'div.catalog-product__name.ui-link.ui-link_black')
