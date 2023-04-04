from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import time

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
                print(f'Name: {name[0].text}')
                print(f'Link: {link}')
                driver.execute_script("window.open('{}', '_blank')".format(link))

                            # Switch to the new tab
                driver.switch_to.window(driver.window_handles[-1])

                wait.until(EC.visibility_of_element_located((By.LINK_TEXT, 'Характеристики'))).click()

                                #con_characts=driver.find_elements(By.CSS_SELECTOR, 'div.detail-props-wrap')
                con_characts=driver.find_elements(By.CSS_SELECTOR, 'div.table-block')

                                
                sniff_charact_qtech(name_prode, con_characts)

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
                print(f'Name: {name[0].text}')
                print(f'Link: {link}')
                driver.execute_script("window.open('{}', '_blank')".format(link))

                            # Switch to the new tab
                driver.switch_to.window(driver.window_handles[-1])

                wait.until(EC.visibility_of_element_located((By.LINK_TEXT, 'Характеристики'))).click()

                                #con_characts=driver.find_elements(By.CSS_SELECTOR, 'div.detail-props-wrap')
                con_characts=driver.find_elements(By.CSS_SELECTOR, 'div.table-block')

                                
                sniff_charact_qtech(name_prode, con_characts)

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
                print(f'Name: {name[0].text}')
                print(f'Link: {link}')
                driver.execute_script("window.open('{}', '_blank')".format(link))

                            # Switch to the new tab
                driver.switch_to.window(driver.window_handles[-1])

                wait.until(EC.visibility_of_element_located((By.LINK_TEXT, 'Характеристики'))).click()

                                #con_characts=driver.find_elements(By.CSS_SELECTOR, 'div.detail-props-wrap')
                con_characts=driver.find_elements(By.CSS_SELECTOR, 'div.table-block')

                                
                sniff_charact_qtech(name_prode, con_characts)

                driver.close()
                driver.switch_to.window(driver.window_handles[0])


    
def sniff_charact_qtech(name_prode, con_characts):
    if (name_prode=='Управляемые коммутаторы'):
        ports1, ports2, type, speed, level, isp = ' '*6
        for container in con_characts:
            attributes=container.find_elements(By.TAG_NAME, 'tr')
            for attribute in attributes:
                characts=attribute.find_elements(By.TAG_NAME, 'td')
                match characts[0].text:
                    case('Порты 10/100/1000BASE-T PoE'):
                        ports1=characts[1].text
                    case('Порты 10/100/1000BASE-T'):
                        ports1=characts[1].text
                    case('Порты 10GbE SFP+'):
                        ports2=characts[1].text
                    case('Порты 100/1000BASE-X SFP'):
                        ports2=characts[1].text
                    case('Порты комбо 1000BASE-T\SFP'):
                        ports2=characts[1].text
                    case('Тип коммутации'):
                        type=characts[1].text
                    case('Пропускная способность'):
                        speed=characts[1].text
                    case('Уровень коммутатора'):
                        level=characts[1].text
                    case('Вариант исполнения'):
                        isp=characts[1].text
        print(f"Connection type: {ports1, ports2, type, speed, level, isp, 'управляемый'}")
    elif (name_prode=='Неуправляемые коммутаторы'):
        ports1, ports2, type, speed, level, isp = ' '*6
        for container in con_characts:
            attributes=container.find_elements(By.TAG_NAME, 'tr')
            for attribute in attributes:
                characts=attribute.find_elements(By.TAG_NAME, 'td')
                match characts[0].text:
                    case('Порты 10/100BASE-T'):
                        ports1=characts[1].text
                    case('Порты 10/100BASE-T PoE'):
                        ports1=characts[1].text
                    case('Порты 10GbE SFP+'):
                        ports2=characts[1].text
                    case('Тип коммутации'):
                        type=characts[1].text
                    case('Пропускная способность'):
                        speed=characts[1].text
                    case('Уровень коммутатора'):
                        level=characts[1].text
                    case('Вариант исполнения'):
                        isp=characts[1].text
        print(f"Connection type: {ports1, ports2, type, speed, level, isp, 'неуправляемый'}")
    elif (name_prode=='Маршрутизаторы'):
        ports1, ports2=' '*2
        for container in con_characts:
            attributes=container.find_elements(By.TAG_NAME, 'tr')
            for attribute in attributes:
                characts=attribute.find_elements(By.TAG_NAME, 'td')
                match characts[0].text:
                    case('Порты 10/100/1000BASE-T (LAN)'):
                        ports1=characts[1].text
                    case('Порты 10/100/1000BASE-T (WAN)'):
                        ports2=characts[1].text
                    case('Порты комбо 1000BASE-T\SFP (WAN)'):
                        ports2=characts[1].text
                        
        print(f"Connection type: {ports1, ports2}")
    elif (name_prode=='Серверные платформы'):
        ports, count1, count2, count3=' '*4
        for container in con_characts:
            attributes=container.find_elements(By.TAG_NAME, 'tr')
            for attribute in attributes:
                characts=attribute.find_elements(By.TAG_NAME, 'td')
                match characts[0].text:
                    case('Порты 10/100/1000BASE-T'):
                        ports=characts[1].text
                    case('Дисковая корзина (front)'):
                        count1=(characts[1].text).split('*')
                        count1=int(count1[0])
                    case('Дисковая корзина (back)'):
                        count2=(characts[1].text).split('*')
                        count2=int(count2[0])
                        count3=count1+count2
        if (count3==' '):
            count1=str(count1)      
            print(f"Connection type: {ports, count1}")
        else:
            count3=str(count3)
            print(f"Connection type: {ports, count3}")
    elif (name_prode=='Внешние точки доступа'):
        ports, stand, var=' '*3
        for container in con_characts:
            attributes=container.find_elements(By.TAG_NAME, 'tr')
            for attribute in attributes:
                characts=attribute.find_elements(By.TAG_NAME, 'td')
                match characts[0].text:
                    case('Порты 10/100/1000BASE-T (WAN)'):
                        ports=characts[1].text
                    case('Порты 10/100/1000/2500BASE-T (WAN)'):
                        ports=characts[1].text
                    case('Порты 10/100/1000BASE-T'):
                        ports=characts[1].text
                    case('Стандарт Wi-Fi'):
                        stand=characts[1].text
                    case('Варианты крепления'):
                        var=characts[1].text
        print(f"Connection type: {ports, stand, var, 'вне помещения'}")
    elif (name_prode=='Внутренние точки доступа'):
        ports1, ports2, stand, var=' '*4
        for container in con_characts:
            attributes=container.find_elements(By.TAG_NAME, 'tr')
            for attribute in attributes:
                characts=attribute.find_elements(By.TAG_NAME, 'td')
                match characts[0].text:
                    case('Порты 10/100/1000/2500BASE-T (LAN)'):
                        ports1=characts[1].text
                    case('Порты 10/100/1000BASE-T (LAN)'):
                        ports1=characts[1].text
                    case('Порты 10/100/1000/2500BASE-T (WAN)'):
                        ports2=characts[1].text
                    case('Порты 10/100/1000BASE-T (WAN)'):
                        ports2=characts[1].text
                    case('Стандарт Wi-Fi'):
                        stand=characts[1].text
                    case('Варианты крепления'):
                        var=characts[1].text
        print(f"Connection type: {ports1, ports2, stand, var, 'внутри помещения'}")
    elif (name_prode=='Wi-Fi роутеры'):
        ports1, ports2, stand, ipv6=' '*4
        for container in con_characts:
            attributes=container.find_elements(By.TAG_NAME, 'tr')
            for attribute in attributes:
                characts=attribute.find_elements(By.TAG_NAME, 'td')
                match characts[0].text:
                    case('Порты 10/100BASE-T (LAN)'):
                        ports1=characts[1].text
                    case('Порты 10/100/1000BASE-T (LAN)'):
                        ports1=characts[1].text
                    case('Порты 10/100BASE-T (WAN)'):
                        ports2=characts[1].text
                    case('Порты 10/100/1000BASE-T (WAN)'):
                        ports2=characts[1].text
                    case('Стандарт Wi-Fi'):
                        stand=characts[1].text
                    case('Сетевые протоколы'):
                        ipv6=characts[1].text
                        ipv6=ipv6.split(', ')
                        if(ipv6[0]=='IPv4/IPv6'):
                            ipv6='есть'
                        else:
                            ipv6='нет'
        print(f"Connection type: {ports1, ports2, stand, ipv6}")

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