import sys
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
from credentials import get_credentials


def press_server(driver, element):
    webdriver.ActionChains(driver).click_and_hold(element).perform()
    webdriver.ActionChains(driver).release().perform()


def get_server_names():
    return [
        ('Clash of Clans Français 🇫🇷'),
        ('Clash Community'),
        ('La Souce Family')
    ]

def find_channels(driver):
    channels= []
    channels_availables = WebDriverWait(driver, 20).until(
    EC.presence_of_all_elements_located((By.XPATH, "//*[@id='channels']/ul/li/div/div/a/div[2]/div")))
    for channel_clickable in channels_availables:
        channels.append((channel_clickable.text,channel_clickable))
    return channels

def find_servers(driver, server_names):
    servers_to_send = []
    servers_availables = WebDriverWait(driver, 20).until(
    EC.presence_of_all_elements_located((By.XPATH, "//div[@role='treeitem']")))

    for server_clickable in servers_availables:
        if server_clickable.get_attribute("aria-label").strip() in server_names:
            servers_to_send.append((server_clickable.get_attribute("aria-label").strip(), server_clickable))
    return servers_to_send

def send_message(driver, text):
    action = webdriver.ActionChains(driver)
    # input_box = driver.find_element(by=By.CSS_SELECTOR, value=r'#app-mount > div.app-3xd6d0 > div > div.layers-OrUESM.layers-1YQhyW > div > div > div > div > div.chat-2ZfjoI > div.content-1jQy2l > main > form > div > div > div > div.scrollableContainer-15eg7h.webkit-QgSAqd > div > div.textArea-2CLwUE.textAreaSlate-9-y-k2.slateContainer-3x9zil > div.markup-eYLPri.slateTextArea-27tjG0.fontSize16Padding-XoMpjI > div')
    action.send_keys(f'{text}').key_down(Keys.ENTER).key_up(Keys.ENTER).perform()

#app-mount > div.app-3xd6d0 > div > div.layers-OrUESM.layers-1YQhyW > div > div > div > div > div.chat-2ZfjoI > div.content-1jQy2l > main > form > div > div > div > div.scrollableContainer-15eg7h.webkit-QgSAqd > div > div.textArea-2CLwUE.textAreaSlate-9-y-k2.slateContainer-3x9zil > div.markup-eYLPri.slateTextArea-27tjG0.fontSize16Padding-XoMpjI > div > span > span > span

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
        edge_options.add_experimental_option("detach", True)
        ser = EdgeService(executable_path="./msedgedriver.exe")
        return webdriver.Edge(service=ser, options=edge_options)
     
     


def do_login(driver):
    driver.find_element(by=By.NAME, value='email').send_keys(get_credentials()['username'])
    driver.find_element(by=By.NAME, value='password').send_keys(get_credentials()['password'])
    # button = WebDriverWait(driver, 20).until(
    #     EC.presence_of_all_elements_located((By.CSS_SELECTOR, r'#app-mount > div.app-3xd6d0 > div > div > div > div > form > div > div > div.mainLoginContainer-wHmAjP > div.block-3uVSn4.marginTop20-2T8ZJx > button.marginBottom8-emkd0_.button-1cRKG6.button-f2h6uQ.lookFilled-yCfaCM.colorBrand-I6CyqQ.sizeLarge-3mScP9.fullWidth-fJIsjq.grow-2sR_-F')))
    # button = driver.find_element(by=By.CSS_SELECTOR, value=r'#app-mount > div.app-3xd6d0 > div > div > div > div > form > div > div > div.mainLoginContainer-wHmAjP > div.block-3uVSn4.marginTop20-2T8ZJx > button.marginBottom8-emkd0_.button-1cRKG6.button-f2h6uQ.lookFilled-yCfaCM.colorBrand-I6CyqQ.sizeLarge-3mScP9.fullWidth-fJIsjq.grow-2sR_-F')
    for element in driver.find_elements(By.TAG_NAME, "button"):
        if element.text == "Iniciar sesión":
             button = element
    webdriver.ActionChains(driver).click_and_hold(button).perform()
    webdriver.ActionChains(driver).release().perform()


def get_text_with_data():
    cd = ClashData()
    with open("text.txt","r", encoding='UTF-8') as f2:
        return f2.read()\
            .replace(r'{date}',datetime.now()\
            .strftime("%d/%m/%Y"))\
            .replace(r'{clan_members}',str(cd.members))\
        

#Debug
if __name__ == '__main__':
    print(get_text_with_data())
