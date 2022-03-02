from urllib import response
import requests
import credentials
import pandas as pd
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
        
    def get_player_power_attack(self, player_compos=None, limit=None):
        player_tags = self.get_player_tags(limit)
        player_levels = {}

        for player in player_tags:
            response_levels = requests.get(f'{self.credentials["base_url"]}/players/{player[1]}', headers=self.headers)
    
            player_levels[response_levels.json()["name"]] = {
                "town_hall": response_levels.json()["townHallLevel"],
                "troops": response_levels.json()["troops"],
                "heroes": response_levels.json()["heroes"],
                "spells": response_levels.json()["spells"]
            }

        df = pd.DataFrame.from_dict(player_levels)
        df.to_excel('./player_levels.xlsx', index=False)
        return df

    def get_percentage(self):
        pass
        
#Debug
if __name__ == '__main__':
    
    cd = ClashData()
    print(cd.get_player_power_attack())