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

import utils
channels=[
    'recrutement-clan',
    'recrutement_clans'
]

if __name__ == '__main__':
    t = time.localtime()
    text = utils.get_text_with_data()

    url = "https://www.discord.com/login"
    servers = utils.get_server_names()

    driver=utils.get_driver()
    print(driver)
    driver.get("https://www.discord.com/login")
    driver.maximize_window()
    utils.do_login(driver)
    print('Login done...')
    servers_to_access = utils.find_servers(driver,servers)
    print(f'List of servers found:{servers_to_access}')


    try:
        while True:
            current_time=time.strftime("%H:%M:%S", time.localtime())
            print("Son las ", current_time, ' horas')
            if current_time == '20:30:00':
                for server in servers_to_access:
                    print(server)
                    if 'https://discord.com/login' in driver.current_url:
                        utils.do_login(driver)
                                #driver.execute_script(f'alert(\'{server[1]}\');')
                    
                                #driver.switch_to.alert.accept()
                    if server[0] in servers:
                        
                        if server[0] == 'La Souce Family':
                            utils.press_server(driver, server[1])
                            channels = utils.find_channels(driver)
                            for channel in channels:
                                if channel[0] == 'a-l-abris-des-regards' or  channel[0] == 'général':
                                    utils.press_server(driver, channel[1])
                                    
                                    if sys.platform == 'linux':
                                        utils.send_message(driver,f'Messages envoyés à {time.strftime("%H:%M:%S", time.localtime())}')
                                    else:
                                        
                                        utils.send_message(driver,f'Messages envoyés à {time.strftime("%H:%M:%S", time.localtime())}')
                        else:
                            utils.press_server(driver, server[1])
                            channels_server = utils.find_channels(driver)
                            for channel in channels_server:
                                if channel[0] in channels:
                                    utils.press_server(driver, channel[1])
                                    sleep(2)
                                    if sys.platform == 'linux':
                                        utils.send_message(driver,text)
                                    else:
                                        utils.send_message(driver,text)
    except:
        print('Exception...')
        driver.quit()
        exit()
    # driver.quit()
    # exit()



    
