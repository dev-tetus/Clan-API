import sys
import pyperclip
from selenium import webdriver


from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chromium.service import ChromiumService

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

from clash_data import ClashData
import credentials as cred

from time import sleep
from power import Power



text = """
     S.N.3.T Niveau {clan_level}
:page_facing_up: DESCRIPTION 

     SN3T est un jeune clan créé par 5 amis chacun déterminé à performer
     et devenir des joueurs aguerris. Aujourd'hui nous présentons notre
     clan, notre famille, constitutiée de joueurs solides ayant l'ambition
     de fonder un clan d'élite.

:chart_with_upwards_trend: INFO

  ✅ Chez SN3T, nous recherchons des personnes matures, motivées et engagées. Nous sommes un clan
     très flexible, ce qui signifie que l'on accepte que les gens puissent être absents pour n'importe
     quelle raison qu'ils considèrent valable. Ce que nous exigeons est que ceux s'étant précédemment engagé 
     pour un événement y participent alors activement.

:mag: __**CE CLAN EST FAIT POUR TOI SI**__:

  ✅ Tu souhaites parctiper à tous les événements (GDC, JDC, LDC)
  
  ✅ Améliorer tes héros est la priorité

  ✅ 2 :star: ne te satisfait pas

  ✅ Rejoindre un discord ne te pose pas de problèmes


     Tout respect des règles et efforts fournis au sein du clan seront felicités à travers différents biais
     

:european_castle: STATS DU CLAN AU {date}
__***Calculé avec l'API de Clash of Clans***__
        :passport_control: {clan_members}/50
        :trophy: {trophies} points du clan
        :gift: {donations_average} dons/joueur
        :fire: {clan_total_power_attack} % (Puissance d'attaque TOTALE du clan) __***Par rapport aux niveaux max de toutes les unités y compris les non débloquées***__
        :fire: {clan_actual_power_attack} % (Puissance d'attaque ACTUELLE du clan) __***Par rapport aux niveaux max possibles pour chaque HDV du clan***__
        :fire: Série actuelle de {win_streak} victoire(s) en guerre
:clipboard: PRÉREQUIS
        :house: HDV {required_townhall} minimum
        :trophy: {required_trophies} trophées minimum
        :star: Actif
        :star: Donnateur généreux

https://discord.gg/pegaQ9nygB


https://link.clashofclans.com/fr?action=OpenClanProfile&tag=2LV9J8VLQ
"""

def press_element(driver, element):
    webdriver.ActionChains(driver).click_and_hold(element).perform()
    webdriver.ActionChains(driver).release().perform()


def get_server_names_and_channels():
    return [
        ('278653494846685186','280350080895025152'),    #Clash of Clans Français 🇫🇷
        ('475679888981098496','911590761546518529'),   #Clash Community
        ('926200062319669358','926792984215838741'), #Café du recrutement 🇫🇷Clash A L'asso
        ('635409199064416288','635409199064416294'),   #La SC mania
        # ('677188056616402945','691673658111950862')   #La Souce Family
    ]

def find_servers(driver, server_names):
    servers_to_send = []
    servers_availables = WebDriverWait(driver, 20).until(
    EC.presence_of_all_elements_located((By.XPATH, "//div[@role='treeitem']")))

    sleep(2)
    for server_clickable in servers_availables:
        if server_clickable.get_attribute("aria-label").strip() in server_names:
            servers_to_send.append((server_clickable.get_attribute("aria-label").strip(), server_clickable))
    return servers_to_send

def send_message(driver, text):
    for part in text.split('\n'):
        # elem.send_keys(part)
        webdriver.ActionChains(driver).send_keys(part).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.ENTER).perform()
    webdriver.ActionChains(driver).key_down(Keys.ENTER).key_up(Keys.ENTER).perform()

def get_driver():
    if sys.platform == 'linux':
        print("Hello")
        chrome_options = ChromeOptions()
        chrome_options.add_argument("no-sandbox")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=800,600")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--headless")
        # ser=ChromeService(executable_path="./chromedriver")
        service = ChromiumService(executable_path="/usr/lib/chromium-browser/chromedriver", start_error_message='Service Error')
        chrome_driver = webdriver.Chrome(service=service, options=chrome_options)
        return chrome_driver
    else:
        edge_options = EdgeOptions()
        ser = EdgeService(executable_path="./msedgedriver.exe")
        # edge_options.add_experimental_option("detach", True)
        return webdriver.Edge(service=ser, options=edge_options)
     
     


def do_login(driver):
    driver.find_element(by=By.NAME, value='email').send_keys(cred.get_credentials()['username'])
    driver.find_element(by=By.NAME, value='password').send_keys(cred.get_credentials()['password'])
    sleep(1)
    # button = WebDriverWait(driver, 20).until(
    #     EC.presence_of_all_elements_located((By.CSS_SELECTOR, r'#app-mount > div.app-3xd6d0 > div > div > div > div > form > div > div > div.mainLoginContainer-wHmAjP > div.block-3uVSn4.marginTop20-2T8ZJx > button.marginBottom8-emkd0_.button-1cRKG6.button-f2h6uQ.lookFilled-yCfaCM.colorBrand-I6CyqQ.sizeLarge-3mScP9.fullWidth-fJIsjq.grow-2sR_-F')))
    # button = driver.find_element(by=By.CSS_SELECTOR, value=r'#app-mount > div.app-3xd6d0 > div > div > div > div > form > div > div > div.mainLoginContainer-wHmAjP > div.block-3uVSn4.marginTop20-2T8ZJx > button.marginBottom8-emkd0_.button-1cRKG6.button-f2h6uQ.lookFilled-yCfaCM.colorBrand-I6CyqQ.sizeLarge-3mScP9.fullWidth-fJIsjq.grow-2sR_-F')
    for element in driver.find_elements(By.TAG_NAME, "button"):
        if element.text == "Login" or element.text == "Iniciar sesión":
             button = element
    webdriver.ActionChains(driver).click_and_hold(button).perform()
    webdriver.ActionChains(driver).release().perform()


def get_text_with_data():
    cd = ClashData()
    p = Power(players = cd.get_player_tags())
    clan_members = cd.get_clan_members().__len__()
    trophies = cd.get_clan_points()
    donations_average = cd.get_troop_donation_avg()
    clan_total_power_attack = p.total_clan_power_attack
    clan_actual_power_attack = p.actual_clan_power_attack
    required_townhall= cd.get_required_townhall()
    required_trophies= cd.get_required_trophies()
    win_streak = cd.get_win_streak()
    clan_level=cd.get_clan_level()
    
    return text.format(date=datetime.now().strftime("%d/%m/%Y"),clan_level=str(clan_level),clan_members=str(clan_members),trophies=trophies,donations_average=donations_average,clan_total_power_attack=clan_total_power_attack,clan_actual_power_attack=clan_actual_power_attack, required_townhall=required_townhall,required_trophies=required_trophies, win_streak=win_streak)
            # .replace(r'{date}',datetime.now()\
            # .strftime("%d/%m/%Y"))\
            # .replace(r'{clan_members}',str(cd.clan_members))\
        

#Debug
if __name__ == '__main__':
    print(get_text_with_data())
