import pandas as pd
import numpy as np
import credentials

from clash_data import ClashData

pd.options.display.float_format = "{:,.2f}".format

class ClanPowerAttack():
    def __init__(self):
        self.name = 'couocou'
        self.super_troops = ['Super Barbarian',
        'Super Archer',
        'Super Wall Breaker',
        'Super Giant',
        'Sneaky Goblin',
        'Inferno Dragon',
        'Super Valkyrie',
        'Super Witch',
        'Super Bowler',
        'Super Dragon',
        'Super Wizard',
        'Super Minion',
        'Rocket Balloon',
        'Ice Hound']

    def get_traduction(self):
        text_df = pd.read_csv(credentials.get_credentials()['texts_csv'],sep=';', engine=None, usecols=['TID', 'EN'])
        troops_df = pd.read_csv(credentials.get_credentials()['troops_csv'],sep=';', engine=None, usecols=['Name', '"TID"', '"ProductionBuilding"']).rename(columns={'"TID"': 'TID','"ProductionBuilding"': 'ProductionBuilding'})

        troops_df['TID'] = troops_df['TID'].str.strip('"')
        troops_df['ProductionBuilding'] = troops_df['ProductionBuilding'].str.strip('"')
        troops_df = troops_df[(troops_df['ProductionBuilding'] == 'Barrack') | (troops_df['ProductionBuilding'] == 'Dark Elixir Barrack')]
        # print(troops_df[troops_df['TID'] == 'TID_BARBARIAN'])
        # print(text_df[text_df['TID'] == 'TID_BARBARIAN'])
        traduction = pd.merge(text_df, troops_df, how='inner')

        return traduction.drop(columns=['TID','Name']).drop_duplicates(ignore_index=True).rename(columns={'EN':'TroopName'})

    def get_lab_levels(self):

        max_lab__per_townhall_dataframe = pd.read_csv(credentials.get_credentials()['buildings_csv'],sep=';',engine=None, usecols=['Name','BuildingLevel','TownHallLevel']).rename(columns={'BuildingLevel': 'LaboratoryLevel'})
        max_lab__per_townhall_dataframe = max_lab__per_townhall_dataframe[max_lab__per_townhall_dataframe["Name"] == "Laboratory"]

        return max_lab__per_townhall_dataframe

    def get_locked_troops(self, player_info_dataframe):
        text_df = pd.read_csv(credentials.get_credentials()['texts_csv'],sep=';', engine=None, usecols=['TID', 'EN'])
        troops_df = pd.read_csv(credentials.get_credentials()['troops_csv'],sep=';', engine=None, usecols=['Name', '"TID"', '"ProductionBuilding"', '"TroopLevel"', 'DisableDonate','IsSecondaryTroop','"BarrackLevel"','"LaboratoryLevel"','"VillageType"']).rename(columns={'"TID"': 'TID','"ProductionBuilding"': 'ProductionBuilding','"TroopLevel"':'TroopLevel','"BarrackLevel"':'BarrackLevel','"LaboratoryLevel"':'LaboratoryLevel','"VillageType"':'VillageType'})

        troops_df['VillageType'] = troops_df['VillageType'].str.strip('"')
        troops_df = troops_df[(troops_df['VillageType'] == 'int') | (troops_df['VillageType'] == '0')]
        troops_df['TID'] = troops_df['TID'].str.strip('"')
        troops_df['ProductionBuilding'] = troops_df['ProductionBuilding'].str.strip('"')
        troops_df = troops_df[(troops_df['ProductionBuilding'] == 'Barrack') | (troops_df['ProductionBuilding'] == 'Dark Elixir Barrack')]

        traduction = pd.merge(text_df, troops_df, how='inner')
        locked_troops = pd.merge(traduction, player_info_dataframe[player_info_dataframe['ProductionBuilding'].isnull()], how='inner', left_on='Name', right_on='TroopName').drop(columns=['TID','EN','Name'])

        actual_max_barrack_level =  player_info_dataframe['BarrackLevel'].unique()[0]
        actual_max_dark_barrack_level = player_info_dataframe['DarkBarrackLevel'].unique()[0]
        actual_townhall_level = player_info_dataframe['TownHallLevel'].unique()[0]
        username=player_info_dataframe['username'].unique()[0]

        locked_troops['LaboratoryLevel'] = locked_troops['LaboratoryLevel'].astype(np.float64)
        locked_troops['BarrackLevel_x'] = locked_troops['BarrackLevel_x'].astype(np.float64)

        for locked_troop in locked_troops['TroopName'].unique():

            if (locked_troops[locked_troops['TroopName'] == locked_troop]['IsSecondaryTroop'].unique()[0] == 'true') or (locked_troops[locked_troops['TroopName'] == locked_troop]['DisableDonate'].unique()[0] == 'TRUE'):
                continue
            else:
                if locked_troops[locked_troops['TroopName'] == locked_troop]['ProductionBuilding_x'].unique()[0] == 'Barrack':

                    troop_min_barrack_level = locked_troops[locked_troops['TroopName'] == locked_troop]['BarrackLevel_x'].values.tolist()[0]

                    if troop_min_barrack_level <= np.float64(actual_max_barrack_level):

                        actual_player_lab = player_info_dataframe['ActualLab'].values.tolist()[0]
                        print(f'player_lab: {actual_player_lab}')
                        actual_max_troop_level = player_info_dataframe[player_info_dataframe['TroopName'] == locked_troop]['MaxLevel'].values.tolist()[0]

                        player_info_dataframe.loc[(player_info_dataframe["TroopName"] == locked_troop), "ProductionBuilding"] = 'Barrack'
                        player_info_dataframe.loc[(player_info_dataframe["TroopName"] == locked_troop), "ActualLab"] = actual_player_lab
                        player_info_dataframe.loc[(player_info_dataframe["TroopName"] == locked_troop), "TownHallLevel"] = actual_townhall_level
                        player_info_dataframe.loc[(player_info_dataframe["TroopName"] == locked_troop), "DarkBarrackLevel"] = actual_max_dark_barrack_level
                        player_info_dataframe.loc[(player_info_dataframe["TroopName"] == locked_troop), "BarrackLevel"] = actual_max_barrack_level
                        player_info_dataframe.loc[(player_info_dataframe["TroopName"] == locked_troop), "level"] = '0'
                        player_info_dataframe.loc[(player_info_dataframe["TroopName"] == locked_troop), "name"] = locked_troop
                        player_info_dataframe.loc[(player_info_dataframe["TroopName"] == locked_troop), "username"] = username

                        for lab_level in locked_troops[locked_troops['TroopName'] == locked_troop]['LaboratoryLevel'].unique():

                            if np.float64(lab_level) <= np.float64(actual_player_lab):

                                new_level=locked_troops.loc[(locked_troops["TroopName"] == locked_troop) & (locked_troops["LaboratoryLevel"] == lab_level)]['TroopLevel'].max()
                                print(new_level)

                                if actual_max_troop_level < np.float64(new_level):

                                    player_info_dataframe.loc[(player_info_dataframe["TroopName"] == locked_troop), "MaxLevel"] = np.float64(new_level)

                else:
                    troop_min_barrack_level = locked_troops[locked_troops['TroopName'] == locked_troop]['BarrackLevel_x'].values.tolist()[0]

                    if troop_min_barrack_level <= np.float64(actual_max_dark_barrack_level):

                        actual_player_lab = player_info_dataframe['ActualLab'].values.tolist()[0]
                        print(f'player_lab: {actual_player_lab}')
                        actual_max_troop_level = player_info_dataframe[player_info_dataframe['TroopName'] == locked_troop]['MaxLevel'].values.tolist()[0]

                        player_info_dataframe.loc[(player_info_dataframe["TroopName"] == locked_troop), "ProductionBuilding"] = 'Barrack'
                        player_info_dataframe.loc[(player_info_dataframe["TroopName"] == locked_troop), "ActualLab"] = actual_player_lab
                        player_info_dataframe.loc[(player_info_dataframe["TroopName"] == locked_troop), "TownHallLevel"] = actual_townhall_level
                        player_info_dataframe.loc[(player_info_dataframe["TroopName"] == locked_troop), "DarkBarrackLevel"] = actual_max_dark_barrack_level
                        player_info_dataframe.loc[(player_info_dataframe["TroopName"] == locked_troop), "BarrackLevel"] = actual_max_barrack_level
                        player_info_dataframe.loc[(player_info_dataframe["TroopName"] == locked_troop), "level"] = '0'
                        player_info_dataframe.loc[(player_info_dataframe["TroopName"] == locked_troop), "name"] = locked_troop
                        player_info_dataframe.loc[(player_info_dataframe["TroopName"] == locked_troop), "username"] = username

                        for lab_level in locked_troops[locked_troops['TroopName'] == locked_troop]['LaboratoryLevel'].unique():

                            if np.float64(lab_level) <= np.float64(actual_player_lab):

                                new_level=locked_troops.loc[(locked_troops["TroopName"] == locked_troop) & (locked_troops["LaboratoryLevel"] == lab_level)]['TroopLevel'].max()
                                print(new_level)

                                if actual_max_troop_level < np.float64(new_level):

                                    player_info_dataframe.loc[(player_info_dataframe["TroopName"] == locked_troop), "MaxLevel"] = np.float64(new_level)

        player_info_dataframe= player_info_dataframe.dropna(subset=['ActualLab']).drop(columns=['TroopName'])
        return player_info_dataframe

        # player_actual_lab = player_info_dataframe['ActualLab'].unique()[0]
        # player_actual_townhall = player_info_dataframe['TownHallLevel'].unique()[0]
        # player_actual_dark_barrack = player_info_dataframe['DarkBarrackLevel'].unique()[0]
        # player_actual_barrack = player_info_dataframe['BarrackLevel'].unique()[0]


        # return type(player_actual_lab)







    def get_max_barrack_level(self,player_info_dataframe):

        barracks_dataframe = pd.read_csv(credentials.get_credentials()['buildings_csv'],sep=';',engine=None, usecols=['Name','BuildingLevel','TownHallLevel']).rename(columns={'BuildingLevel': 'BarrackLevel'})
        
        max_barrack__per_townhall_dataframe = barracks_dataframe[(barracks_dataframe["Name"] == "Barrack")]
        max_dark_barrack_per_townhall_dataframe =  barracks_dataframe[barracks_dataframe["Name"] == 'Dark Elixir Barrack']

        player_info_dataframe = pd.merge(max_barrack__per_townhall_dataframe, player_info_dataframe, how="right",left_on='TownHallLevel', right_on='townHallLevel')#.drop(columns=['Name','TownHallLevel'])
        player_info_dataframe = pd.merge(max_dark_barrack_per_townhall_dataframe, player_info_dataframe, how="right",left_on='TownHallLevel', right_on='townHallLevel').drop(columns=['TownHallLevel_x','TownHallLevel_y']).rename(columns={'BarrackLevel_x':'DarkBarrackLevel','Name_x':'Dark Elixir Barrack','Name_y':'Barrack','BarrackLevel_y':'BarrackLevel'})

        return player_info_dataframe

    def get_troops_for_max_barrack(self,barrack_level,dark_barrack_level):
        troops_df = pd.read_csv(credentials.get_credentials()['troops_csv'],sep=';',engine=None, usecols=['Name', '"TroopLevel"','"LaboratoryLevel"','"TID"', '"BarrackLevel"','"VillageType"','"ProductionBuilding"'])  #max troop level per lab level in game
        troops_df['"TID"'] = troops_df['"TID"'].str.strip('"')
        troops_df['"VillageType"'] = troops_df['"VillageType"'].str.strip('"')
        troops_df['"ProductionBuilding"'] = troops_df['"ProductionBuilding"'].str.strip('"')
        troops_df = troops_df[(troops_df['"ProductionBuilding"'] == 'Barrack') | (troops_df['"ProductionBuilding"'] == 'Dark Elixir Barrack')]
        troops_df = troops_df[(troops_df['"VillageType"'] == 'int') | (troops_df['"VillageType"'] == '0')]

        texts_df = pd.read_csv(credentials.get_credentials()['texts_csv'], sep=';', engine=None, usecols=['TID','EN'])
        troops_df = pd.merge(troops_df,texts_df, left_on='"TID"', right_on='TID').drop(columns=['Name', '"TID"', 'TID','"VillageType"']).rename(columns={'EN': 'TroopName','"TroopLevel"':'TroopLevel', '"LaboratoryLevel"': 'LaboratoryLevel','"BarrackLevel"':'BarrackLevel','"ProductionBuilding"':'ProductionBuilding'})

        unique_troops= troops_df['TroopName'].unique()
        # print('Here',unique_troops)


        troops_df['BarrackLevel'] = troops_df['BarrackLevel'].astype(np.float64)

        available_troops = pd.DataFrame(columns=['TroopLevel','LaboratoryLevel','BarrackLevel', 'TroopName'])

        for troop in unique_troops:
            if troops_df[troops_df['TroopName'] == troop]['ProductionBuilding'].unique()[0] == 'Dark Elixir Barrack':

                for max_barrack_level in troops_df[troops_df['TroopName'] == troop]['BarrackLevel'].nlargest(n=50):

                    if max_barrack_level <= np.float64(dark_barrack_level):

                        available_troops= pd.concat([available_troops, troops_df[troops_df['TroopName'] == troop]])
            else:

                for max_barrack_level in troops_df[troops_df['TroopName'] == troop]['BarrackLevel'].nlargest(n=50):

                    if max_barrack_level <= int(barrack_level):

                        available_troops= pd.concat([available_troops, troops_df[troops_df['TroopName'] == troop]])
        
        return available_troops

    def get_troops_max_level_for_laboratory(self):
        troops_df = pd.read_csv(credentials.get_credentials()['troops_csv'],sep=';',engine=None, usecols=['Name', '"TroopLevel"','"LaboratoryLevel"','"TID"', '"BarrackLevel"'])  #max troop level per lab level in game
        troops_df['"TID"'] = troops_df['"TID"'].str.strip('"')
        # print(troops_df)
        texts_df = pd.read_csv(credentials.get_credentials()['texts_csv'], sep=';', engine=None, usecols=['TID','EN'])
        # print(texts_df[texts_df['EN'] == 'Hog Rider'])
        troops_df = pd.merge(troops_df,texts_df, left_on='"TID"', right_on='TID').drop(columns=['Name', '"TID"', 'TID']).rename(columns={'EN': 'TroopName','"TroopLevel"':'TroopLevel', '"LaboratoryLevel"': 'LaboratoryLevel','"BarrackLevel"':'BarrackLevel'})
        # print(troops_df[troops_df['TroopName'] == 'Hog Rider'])
        return troops_df

    def get_spells_max_level_for_laboratory(self):
        spells_df = pd.read_csv(credentials.get_credentials()['spells_csv'],sep=';',engine=None, usecols=['Name','SpellForgeLevel','LaboratoryLevel','ProductionBuilding','DisableProduction','TID'])  #max troop level per lab level in game
        texts_df = pd.read_csv(credentials.get_credentials()['texts_csv'], sep=';',engine=None, usecols=['TID','EN'])

        spells_df = spells_df[spells_df["Name"] != "String"].rename(columns={'SpellForgeLevel': 'SpellLevel'})
        spells_df = spells_df[(spells_df["ProductionBuilding"] == "Spell Forge") | (spells_df["ProductionBuilding"] == "Mini Spell Factory")]
        spells_df["DisableProduction"] = spells_df["DisableProduction"].str.lower()
        spells_df = spells_df[spells_df["DisableProduction"] != 'true']
        spells_df = pd.merge(spells_df,texts_df, how='inner',left_on='TID', right_on='TID').drop(columns=['Name','TID','DisableProduction']).rename(columns={'EN':'Name'})

        # print(spells_df[spells_df['Name'] == 'Bat Spell'])
        return spells_df

    def get_max_troop_level_for_lab_player(self,max_troops_per_lab, player_info_dataframe, super_troops_available):
        player_info_dataframe['MaxLevel'] = 0
        only_troops = pd.merge(max_troops_per_lab, player_info_dataframe, how='inner',left_on=['TroopName'], right_on=['TroopName'])#.drop(columns=['TroopName','townHallLevel'])
        unique_troops= only_troops['TroopName'].unique()

        
        max_troops_per_lab['LaboratoryLevel'] = pd.to_numeric(max_troops_per_lab['LaboratoryLevel'], errors='coerce')
        max_troops_per_lab = max_troops_per_lab.dropna(subset=['LaboratoryLevel'])
        max_troops_per_lab['LaboratoryLevel'] = max_troops_per_lab['LaboratoryLevel'].astype(np.float64)
        max_troops_per_lab = max_troops_per_lab.drop_duplicates()
        player_info_dataframe['ActualLab'] = player_info_dataframe['ActualLab'].astype(np.float64)
        player_info_dataframe = player_info_dataframe.drop_duplicates()
        try:
            for troop in unique_troops:
       
                for max_lab_level in max_troops_per_lab[max_troops_per_lab['TroopName'] == troop]['LaboratoryLevel'].nlargest(n=50):

                    if player_info_dataframe[player_info_dataframe['TroopName'] == troop]['ActualLab'].max() >= max_lab_level:


                        new_level = max_troops_per_lab.loc[(max_troops_per_lab["TroopName"] == troop) & (max_troops_per_lab["LaboratoryLevel"] == max_lab_level)]['TroopLevel'].max()

                        maximum_actual_level=player_info_dataframe.loc[player_info_dataframe['TroopName'] == troop]['MaxLevel'].values.tolist()[0]

                        if troop in self.super_troops:
                            if troop in super_troops_available['SuperTroopName'].unique():
                                if  maximum_actual_level < int(new_level):
                                    player_info_dataframe.loc[(player_info_dataframe["TroopName"] == troop), "MaxLevel"] = int(new_level)
                            else:
                                player_info_dataframe.loc[(player_info_dataframe["TroopName"] == troop), "MaxLevel"] = -1
                        else:
                            if maximum_actual_level < int(new_level):
                                player_info_dataframe.loc[(player_info_dataframe["TroopName"] == troop), "MaxLevel"] = int(new_level)
                        
                    else:
                        player_info_dataframe.loc[(player_info_dataframe["TroopName"] == troop), "MaxLevel"] = -1
            return player_info_dataframe.drop(columns=['TroopLevel', 'LaboratoryLevel']).drop_duplicates()
        except:
            return player_info_dataframe.drop(columns=['TroopLevel','LaboratoryLevel']).drop_duplicates()
        
    def get_max_spell_level_for_lab_player(self, spells_max_levels_per_lab, only_troops_df,player_info_dataframe):
        only_spells = pd.merge(spells_max_levels_per_lab, player_info_dataframe, how='inner',left_on=['Name'], right_on=['name'])
        unique_spells = spells_max_levels_per_lab['Name'].unique()


        spells_max_levels_per_lab['LaboratoryLevel'] = pd.to_numeric(spells_max_levels_per_lab['LaboratoryLevel'], errors='coerce')
        spells_max_levels_per_lab = spells_max_levels_per_lab.dropna(subset=['LaboratoryLevel'])
        spells_max_levels_per_lab['LaboratoryLevel'] = spells_max_levels_per_lab['LaboratoryLevel'].astype(np.float64)
        spell_dataframe = pd.DataFrame()
       
        actual_player_lab = only_troops_df['ActualLab'].values.tolist()[0]

        for spell in unique_spells:
            spell_dataframe=player_info_dataframe.loc[player_info_dataframe['name'] == spell]

            only_troops_df = pd.concat([only_troops_df, spell_dataframe])
            only_troops_df.loc[(only_troops_df["name"] == spell), "MaxLevel"] = -1

            if not spell_dataframe.empty:
                only_troops_df.loc[(only_troops_df['name'] == spell), 'ProductionBuilding'] = only_spells[only_spells['name'] == spell]['ProductionBuilding'].unique()[0]
                
                for max_lab_level in spells_max_levels_per_lab[spells_max_levels_per_lab['Name'] == spell]['LaboratoryLevel'].nlargest(n=50):
                    if actual_player_lab >= max_lab_level:

                        new_level = spells_max_levels_per_lab.loc[(spells_max_levels_per_lab["Name"] == spell) & (spells_max_levels_per_lab["LaboratoryLevel"] == max_lab_level)]['SpellLevel'].max()
                        
                        maximum_actual_level=only_troops_df.loc[(only_troops_df["name"] == spell), "MaxLevel"].values.tolist()[0]
                        # print(f'spell:{spell} | lab_level:{max_lab_level} | player_lab:{actual_player_lab} | new_spell_level:{new_level} | maximum_actual_level:{maximum_actual_level}')

                        if  maximum_actual_level < int(new_level):

                            only_troops_df.loc[(only_troops_df["name"] == spell), "MaxLevel"] = int(new_level)
                            only_troops_df.loc[(only_troops_df["name"] == spell), "ActualLab"] = int(actual_player_lab)
                            # print(only_troops_df[only_troops_df["name"] == spell])
            else:
                continue
        only_troops = only_troops_df.drop_duplicates().drop(columns=['Name','LaboratoryLevel','townHallLevel']).reset_index(drop=True)
        return only_troops

    def get_max_heroes_for_townhall_player(self, only_troops_df, player_info_dataframe):

        townHall_level=player_info_dataframe['townHallLevel'].iloc[0]
        dark_barrack_level=player_info_dataframe['DarkBarrackLevel'].iloc[0]
        barrack_level=player_info_dataframe['BarrackLevel'].iloc[0]
        player_lab_level=only_troops_df['ActualLab'].iloc[0]
        player_username=player_info_dataframe['username'].iloc[0]

        max_heroes_per_townhall = pd.read_csv(credentials.get_credentials()['heroes_csv'], sep=';',usecols=["Name", "Level","RequiredTownHallLevel","VillageType"])
        max_heroes_per_townhall = max_heroes_per_townhall[(max_heroes_per_townhall["Name"] != "String") & (max_heroes_per_townhall["VillageType"] != '1')].drop(columns=['VillageType']).rename(columns={'Name':'name'})
        max_heroes_per_townhall['Level'] = max_heroes_per_townhall['Level'].astype(np.float64)

        heroes_with_th= max_heroes_per_townhall[max_heroes_per_townhall['RequiredTownHallLevel'] == townHall_level]
        only_heroes = pd.merge(heroes_with_th, player_info_dataframe, how='inner', left_on='name', right_on='name')
        unique_heroes =only_heroes['name'].unique()
        hero_df = pd.DataFrame()



        for hero in unique_heroes:

            actual_level = player_info_dataframe[player_info_dataframe['name'] == hero]['level'].unique()[0]
            hero_df = heroes_with_th[heroes_with_th['name']==hero]
            hero_df =hero_df[hero_df['Level']==hero_df['Level'].max()]

            only_troops_df = pd.concat([only_troops_df, hero_df])
            only_troops_df.loc[(only_troops_df["name"] == hero), "MaxLevel"] = hero_df['Level'].iloc[0]
            only_troops_df.loc[(only_troops_df["name"] == hero), "level"] = actual_level
            only_troops_df.loc[(only_troops_df["name"] == hero), "ActualLab"] = player_lab_level
            only_troops_df.loc[(only_troops_df["name"] == hero), "TownHallLevel"] = townHall_level
            only_troops_df.loc[(only_troops_df["name"] == hero), "DarkBarrackLevel"] = dark_barrack_level
            only_troops_df.loc[(only_troops_df["name"] == hero), "BarrackLevel"] = barrack_level
            only_troops_df.loc[(only_troops_df["name"] == hero), "username"] = player_username
            only_troops_df.loc[(only_troops_df["name"] == hero), "ProductionBuilding"] = 'None'
        try:

            return only_troops_df.drop(columns=['Level','RequiredTownHallLevel'])

        except:
            return only_troops_df

    def get_super_troops_if_possible(self,player_info_dataframe):

        troops_df = pd.read_csv(credentials.get_credentials()['troops_csv'], sep=';', engine=None, usecols=['Name','"TroopLevel"'])

        super_troops_df = pd.read_csv(credentials.get_credentials()['super_troops_csv'], sep=';',engine=None, usecols=['Name','MinOriginalLevel','Original','Replacement'])
        super_troops_df = super_troops_df[super_troops_df['Name'] != 'String']
        super_troops_df = pd.merge(super_troops_df,troops_df, how='inner',left_on='Replacement', right_on='Name').drop(columns=['Name_y']).rename(columns={'Name_x': 'SuperTroopName'})
        super_troops_df['SuperTroopName'] = super_troops_df['SuperTroopName'].str.replace('Super','Super ')
        super_troops_df['SuperTroopName'] = super_troops_df['SuperTroopName'].str.replace('Wall','Wall ')

        
        unique_super_troops= super_troops_df['SuperTroopName'].unique()
        
        super_troops_available = pd.DataFrame(columns=['SuperTroopName'])

        for super_troop in unique_super_troops:

            super_troop_df = super_troops_df[super_troops_df['SuperTroopName'] == super_troop]
            minimum_level = np.float64(super_troop_df['MinOriginalLevel'].unique()[0])
            original_troop_name=super_troop_df[super_troop_df['SuperTroopName']==super_troop]['Original'].unique()[0]
            player_original_troop_df = player_info_dataframe[player_info_dataframe['TroopName'] == original_troop_name]

            if player_original_troop_df.empty:
                continue

            else:

                current_level = np.float64(player_info_dataframe[player_info_dataframe['TroopName'] == original_troop_name]['level'].unique()[0])

                if minimum_level>current_level:
                    continue

                else:
                    super_troops_available = pd.concat([super_troops_available, super_troop_df])
                    continue
        try:
            super_troops_available = super_troops_available.drop(columns=['Original', 'MinOriginalLevel','Replacement'])
            return super_troops_available
        except:
            return super_troops_available

    def get_production_building_for_troops(self,player_info_dataframe):
        troops_df = self.get_traduction()

        result = pd.merge(troops_df, player_info_dataframe, how='inner', left_on='TroopName', right_on='name')
        return result.drop(columns=['Dark Elixir Barrack','Barrack','TroopName'])

    def add_player_power_attack(self,troops_df):
      
        troops_df['PowerAttack'] = 0
        for i,row in troops_df.iterrows():
            if troops_df.at[i, 'MaxLevel'] == -1:
                troops_df.at[i, 'PowerAttack'] = np.NaN
                continue
            else:
                troops_df.at[i, 'PowerAttack'] = troops_df.at[i, 'level']/troops_df.at[i, 'MaxLevel']
        return troops_df



    def get_max_levels_for_townhall(self,tag=None, DEBUG=False):
        clash_data = ClashData()

        player_info_dataframe = clash_data.get_player_info(tag=tag).drop_duplicates()
        player_info_dataframe = self.get_max_barrack_level(player_info_dataframe)

        max_lab__per_townhall_dataframe = self.get_lab_levels()
        spells_max_levels_per_lab = self.get_spells_max_level_for_laboratory()
        troops_max_levels_per_lab = self.get_troops_max_level_for_laboratory()
        
        player_info_dataframe_with_lab = pd.merge(max_lab__per_townhall_dataframe,player_info_dataframe, how='inner',left_on='TownHallLevel', right_on='townHallLevel').drop(columns=['maxLevel','village'])
        
        only_troops_df = self.get_production_building_for_troops(player_info_dataframe_with_lab)
        
        troops_with_barrack=self.get_troops_for_max_barrack(player_info_dataframe_with_lab['BarrackLevel'].unique()[0],player_info_dataframe_with_lab['DarkBarrackLevel'].unique()[0])
        
        only_troops_df = pd.merge(player_info_dataframe_with_lab,troops_with_barrack, how='right',left_on='name', right_on='TroopName')\
                .drop(columns=['BarrackLevel_y','townHallLevel','Name'])\
                    .rename(columns={'LaboratoryLevel_x': 'ActualLab', 'BarrackLevel_x': 'BarrackLevel','LaboratoryLevel_y': 'LaboratoryLevel','ProductionBuilding_x':'ProductionBuilding'})

       
        player_info_dataframe.sort_values('name', inplace=True,ignore_index=True)

        super_troops_availables = self.get_super_troops_if_possible(only_troops_df)

        only_troops_df = self.get_max_troop_level_for_lab_player(troops_max_levels_per_lab, only_troops_df, super_troops_availables)
        only_troops_df = self.get_locked_troops(only_troops_df)

        only_troops_df = self.get_max_spell_level_for_lab_player(spells_max_levels_per_lab, only_troops_df, player_info_dataframe_with_lab)

        
        only_troops_df=self.get_max_heroes_for_townhall_player(only_troops_df,player_info_dataframe).drop(columns=['Dark Elixir Barrack','Barrack','DarkBarrackLevel']).drop_duplicates(ignore_index=True)

        only_troops_df=self.add_player_power_attack(only_troops_df)
        return only_troops_df



    def get_players_power_attack(self, player_compos=None, limit=None, DEBUG=False):
        cd = ClashData()
        player_tags = cd.get_player_tags(limit)
        player_levels = pd.DataFrame(columns=['PowerAttack', 'Username'])
        player_power_attack_dataframe= pd.DataFrame(columns=['PowerAttack', 'Username'])

        for player in player_tags:
            troops_df=self.get_max_levels_for_townhall(tag=player[1])
            player_power_attack = troops_df['PowerAttack'].mean()
            
            player_power_attack_dataframe= {'PowerAttack': [player_power_attack], 'Username': [player[0]]}
            player_power_attack_dataframe = pd.DataFrame.from_dict(player_power_attack_dataframe)

            player_levels = pd.concat([player_levels,player_power_attack_dataframe])
        

        print(player_levels)
        clan_power_attack = player_levels['PowerAttack'].mean()

        return clan_power_attack

if __name__ == '__main__':
    cd = ClanPowerAttack()
    print(cd.get_players_power_attack())


 