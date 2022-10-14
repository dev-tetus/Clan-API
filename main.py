import time
from datetime import datetime
from os import path
import sys
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chromium.service import ChromiumService
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait

import classes.utils as utils
import classes.player as p
channels=[
    '📬・recrutement-clan',
    'recrutement_clans',
    '📮・recrutement-clan'
    '⚔clan_cherche_joueurs',
    'les-clans-qui-recrutent',
    
]

if __name__ == '__main__':
    
          
    


    done = False
    base_url_channels = "https://www.discord.com/channels/"

    t = time.localtime()
    text = utils.get_text_with_data()

    url = "https://www.discord.com/login"
    servers = utils.get_server_names_and_channels()

    driver=utils.get_driver()


    driver.get("https://www.discord.com/login")
    driver.maximize_window()

    utils.do_login(driver)
    print('Login done...')
    # servers_to_access = utils.find_servers(driver,servers)
    # print(f'List of servers found:{servers_to_access}')


    try:
        while not done:
            current_time=time.strftime("%H:%M:%S", time.localtime())
            print("Son las ", current_time, ' horas')
            if True:#current_time == '00:20:00':
                for server in servers:
                    driver.get(f'{base_url_channels}{server[0]}/{server[1]}')
                    sleep(5)
                       
                    if 'https://discord.com/login' in driver.current_url:
                        utils.do_login(driver)
                    
                    
                    sleep(5)
                    utils.send_message(driver,text)
                   
                    print('\n############################################\n\t\t\tSent!\n############################################')
            done = True
    except Exception as e:
        print(e)
        print('Exception...')
        driver.quit()
        exit()
    


    
