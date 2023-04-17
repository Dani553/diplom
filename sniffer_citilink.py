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
            cursor.execute("""INSERT INTO charact_router (charact1, charact2, charact3, charact4, charact5) values (%s, %s, %s, %s, %s)""", stack)
            cursor.execute("""SELECT id_charact FROM charact_router ORDER BY id_charact DESC LIMIT 1""")
            id = cursor.fetchall()
            base_inf+=id
            cursor.execute("""INSERT INTO router (name, link, price, id_charact) values (%s, %s, %s, %s)""", base_inf)
        case('Точки доступа'):
            cursor.execute("""INSERT INTO charact_toch (charact2, charact3, charact4, charact5) values (%s, %s, %s, %s)""", stack)
            cursor.execute("""SELECT id_charact FROM charact_toch ORDER BY id_charact DESC LIMIT 1""")
            id = cursor.fetchall()
            base_inf+=id
            cursor.execute("""INSERT INTO toch (name, link, price, id_charact) values (%s, %s, %s, %s)""", base_inf)
        case('Коммутационные шкафы'):
            cursor.execute("""INSERT INTO charact_shkaf (charact1, charact2, charact3, charact4, charact5) values (%s, %s, %s, %s, %s)""", stack)
            cursor.execute("""SELECT id_charact FROM charact_shkaf ORDER BY id_charact DESC LIMIT 1""")
            id = cursor.fetchall()
            base_inf+=id
            cursor.execute("""INSERT INTO shkaf (name, link, price, id_charact) values (%s, %s, %s, %s)""", base_inf)
        case('Серверные шкафы'):
            cursor.execute("""INSERT INTO charact_shkaf (charact1, charact2, charact3, charact4, charact5) values (%s, %s, %s, %s, %s)""", stack)
            cursor.execute("""SELECT id_charact FROM charact_shkaf ORDER BY id_charact DESC LIMIT 1""")
            id = cursor.fetchall()
            base_inf+=id
            cursor.execute("""INSERT INTO shkaf (name, link, price, id_charact) values (%s, %s, %s, %s)""", base_inf)
        case('Сетевые хранилища'):
            cursor.execute("""INSERT INTO charact_chran (charact1, charact2, charact3, charact4) values (%s, %s, %s, %s)""", stack)
            cursor.execute("""SELECT id_charact FROM charact_chran ORDER BY id_charact DESC LIMIT 1""")
            id = cursor.fetchall()
            base_inf+=id
            cursor.execute("""INSERT INTO chran (name, link, price, id_charact) values (%s, %s, %s, %s)""", base_inf)

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
    elif (name_prod=='Коммутаторы'):
        products = driver.find_elements(By.CSS_SELECTOR, 'div.app-catalog-l9pqdy.e1btxpey0')[:10]
    else:
        products = driver.find_elements(By.CSS_SELECTOR, 'a.app-catalog-fjtfe3.e1lhaibo0')[:10]

    for product in products:
        link = product.get_attribute('href')

        time.sleep(3)

        driver.execute_script("window.open('{}', '_blank')".format(link))

        # Switch to the new tab
        driver.switch_to.window(driver.window_handles[-1])

        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'span.e1j9birj0.e106ikdt0.app-catalog-1f8xctp.e1gjr6xo0')))
        price = driver.find_elements(By.CSS_SELECTOR, 'span.e1j9birj0.e106ikdt0.app-catalog-1f8xctp.e1gjr6xo0')[0]
        price=price.text

        name = driver.find_elements(By.CSS_SELECTOR, 'h1.e1ubbx7u0.eml1k9j0.app-catalog-tn2wxd.e1gjr6xo0')[0]
        name=name.text

        base_inf=[name, link, price]

        charact=wait.until(EC.visibility_of_element_located((By.LINK_TEXT, 'Характеристики')))
        charact_link=charact.get_attribute('href')
        
        driver.get(charact_link)
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'app-catalog-15159qd.e1gf3j8k0')))
        characts=driver.find_elements(By.CLASS_NAME, 'app-catalog-15159qd.e1gf3j8k0')[0]
        characts=(characts.text).split('\n')

        prod_inform_citilink(name_prod, characts, base_inf)

        driver.close()
        driver.switch_to.window(driver.window_handles[0])

def prod_inform_citilink(name_prode, connection_type, base_inf):
    ipv6, stand, stand1, stand2, speed, wan, lan, stand3, stand4=' '*9
    if (name_prode=='Wi-Fi роутеры'):
        for i in range(len(connection_type)):
            match connection_type[i]:
                case('Поддержка протокола IPv6'):
                    ipv6=connection_type[i+1]
                case('Стандарт Wi-Fi 802.11b'):
                    if (connection_type[i+1]=='есть'):
                        output=(connection_type[i]).split(' ')
                        stand=output[2]
                    else:
                        stand='-'
                case('Стандарт Wi-Fi 802.11g'):
                    if (connection_type[i+1]=='есть'):
                        output=(connection_type[i]).split(' ')
                        stand1=output[2]
                    else:
                        stand1='-'
                case('Стандарт Wi-Fi 802.11n, 2.4 ГГц'):
                    if (connection_type[i+1]=='есть'):
                        output=(connection_type[i]).split(' ')
                        stand2=output[2]
                    else: 
                        stand2='-'
                case('Стандарт Wi-Fi 802.11a, 5 ГГц'):
                    if (connection_type[i+1]=='есть'):
                        output=(connection_type[i]).split(' ')
                        stand3=output[2]
                    else:
                        stand3='-'
                case('Стандарт Wi-Fi 802.11ac, 5 ГГц'):
                    if (connection_type[i+1]=='есть'):
                        output=(connection_type[i]).split(' ')
                        output[2]=output[2].replace(',', '')
                        stand4=output[2]
                    else: 
                        stand4='-'
                case('Скорость 802.11n, 2.4 ГГц'):
                    speed=connection_type[i+1]
                case('Кол-во портов WAN'):
                    wan=connection_type[i+1]
                case('Количество выходных портов 10/100BASE-TX'):
                    lan=connection_type[i+1]
                case('Количество выходных портов 10/100/1000BASE-TX'):
                    lan=connection_type[i+1]

        stand=stand+', '+stand1+', '+stand2+' '+stand3+' '+stand4
        stack_info=[wan, lan, stand, speed, ipv6]

        database_open(name_prode, stack_info, base_inf)

    if (name_prode=='Точки доступа'):
        setup, stand, stand1, stand2, stand3, stand4, lan, wan_lan=' '*8
        for i in range(len(connection_type)):
            print(connection_type[i])
            match connection_type[i]:
                case('Установка'):
                    setup=connection_type[i+1]
                case('Количество выходных портов 10/100BASE-TX'):
                    lan=connection_type[i+1]
                case('Количество выходных портов 10/100/1000BASE-TX'):
                    lan=connection_type[i+1]
                case('Кол-во портов WAN'):
                    wan=connection_type[i+1]
                case('Стандарт Wi-Fi 802.11b'):
                    if (connection_type[i+1]=='есть'):
                        output=(connection_type[i]).split(' ')
                        stand=output[2]
                    else:
                        stand='-'
                case('Стандарт Wi-Fi 802.11g'):
                    if (connection_type[i+1]=='есть'):
                        output=(connection_type[i]).split(' ')
                        stand1=output[2]
                    else:
                        stand1='-'
                case('Стандарт Wi-Fi 802.11n, 2.4 ГГц'):
                    if (connection_type[i+1]=='есть'):
                        output=(connection_type[i]).split(' ')
                        stand2=output[2]
                    else: 
                        stand2='-'
                case('Стандарт Wi-Fi 802.11a, 5 ГГц'):
                    if (connection_type[i+1]=='есть'):
                        output=(connection_type[i]).split(' ')
                        stand3=output[2]
                    else:
                        stand3='-'
                case('Стандарт Wi-Fi 802.11ac, 5 ГГц'):
                    if (connection_type[i+1]=='есть'):
                        output=(connection_type[i]).split(' ')
                        stand4=output[2]
                    else: 
                        stand4='-'
        if (wan!=' '):
            wan_lan=int(wan)+int(lan)
            wan_lan=str(wan_lan)
        else:
            wan_lan=lan
        if (stand==' '):
            if(stand1==' '):
                stand=stand2+' '+stand3+' '+stand4
            else:
                stand=stand1+', '+stand2+' '+stand3+' '+stand4
        else:
            stand=stand+', '+stand1+', '+stand2+' '+stand3+' '+stand4

        if (setup=='на мачту') | (setup=='на стену, трубостойку'):
            rasp='вне помещения'
        else:
            rasp='внутри помещения'
        
        if (setup!=' '):
            stack_info=[wan_lan, stand, rasp, setup]

            database_open(name_prode, stack_info, base_inf)

    if (name_prode=='Серверные шкафы'):
        razm, height, sec, count=' '*4
        for i in range(len(connection_type)):
            match connection_type[i]:
                case('Размещение'):
                    razm=connection_type[i+1]
                case('Высота'):
                    count=connection_type[i+1]
                    count=count.replace('U', '')
                case('Степень защиты IP'):
                    sec=connection_type[i+1]   
                case('Размеры (ШхВхГ)'):
                    height=(connection_type[i+1]).split('x')
                    height=height[1]           
        if (height!=' '):
            stack_info=[razm, count, sec, height, 'cерверные шкафы']
            database_open(name_prode, stack_info, base_inf)

    if (name_prode=='Коммутационные шкафы'):
        razm, height, sec, count=' '*4
        for i in range(len(connection_type)):
            match connection_type[i]:
                case('Размещение'):
                    razm=connection_type[i+1]
                case('Высота'):
                    count=connection_type[i+1]
                    count=count.replace('U', '')
                case('Степень защиты IP'):
                    sec=connection_type[i+1]   
                case('Размеры (ШхВхГ)'):
                    height=connection_type[i+1].split('x')
                    if (height==(' ')):
                        height=connection_type[i+1].split('x')
                        height=height[1]
                    else:
                        height=height[1]           

        stack_info=[razm, count, sec, height, 'коммутационные шкафы']
        database_open(name_prode, stack_info, base_inf)

    if (name_prode=='Сетевые хранилища'):
        count_hdd, max, speed, ports=' '*4
        for i in range(len(connection_type)):
            match connection_type[i]:
                case('Количество отсеков для HDD'):
                    count_hdd=connection_type[i+1]
                case('Поддержка HDD большого объема'):
                    max=connection_type[i+1]
                    max=max.split(' ')[1]
                case('Поддержка HDD большого объема'):
                    max=connection_type[i+1]
                    max=max.split(' ')[1]
                case('Скорость передачи данных'):
                    speed=connection_type[i+1]
                    if (speed=='10/100/1000 Мбит/с'):
                        speed='1'
                    else:
                        speed=speed.split(' ')[2]
                        if (speed=='10/100/1000'):
                            speed='1'
                case('Количество портов RJ-45'):
                    ports=connection_type[i+1]              
        if (max!=' '):
            stack_info=[count_hdd, max, ports, speed]
            database_open(name_prode, stack_info, base_inf)

driver = webdriver.Chrome()

wait = WebDriverWait(driver, 100)

# driver.get('https://www.citilink.ru/catalog/wi-fi-routery-marshrutizatory/')
# sniff_info_citilink('Wi-Fi роутеры')

driver.get('https://www.citilink.ru/catalog/tochki-dostupa/')
sniff_info_citilink('Точки доступа')

# driver.get('https://www.citilink.ru/catalog/shkafy-servernye/')
# sniff_info_citilink('Коммутационные шкафы')

# driver.get('https://www.citilink.ru/catalog/shkafy-servernye/?p=2')
# sniff_info_citilink('Серверные шкафы')

# driver.get('https://www.citilink.ru/catalog/setevye-hranilischa-nas')
# sniff_info_citilink('Сетевые хранилища')

driver.quit()