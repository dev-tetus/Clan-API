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

import utils


if __name__ == '__main__':

    url = "https://www.discord.com/login"
    servers = utils.get_server_names()

    driver=utils.get_driver()
    print(driver)

    
    driver.maximize_window()
    driver.get("https://www.discord.com/login")
    
    utils.do_login(driver)
    sleep(2)
    print('Login done...')
    servers_to_access = utils.find_servers(driver,servers)
    print(servers_to_access)

    for server in servers_to_access:
        print(server)
        if 'https://discord.com/login' in driver.current_url:
            utils.do_login(driver)
                    #driver.execute_script(f'alert(\'{server[1]}\');')
        sleep(2)
                    #driver.switch_to.alert.accept()
        if server[0] == 'La Souce Family':
            utils.press_server(driver, server[1])
            driver.execute_script(r'alert("J\'envoie une alerte!!!");')
            sleep(3)
            driver.switch_to.alert.accept()
            channels = utils.find_channels(driver)
            print(channels)
            for channel in channels:
                if channel[0] == 'général':
                    utils.press_server(driver, channel[1])
                    sleep(2)
                    if sys.platform == 'linux':
                        utils.send_message(driver,"Message depuis raspberry!")
                    else:
                        utils.send_message(driver,"Groooos pdd")
            


            
            # driver.get("https://discord.com/channels/677188056616402945/677188057417646113")
        
            

    
    driver.quit()
    exit()



    
