from datetime import datetime
import site
import sys
from os import path
from time import sleep
from venv import main

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.relative_locator import locate_with

from selenium.webdriver.common.alert import Alert

import clash_data

#Read discord credentials from file
f = open("credentials.txt", "r")
content = f.readlines()
print(content)

#Data
#############################################
username = content[0].split(' ')[1].strip()
password = content[1].split(' ')[1].strip()

text = '''
𝒮𝒩𝟥𝒯

📄 DESCRIPTION 

         Salut a tous, nous sommes un groupe d'amis qui jouent au jeu depuis 10 ans maintenant et
nous venons de prendre la décision de créer notre propre clan en ayant pour but de performer
un maximum et grandir tous ensemble.

📈 PROJETS ACTUELS ET FUTURS

        ✅ En attendant de retrouver des joueurs motivés et responsables, nous lançons des guerres 24/7 
histoire de gagner de l'XP du clan afin d'obtenir les avantages de celui-ci au plus vite, ceci dit,
nous avons l'intention de faire la Ligue de clans en ayant le même objectif en tête.
nous vous invitons a nous rejoindre à cet étape étant donné que c'est la partie dans laquelle
la constance et compromis des joueurs sont essentiels et c'est justement ce que SN3T recherche
au long terme, des joueurs motivés et prêts à faire avancer le clan épaulé par tout les autres membres.

        ✅ Une fois que cette étape sera franchie(où nous commencerons à voir un joli nombre de joueurs), nous commencerons
à prévoir d'autres événements internes au clan afin d'obtenir les résultats recherchés au niveau collectif et image
du clan.

🏰 MEMBRES DU CLAN {date}
        🛂 {clan_members}/50
        🎁 +/- 1,5K donations/joueur
📋 PRÉREQUIS
        ⭐ Pas de village préma
        ⭐ Maturité
        ⭐ Actif
        ⭐ Donneur généreux


https://link.clashofclans.com/fr?action=OpenClanProfile&tag=2LV9J8VLQ
'''.format(date=datetime.now().strftime("%d/%m/%Y"), clan_members=clash_data.get_clan_members_count())




#Dictionary of servers with channels
##############################################
servers = [
    ('Clash Champ Fr', 'https://www.discord.com/channels/278653494846685186/280350080895025152'),
    ('Clash Community','https://www.discord.com/channels/475679888981098496/911590761546518529')
]
##############################################


url = "https://www.discord.com/login"

#Edge driver to open browser
driver_path = r"./msedgedriver.exe"

if __name__ == '__main__':
    print(text)
    
    # ser = Service(executable_path=driver_path)
    # driver=webdriver.Edge(service=ser)

    # driver.maximize_window()
    # driver.get("https://www.discord.com/login")
    
    # password_box = driver.find_element(by=By.NAME, value='email').send_keys(username)
    # password_box = driver.find_element(by=By.NAME, value='password').send_keys(password)
    # submit_btn=driver.find_elements(By.TAG_NAME, "button")
    
    # for element in submit_btn:
    #     if element.text == "Iniciar sesión":
    #         button = element

    # webdriver.ActionChains(driver).click_and_hold(button).perform()
    # webdriver.ActionChains(driver).release().perform()
    # sleep(3)
    # main_url = driver.current_url

    # for server in servers:
    #     print(server[1].replace('www.',''))
    #     driver.get(server[1])
        
        
    #     if driver.current_url != server[1].replace('www.',''):
    #         driver.find_element(by=By.NAME, value='email').send_keys(username)
    #         driver.find_element(by=By.NAME, value='password').send_keys(password)
    #         submit_btn=driver.find_elements(By.TAG_NAME, "button")
    #         for element in submit_btn:
    #             if element.text == "Iniciar sesión":
    #                 button = element
    #         webdriver.ActionChains(driver).click_and_hold(driver.find_elements(By.TAG_NAME, "button")).perform()
            
    #         webdriver.ActionChains(driver).release().perform()
        
    #     sleep(6)
    #     driver.execute_script("alert('Hola bombon de melocoton')")
    #     sleep(5)
        
    #     alert = driver._switch_to.alert.accept()
        
   
    

   
    #driver.quit()




    