import sys
import os

def get_credentials():

    # if sys.platform == "Linux":
    #     f = open('credentials-linux.txt', 'r')
    # else:
    #     f = open('credentials.txt', 'r')
    # content = f.readlines()
    credentials = {
        'username': os.environ['username'],
        'password': os.environ['password'],
        'api_key': os.environ['api_key'],
        'base_url': os.environ['base_url'],
        'clan_tag': os.environ['clan_tag'],
        'spells_csv': os.environ['spells_csv'],
        'troops_csv': os.environ['troops_csv'],
        'heroes_csv': os.environ['heroes_csv'],
        'buildings_csv': os.environ['buildings_csv'],
        'texts_csv': os.environ['texts_csv'],
        'pets_csv': os.environ['pets_csv'],
        'db_ip' : os.environ['db_ip'],
        'db_user' : os.environ['db_user'],
        'db_pass' : os.environ['db_pass'],
    }
    return credentials
