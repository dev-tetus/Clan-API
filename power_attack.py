import os
import pandas as pd
import json
import credentials

from clash_data import ClashData
#TODO CREATE CLASS 
class ClanPowerAttack():
    def __init__(self):
        self.name = 'couocou'

    '''
        Returns DataFrame with cols=[Name TroopLevel LaboratoryLevel]
    '''
    def get_troops_max_level_for_laboratory(self):
        troops_df = pd.read_csv(credentials.get_credentials()['troops_csv'],sep=';',engine=None, usecols=['Name', '"TroopLevel"','"LaboratoryLevel"'])  #max troop level per lab level in game
        troops_df = troops_df[troops_df["Name"] != "String"].rename(columns={'"TroopLevel"': 'TroopLevel','"LaboratoryLevel"':'LaboratoryLevel'})
        return troops_df


    '''
        Returns DataFrame with cols=[BuildingLevel townHallLevel username]
    '''
    def get_max_levels_for_townhall(self,tag=None, DEBUG=False):
        max_lab__per_townhall_dataframe = pd.read_csv(credentials.get_credentials()['buildings_csv'],sep=';',engine=None, usecols=['Name','BuildingLevel','TownHallLevel']).rename(columns={'BuildingLevel': 'LaboratoryLevel'})
        max_lab__per_townhall_dataframe = max_lab__per_townhall_dataframe[max_lab__per_townhall_dataframe["Name"] == "Laboratory"]
        
        #TODO Gather heroes and spells data from .csv and merge to player_max_lab
        # max_heroes_per_townhall_dataframe = pd.read_csv(credentials.get_credentials()['heroes_csv'],sep=';',engine=None, usecols=['Name','Level','TownHallLevel']).rename(columns={'BuildingLevel': 'LaboratoryLevel'}))
        clash_data = ClashData()            #TO SET AS ATTRIBUTE FOR CLASS
        player_info_dataframe = clash_data.get_player_info(tag=tag).drop_duplicates()#drop(columns=['level','maxLevel', 'name', 'village']).drop_duplicates()
        player_max_lab = pd.merge(max_lab__per_townhall_dataframe,player_info_dataframe, how='inner',left_on='TownHallLevel', right_on='townHallLevel').drop(columns=['TownHallLevel','Name','maxLevel','village'])
        return player_max_lab



    def get_players_power_attack(self, player_compos=None, limit=None, DEBUG=False):
        cd = ClashData()
        player_tags = cd.get_player_tags(limit)
        players_levels = pd.DataFrame(columns=['PowerAttack'])
        troops_max_levels_per_lab = self.get_troops_max_level_for_laboratory()

        for player in player_tags:
            #print(player[1])
            players_levels=pd.concat([players_levels,self.get_max_levels_for_townhall(tag=player[1])], ignore_index=True)
            players_with_max_troop_level=pd.merge(troops_max_levels_per_lab,players_levels, how='inner', left_on=['LaboratoryLevel','Name'], right_on=['LaboratoryLevel','name'])
            players_with_max_troop_level= players_with_max_troop_level.sort_values(by='username').rename(columns={'TroopLevel':'MaxLevel','level':'ActualLevel','name':'TroopName','townHallLevel':'TownHall'}).drop(columns=['Name'])
        players_with_max_troop_level['PowerAttack'] = players_with_max_troop_level.apply(lambda row:(int(row.ActualLevel)/int(row.MaxLevel))*100, axis=1)
        if DEBUG:
            pass
            # player_list = pd.DataFrame.from_dict(player_levels)

            # player_list.to_json('./DEBUG/clan_players_troop_levels.json')
        
        # df.to_excel('./player_levels.xlsx', index=False)
        return players_with_max_troop_level

if __name__ == '__main__':
    cd = ClanPowerAttack()
    df = cd.get_players_power_attack()
    power_attack=df.loc[df['username'] == r"couscous"].sort_values(by='TroopName')['PowerAttack'].mean(axis='index')
    print("La puissance d'attaque est:{:.2f}%".format(power_attack,2))
    pass