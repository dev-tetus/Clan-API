from urllib import response
import requests
import credentials
import pandas as pd
import numpy as np
import urllib


class ClashData():
    def __init__(self):
        self.credentials = credentials.get_credentials()
        self.headers = {
            'content-type': 'application/json',
            'Authorization': 'Bearer {api}'.format(api=self.credentials["api_key"])
        }
        self.members = self.get_clan_members().__len__()


    def get_clan_members(self):
        response= requests.get(f'{self.credentials["base_url"]}/clans/{self.credentials["clan_tag"]}/members', headers=self.headers)
        print(response)
        return response.json()["items"]

    def get_clan_points(self):
        response=requests.get(f'{self.credentials["base_url"]}/clans/{self.credentials["clan_tag"]}', headers=self.headers)
        return response.json()["clanPoints"]

    def get_clan_level(self):
        response=requests.get(f'{self.credentials["base_url"]}/clans/{self.credentials["clan_tag"]}', headers=self.headers)
        return response.json()["clanLevel"]

    def get_troop_donation_avg(self, limit=None):
        donations = 0
        response= requests.get(f'{self.credentials["base_url"]}/clans/{self.credentials["clan_tag"]}/members?limit={limit if limit else 50}', headers=self.headers)
        for player in response.json()["items"]:
            donations += player["donations"]
        avg = donations/limit if limit else donations/self.members
        return avg

    def get_player_tags(self, limit=None):
        player_tags= []
        response_tags = requests.get(f'{self.credentials["base_url"]}/clans/{self.credentials["clan_tag"]}/members?limit={limit if limit else 50}', headers=self.headers)
        for player_tag in response_tags.json()['items']:
            player_tags.append((player_tag["name"], player_tag["tag"].replace("#","%23")))
        return player_tags
        
    def get_player_info(self,tag=None, DEBUG=False):
        #8YQCLQYG   ;   #2C2U9QCP
        response = requests.get(f'{self.credentials["base_url"]}/players/{"%23982C28QQ" if DEBUG else tag }', headers=self.headers)
        player_troop_levels_dataframe = pd.DataFrame(columns=['name', 'level', 'maxLevel', 'village'])
        username_dataframe = pd.DataFrame([np.array([response.json()['name'], response.json()['townHallLevel']])],columns=['username', 'townHallLevel'])

        for troop in response.json()['troops']:
            troop_df = pd.DataFrame.from_records(troop, index=[0])
            player_troop_levels_dataframe= pd.concat([player_troop_levels_dataframe, troop_df],ignore_index=True, axis=0)
            
        for spell in response.json()['spells']:
            spell_df = pd.DataFrame.from_records(spell, index=[0])
            player_troop_levels_dataframe=pd.concat([player_troop_levels_dataframe, spell_df],ignore_index=True, axis=0)
            
        for hero in response.json()['heroes']:
            hero_df= pd.DataFrame.from_records(hero, index=[0])
            player_troop_levels_dataframe=pd.concat([player_troop_levels_dataframe, hero_df],ignore_index=True, axis=0)

        player_troop_levels_dataframe= player_troop_levels_dataframe[player_troop_levels_dataframe['village'] == 'home']
        player_troop_levels_dataframe= pd.merge(player_troop_levels_dataframe, username_dataframe, how='cross')
        player_troop_levels_dataframe= player_troop_levels_dataframe[player_troop_levels_dataframe.columns.difference(['superTroopIsActive'])]
        return player_troop_levels_dataframe

        
#Debug
if __name__ == '__main__':
    cd = ClashData()
    # print(cd.get_player_info(DEBUG=True))

    print(cd.get_troop_donation_avg())
    
    '''
    print(cd.get_player_info(DEBUG=True))

    '''