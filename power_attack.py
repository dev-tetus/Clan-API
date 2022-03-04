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
    def get_max_lab_for_townhall(self):
        max_lab__per_townhall_dataframe = pd.read_csv(credentials.get_credentials()['buildings_csv'],sep=';',engine=None, usecols=['Name','BuildingLevel','TownHallLevel'])
        max_lab__per_townhall_dataframe = max_lab__per_townhall_dataframe[max_lab__per_townhall_dataframe["Name"] == "Laboratory"]
        clash_data = ClashData()            #TO SET AS ATTRIBUTE FOR CLASS
        player_info_dataframe = clash_data.get_player_info(DEBUG=True).drop(columns=['level','maxLevel', 'name', 'village']).drop_duplicates()
        player_max_lab = pd.merge(max_lab__per_townhall_dataframe,player_info_dataframe, how='inner',left_on='TownHallLevel', right_on='townHallLevel').drop(columns=['TownHallLevel','Name'])
        return player_max_lab


    def get_players_power_attack(self, player_compos=None, limit=None, DEBUG=False):
        cd = ClashData()
        player_tags = cd.get_player_tags(limit)
        player_levels = {}

        for player in player_tags:
            response_levels = cd.get_player_info(tag=player[1])
                                                                    #TODO Merge lab_max_level for townHallLevel & troop_max_level for lab_max_level
            
            merge_lab_max=pd.merge(response_levels, self.get_max_lab_for_townhall(),how='inner', on='townHallLevel')
        if DEBUG:
            pass
            # player_list = pd.DataFrame.from_dict(player_levels)

            # player_list.to_json('./DEBUG/clan_players_troop_levels.json')
        
        # df.to_excel('./player_levels.xlsx', index=False)
        return merge_lab_max

if __name__ == '__main__':
    cd = ClanPowerAttack()
    print(cd.get_players_power_attack())
    pass