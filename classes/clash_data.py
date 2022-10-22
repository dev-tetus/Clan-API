from urllib import response
import requests
import credentials as cred
import pandas as pd
import numpy as np
import urllib


# black_list = ["#8VP0C8GG2","#QYC80YUQG","#L82V99R9V","#29L0VJ2JY"]

class ClashData():
    def __init__(self):
        self.credentials = cred.get_credentials()
        self.headers = {
            'content-type': 'application/json',
            'Authorization': 'Bearer {api}'.format(api=self.credentials["api_key"])
        }
    def get_player_role(self,tag):
        response = requests.get(f'{self.credentials["base_url"]}/players/{tag.replace("#","%23")}', headers=self.headers)
        
        return response.json()['role']
    def get_player_clan(self,tag):
        response = requests.get(f'{self.credentials["base_url"]}/players/{tag.replace("#","%23")}', headers=self.headers)
        return response.json()['clan']['tag']
    def get_clan_level(self):
        response = requests.get(f'{self.credentials["base_url"]}/clans/{self.credentials["clan_tag"]}', headers=self.headers)
        return response.json()['clanLevel']

    def get_win_streak(self):
        response = requests.get(f'{self.credentials["base_url"]}/clans/{self.credentials["clan_tag"]}/warlog', headers=self.headers)
        streak = 0
        for war in response.json()['items']:
            if war['attacksPerMember'] > 1:
                if war['result'] == 'win':
                    streak += 1
                else:
                    if streak == 0:
                        return streak
                    else:
                        return streak
            else:
                continue
        return streak
            

    def get_required_trophies(self):
        response = requests.get(f'{self.credentials["base_url"]}/clans/{self.credentials["clan_tag"]}', headers=self.headers)
        return response.json()['requiredTrophies']
    
    def get_required_townhall(self):
        response = requests.get(f'{self.credentials["base_url"]}/clans/{self.credentials["clan_tag"]}', headers=self.headers)
        return response.json()['requiredTownhallLevel']

    def get_clan_points(self):
        response = requests.get(f'{self.credentials["base_url"]}/clans/{self.credentials["clan_tag"]}', headers=self.headers)
        return response.json()['clanPoints']

    def get_clan_members(self):
        response= requests.get(f'{self.credentials["base_url"]}/clans/{self.credentials["clan_tag"]}/members', headers=self.headers)
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
        members = self.get_clan_members().__len__()
        for player in response.json()["items"]:
            donations += player["donations"]
        avg = int(donations/limit if limit else donations/members)
        return avg

    def get_player_tags(self, limit=None,clan_tag=None):
        player_tags= []
        response_tags = requests.get(f'{self.credentials["base_url"]}/clans/{self.credentials["clan_tag"] if clan_tag==None else clan_tag.replace("#","%23")}/members?limit={limit if limit else 50}', headers=self.headers)
        for player_tag in response_tags.json()['items']:
            player_tags.append((player_tag["name"], player_tag["tag"].replace("#","%23")))
        return player_tags
        
    def get_player_info(self,tag=None, DEBUG=False):
        #8YQCLQYG   ;   #2C2U9QCP   ;   %23GYL2RJQL ;   %2392OV8CRGG    ; %23QV8RP8PGC
        response = requests.get(f'{self.credentials["base_url"]}/players/{"%2329L0VJ2JY" if DEBUG else tag.replace("#","%23") }', headers=self.headers)
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
        player_troop_levels_dataframe= pd.merge(player_troop_levels_dataframe, username_dataframe, how='cross').drop(columns=['village']).rename(columns={"name":"TroopName","maxLevel":"MaxLevel","level":"ActualLevel"})
        # print(player_troop_levels_dataframe)
        player_troop_levels_dataframe= player_troop_levels_dataframe[player_troop_levels_dataframe.columns.difference(['superTroopIsActive'])]
        # print(player_troop_levels_dataframe)
        return player_troop_levels_dataframe

        
#Debug
if __name__ == '__main__':
    cd = ClashData()
    # print(cd.get_player_info(DEBUG=True))

    # print(cd.get_clan_points())

    # print(cd.get_win_streak())
    # cd.get_player_info('%23R2OPRQG8')
    # print(cd.get_clan_level())
    
    cd.get_player_info(DEBUG=True)
    '''

    '''