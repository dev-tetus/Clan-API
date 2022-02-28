import asyncio
import logging
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.relative_locator import locate_with



url = "https://www.google.com"

driver_path = r"./msedgedriver.exe"
browser_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"

#Set-up chrome driver

# options = webdriver.ChromeOptions()


# options.binary_location = browser_path
# options.add_argument(r'--user-data-dir=D:\Dev\Proyectos\discord-scraping\discord-env\Profile 2')
# options.add_argument("--profile-directory=Profile 2")


mail = 'tefilorofi@hotmail.com'
password = 'Teoroca1998$'


if __name__ == '__main__':
    ser = Service(executable_path=driver_path)
    driver=webdriver.Edge(service=ser)
    driver.get("https://www.discord.com/login")
    password_box = driver.find_element(by=By.NAME, value='email').send_keys("tetusrocus")
    password_box = driver.find_element(by=By.NAME, value='password')
    webdriver.ActionChains(driver).context_click(password_box).perform()
    password_box.send_keys("cacacaca")
    # submit_btn=driver.find_element(By.XPATH("//*[@id=app-mount]/div[2]/div/div/div/div/form/div/div/div[1]/div[2]/button[2]"))
    submit_btn=driver.find_elements(By.TAG_NAME, "button")
    for element in submit_btn:
        if element.text == "Iniciar sesión":
            button = element
    webdriver.ActionChains(driver).click_and_hold(button).perform()
    webdriver.ActionChains(driver).release().perform()

    # driver.quit()




    