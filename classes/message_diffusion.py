import time
from time import sleep



import utils as utils
import player as p

class MessageDiffusion():


    def __init__(self):

        self.channels=[
            '📬・recrutement-clan',
            'recrutement_clans',
            '📮・recrutement-clan'
            '⚔clan_cherche_joueurs',
            'les-clans-qui-recrutent',   
        ]
        self.base_url_channels = "https://www.discord.com/channels/"
        self.text = utils.get_text_with_data()
        self.t = time.localtime()
        self.url = "https://www.discord.com/login"
        self.servers = utils.get_server_names_and_channels()
        self.driver=utils.get_driver()
    
    def start_diffusion(self):
        self.driver.get("https://www.discord.com/login")
        self.driver.maximize_window()

        utils.do_login(self.driver)
        print('Login done...')
        try:
            current_time=time.strftime("%H:%M:%S", time.localtime())
            print("Son las ", current_time, ' horas')
            for server in self.servers:
                self.driver.get(f'{self.base_url_channels}{server[0]}/{server[1]}')
                sleep(5)
                if 'https://discord.com/login' in self.driver.current_url:
                    utils.do_login(self.driver)
                sleep(5)
                utils.send_message(self.driver,self.text)
                print('\n############################################\n\t\t\tSent!\n############################################')
            return 1
        except Exception as e:
            print(e)
            print('Exception...')
            self.driver.quit()
        


    
