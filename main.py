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
    '📬・recrutement-clan',
    'recrutement_clans'
]

if __name__ == '__main__':
    done = False


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
        while not done:
            current_time=time.strftime("%H:%M:%S", time.localtime())
            print("Son las ", current_time, ' horas')
            if True:#current_time == '00:20:00':
                for server in servers_to_access:
                    print(server)
                    if 'https://discord.com/login' in driver.current_url:
                        utils.do_login(driver)

                    if server[0] in servers:
                        
                        if server[0] == 'La Souce Family':
                            utils.press_element(driver, server[1])
                            channels = utils.find_channels(driver)
                            for channel in channels:
                                if channel[0] == 'a-l-abris-des-regards':
                                    utils.press_element(driver, channel[1])
                                    sleep(2)
                                    if sys.platform == 'linux':
                                        utils.send_message(driver,f'Messages envoyés à {time.strftime("%H:%M:%S", time.localtime())}')
                                    else:
                                        utils.send_message(driver,f'Messages envoyés à {time.strftime("%H:%M:%S", time.localtime())}')
                        else:
                            utils.press_element(driver, server[1])
                            all_channels = utils.find_channels(driver)
                            print(all_channels)
                            for channel in all_channels:
                                sleep(1)
                                print(channel)
                                if channel[0] in channels:
                                    utils.press_element(driver, channel[1])
                                    if sys.platform == 'linux':
                                        print(f'Channel {channel[0]} is in channels list')
                                        # utils.send_message(driver,text)
                                    else:
                                        utils.send_message(driver,text)
                                        print('\n############################################\n\t\t\tSent!\n############################################')
            done = True
    except Exception as e:
        print(e)
        print('Exception...')
        driver.quit()
        exit()
    


    
