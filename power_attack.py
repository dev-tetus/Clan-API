import os
from zlib import DEF_BUF_SIZE
import pandas as pd
import numpy as np
import json
import credentials

from clash_data import ClashData
#TODO CREATE CLASS 
class ClanPowerAttack():
    def __init__(self):
        self.name = 'couocou'


    def get_lab_levels(self):
        max_lab__per_townhall_dataframe = pd.read_csv(credentials.get_credentials()['buildings_csv'],sep=';',engine=None, usecols=['Name','BuildingLevel','TownHallLevel']).rename(columns={'BuildingLevel': 'LaboratoryLevel'})
        max_lab__per_townhall_dataframe = max_lab__per_townhall_dataframe[max_lab__per_townhall_dataframe["Name"] == "Laboratory"]
        return max_lab__per_townhall_dataframe

    '''
        Returns DataFrame with cols=[Name TroopLevel LaboratoryLevel]
    '''
    def get_troops_max_level_for_laboratory(self):
        troops_df = pd.read_csv(credentials.get_credentials()['troops_csv'],sep=';',engine=None, usecols=['Name', '"TroopLevel"','"LaboratoryLevel"'])  #max troop level per lab level in game
        troops_df = troops_df[troops_df["Name"] != "String"].rename(columns={'"TroopLevel"': 'TroopLevel','"LaboratoryLevel"':'LaboratoryLevel'})
        return troops_df

    def get_spells_max_level_for_laboratory(self):
        spells_df = pd.read_csv(credentials.get_credentials()['spells_csv'],sep=';',engine=None, usecols=['Name','SpellForgeLevel','LaboratoryLevel'])  #max troop level per lab level in game
        
        spells_df = spells_df[spells_df["Name"] != "String"].rename(columns={'SpellForgeLevel': 'SpellLevel'})
        spells_df['Name'] = spells_df["Name"]
        # for i in range(1, len(spells_df)):
        #     if i != 1 and spells_df.loc[i,'Name'] == spells_df.loc[i-1,'Name']: 
        #         spells_df.loc[i,'SpellForgeLevel'] = spells_df.loc[i-1,'SpellForgeLevel'] +1
        
        # troops_df = troops_df[troops_df["Name"] != "String"].rename(columns={'"TroopLevel"': 'TroopLevel','"LaboratoryLevel"':'LaboratoryLevel'})
        return spells_df



    '''
        Returns DataFrame with cols=[BuildingLevel townHallLevel username]
    '''
    def get_max_levels_for_townhall(self,tag=None, DEBUG=False):
        max_lab__per_townhall_dataframe = self.get_lab_levels()
        troops_max_levels_per_lab = self.get_troops_max_level_for_laboratory()
        spells_max_levels_per_lab = self.get_spells_max_level_for_laboratory()
        
        clash_data = ClashData()            
                                                                                                    #PLAYER INFO WITH TAG=tag
        player_info_dataframe = clash_data.get_player_info(tag=tag).drop_duplicates()

                                                                                                    #HEROES FOR TH
        heroes_df=self.get_max_heroes_for_townhall(townHallLevel=player_info_dataframe['townHallLevel'].iloc[0])
        
                                                                                                    #MERGE TO GET ACTUAL LABORATORY LEVEL
        player_max_lab = pd.merge(max_lab__per_townhall_dataframe,player_info_dataframe, how='inner',left_on='TownHallLevel', right_on='townHallLevel').drop(columns=['TownHallLevel','Name','maxLevel','village'])
        
                                                                                                    #MERGE TO GET MAX HERO LEVEL
        player_max_lab_and_heroes = pd.merge(player_max_lab, heroes_df, how='left', right_on=['Name', 'RequiredTownHallLevel'], left_on=['name', 'townHallLevel']).drop(columns=['Name', 'RequiredTownHallLevel']).rename(columns={'Level': 'MaxHeroLevel'})
        
                                                                                                    #MERGE TO GET MAX TROOPS
        player_max_lab_and_heroes=pd.merge(troops_max_levels_per_lab,player_max_lab_and_heroes, how='right', left_on=['LaboratoryLevel','Name'], right_on=['LaboratoryLevel','name'])\
            .rename(columns={'TroopLevel':'MaxLevel','level':'ActualLevel','name':'TroopName','townHallLevel':'TownHall'}).drop(columns=['Name'])

        # player_max_lab_and_heroes=player_max_lab_and_heroes.sort_values(by='username')
        
                                                                                                    # players_with_max_troop_level['PowerAttack'] = players_with_max_troop_level.apply(lambda row:(int(row.ActualLevel)/int(row.MaxLevel))*100, axis=1)
                                                                                                    #SPELLS FOR TH
        player_max_lab_and_heroes=pd.merge(spells_max_levels_per_lab,player_max_lab_and_heroes, how='right', left_on=['Name'], right_on=['TroopName'])
        # unique_spells =player_max_lab_and_heroes['TroopName'].unique()
        # player_max_lab_and_heroes['Name'] =player_max_lab_and_heroes['Name'].unique()
        
        # max_spells_dataframe = pd.DataFrame()
        # for spell in unique_spells:
        #     spell_df = player_max_lab_and_heroes[player_max_lab_and_heroes['Name']==spell]
        #     spell_df =spell_df[spell_df['SpellLevel']==spell_df['SpellLevel'].max()]
        #     max_spells_dataframe = pd.concat([max_spells_dataframe, spell_df])
        
        # return player_max_lab_and_heroes['Name']
        # player_max_lab_and_heroes = player_max_lab_and_heroes.replace(np.NaN,'')
        
        player_max_lab_and_heroes=player_max_lab_and_heroes.groupby('Name')
        
        
        return player_max_lab_and_heroes


    def get_max_heroes_for_townhall(self, townHallLevel):
        max_heroes_per_townhall_dataframe = pd.read_csv(credentials.get_credentials()['heroes_csv'], sep=';',usecols=["Name", "Level","RequiredTownHallLevel"])
        max_heroes_per_townhall_dataframe = max_heroes_per_townhall_dataframe[max_heroes_per_townhall_dataframe["Name"] != "String"]

        #MAX HEROES FOR TOWNHALL
        heroes_with_th= max_heroes_per_townhall_dataframe[max_heroes_per_townhall_dataframe['RequiredTownHallLevel'] == townHallLevel]
        
        unique_heroes =max_heroes_per_townhall_dataframe['Name'].unique()
        
        max_heroes_dataframe = pd.DataFrame()
        for hero in unique_heroes:
            hero_df = heroes_with_th[heroes_with_th['Name']==hero]
            hero_df =hero_df[hero_df['Level']==hero_df['Level'].max()]
            max_heroes_dataframe = pd.concat([max_heroes_dataframe, hero_df])
        
        return max_heroes_dataframe


    def get_players_power_attack(self, player_compos=None, limit=None, DEBUG=False):
        cd = ClashData()
        player_tags = cd.get_player_tags(limit)
        players_levels = pd.DataFrame(columns=['PowerAttack'])
        
        for player in player_tags:
            players_levels=pd.concat([players_levels,self.get_max_levels_for_townhall(tag=player[1])], ignore_index=True)
            
        return players_levels

if __name__ == '__main__':
    cd = ClanPowerAttack()
    # df = cd.get_players_power_attack()
    print(cd.get_max_levels_for_townhall(tag='%238YQCLQYG'))
    # print(df[df['username'] == 'Kirikou'])
    # power_attack=df.loc[df['username'] == r"couscous"].sort_values(by='TroopName')['PowerAttack'].mean(axis='index')
    # print("La puissance d'attaque est:{:.2f}%".format(power_attack,2))
    # pass