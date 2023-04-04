from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import time

def sniff_info_citilink(name_prod):

    time.sleep(1)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.css-kan4x7.e1p9cxpz0')))
    cookies=driver.find_element(By.CSS_SELECTOR, 'div.css-kan4x7.e1p9cxpz0')
    driver.execute_script("arguments[0].remove();", cookies)

    # while(driver.find_elements(By.CSS_SELECTOR, 'button.e4uhfkv0.app-catalog-1ryoxjb.e4mggex0')):
    #     wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='e4uhfkv0 app-catalog-1ryoxjb e4mggex0']"))).click()
    #     time.sleep(2)

    if (name_prod=='Сетевые хранилища'):
        products = driver.find_elements(By.CSS_SELECTOR, 'a.app-catalog-9gnskf.e1259i3g0')[:10]
    else:
        products = driver.find_elements(By.CSS_SELECTOR, 'a.app-catalog-fjtfe3.e1lhaibo0')[:10]

    for product in products:
        link = product.get_attribute('href')

        time.sleep(2.5)

        driver.execute_script("window.open('{}', '_blank')".format(link))

        # Switch to the new tab
        driver.switch_to.window(driver.window_handles[-1])

        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'span.e1j9birj0.e106ikdt0.app-catalog-1f8xctp.e1gjr6xo0')))
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
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'app-catalog-15159qd.e1gf3j8k0')))
        characts=driver.find_elements(By.CLASS_NAME, 'app-catalog-15159qd.e1gf3j8k0')[0]
        characts=(characts.text).split('\n')

        prod_inform_citilink(name_prod, characts)

        driver.close()
        driver.switch_to.window(driver.window_handles[0])

def prod_inform_citilink(name_prode, connection_type):
    ipv6, stand, stand1, stand2, max, count, count1, stand3, stand4=' '*9
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

driver = webdriver.Chrome()

wait = WebDriverWait(driver, 100)

driver.get('https://www.citilink.ru/catalog/wi-fi-routery-marshrutizatory/')
sniff_info_citilink('Wi-Fi роутеры')

driver.get('https://www.citilink.ru/catalog/tochki-dostupa/')
sniff_info_citilink('Точки доступа')

driver.get('https://www.citilink.ru/catalog/kommutatory/?p=6')
sniff_info_citilink('Коммутаторы')

driver.get('https://www.citilink.ru/catalog/servery/')
sniff_info_citilink('Серверные платформы')

driver.get('https://www.citilink.ru/catalog/shkafy-servernye/')
sniff_info_citilink('Серверные шкафы')

driver.get('https://www.citilink.ru/catalog/setevye-hranilischa-nas')
sniff_info_citilink('Сетевые хранилища')

driver.quit()