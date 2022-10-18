import pandas as pd
import numpy as np
import credentials as cred
import functools as ft


from clash_data import ClashData
from game_data import GameData



class Player(GameData):
    def __init__(self,tag=None,DEBUG=False):
        super().__init__()
        self.player_troops = ClashData().get_player_info(tag=tag,DEBUG=DEBUG)
        self.townHallLevel = np.int8(self.player_troops['townHallLevel'].unique()[0])
        self.laboratoryLevel = None
        self.barrackLevel = None
        self.darkBarrackLevel = None
        self.spellForgesLevels = None
        self.miniSpellFactory = None
        self.siegeWorkshop = None
        self.petHouseLevel = None
        self.totalPowerAttack = None
        self.actualPowerAttack = None
        self.locked_troops = self.get_locked_troops()
        self.locked_heroes = self.get_locked_heroes()
        self.locked_spells = self.get_locked_spells()
        self.pets = self.get_pets()
        self.locked_pets = self.get_locked_pets()
        self.dataframe = self.get_dataframe()
        self.set_max_barracks_and_lab_levels()
        self.assign_locked_units()
        self.assign_power_attack()
        self.set_mean_power_attack()
    
    def get_merged_dataframes(self,df1,df2,column, how,filter):
        data = df1.merge(df2, on=column, how=how, indicator=True, suffixes=[".x", ".y"])
        data = data[data["_merge"] == filter].drop('_merge',axis=1)
        data.columns = data.columns.str.split(".", expand=True)
        data.columns = data.columns.droplevel(1) if data.columns.nlevels > 1 else data.columns
        data = data.groupby(column).max().rename(columns={"TroopLevel":"MaxLevel"})
        data = data.loc[:,~data.columns.duplicated()]
        return data.reset_index()

    def get_locked_abstract(self, df1, df2, column, how,filter):
        data = self.get_merged_dataframes(df1, df2, column, how,filter)
        data = data.assign(ActualLevel = 0, townHallLevel=self.player_troops["townHallLevel"].unique()[0],username=self.player_troops["username"].unique()[0])
        return data

    def get_pets(self):
        data = self.get_merged_dataframes(self.game_pets,self.player_troops,  "TroopName", "inner", "both")
        
        return data
    def get_locked_pets(self):
        return self.get_locked_abstract(self.game_pets, self.player_troops,"TroopName", "left", "left_only")

    def get_locked_troops(self):
        return self.get_locked_abstract(self.game_troops, self.player_troops,"TroopName", "left", "left_only")

    def get_locked_heroes(self):
        heroes = self.get_locked_abstract(self.game_heroes, self.player_troops,"TroopName", "left", "left_only")
        heroes.assign(ProductionBuilding = "Hero")
        return heroes

    def get_locked_spells(self):
        return self.get_locked_abstract(self.game_spells, self.player_troops,"TroopName", "left", "left_only")
    
    def get_dataframe(self):
        troops = self.game_troops.groupby('TroopName').max()
        spells = self.game_spells.groupby('TroopName').max()
        heroes = self.game_heroes.groupby('TroopName').max()

        df = self.player_troops.merge(troops.rename(columns={"TroopLevel":"MaxLevel"}), how='left', on='TroopName', suffixes=[".player", ".game"])
        df.columns = df.columns.str.split(".", expand=True)
        df.columns = df.columns.droplevel(1)
        df = df.loc[:,~df.columns.duplicated()]
        

        df = df.merge(spells.rename(columns={"TroopLevel":"MaxLevel"}), how='left', on='TroopName', suffixes=[".player", ".game"])
        df['LaboratoryLevelRequired.player'].fillna(df['LaboratoryLevelRequired.game'], inplace=True)
        df['ProductionBuilding.player'].fillna(df['ProductionBuilding.game'], inplace=True)
        df.columns = df.columns.str.split(".", expand=True)
        df.columns = df.columns.droplevel(1)
        df = df.loc[:,~df.columns.duplicated()]


        df = df.merge(heroes.rename(columns={"TroopLevel":"MaxLevel"}), how='left', on='TroopName', suffixes=[".player", ".game"])
        df['ProductionBuilding.player'].fillna(df['ProductionBuilding.game'], inplace=True)
        df.columns = df.columns.str.split(".", expand=True)
        df.columns = df.columns.droplevel(1)
        df = df.loc[:,~df.columns.duplicated()]


        df = pd.concat([df,self.locked_troops,self.locked_spells,self.locked_heroes,self.pets,self.locked_pets]).sort_values(by="ProductionBuilding")
        df[['BarrackLevelRequired', 'LaboratoryLevelRequired',"SpellForgeLevelRequired"]] = df[['BarrackLevelRequired', 'LaboratoryLevelRequired',"SpellForgeLevelRequired"]].fillna(value=0)

        df = self.remove_super_troops(df)

        return df

    def set_max_barracks_and_lab_levels(self):
        self.laboratoryLevel=self.game_buildings[(self.game_buildings["Name"]=="Laboratory") &(self.game_buildings["TownHallLevel"] <= self.townHallLevel)].max()["BuildingLevel"]#.reset_index().at[0,"BuildingLevel"]
        if(np.isnan(self.laboratoryLevel)):
            self.laboratoryLevel = 0
        self.barrackLevel = self.game_buildings[(self.game_buildings["Name"]=="Barrack") & (self.game_buildings["TownHallLevel"] <= self.townHallLevel)].max()["BuildingLevel"]#.reset_index().at[0,"BuildingLevel"]
        self.spellForgesLevels =self.game_buildings[(self.game_buildings["Name"]=="Spell Forge") | (self.game_buildings["Name"]=="Mini Spell Factory") & (self.game_buildings["TownHallLevel"] <= self.townHallLevel)]
  
        min_TownHallLevelRequired_DarkBarrack = self.game_buildings[self.game_buildings["Name"]=="Dark Elixir Barrack"]["TownHallLevel"].min()
        min_TownHallLevelRequired_SpellForge = self.spellForgesLevels[self.spellForgesLevels["Name"]=="Spell Forge"]["TownHallLevel"].min()
        min_TownHallLevelRequired_MiniSpellFactory = self.spellForgesLevels[self.spellForgesLevels["Name"]=="Mini Spell Factory"]["TownHallLevel"].min()
        min_TownHallLevelRequired_SiegeWorkshop = self.game_buildings[self.game_buildings["Name"]=="SiegeWorkshop"]["TownHallLevel"].min()
        min_TownHallLevelRequired_Pet_House = self.game_buildings[self.game_buildings["Name"]=="Pet Shop"]["TownHallLevel"].min()
        if (self.townHallLevel < min_TownHallLevelRequired_DarkBarrack):
            self.darkBarrackLevel = 0
        else: 
            th_arr = self.game_buildings[(self.game_buildings["Name"]=="Dark Elixir Barrack")]
            df_sort = th_arr.iloc[(th_arr['TownHallLevel']-self.townHallLevel).abs().argsort()[:2]]
            self.darkBarrackLevel = df_sort[df_sort["BuildingLevel"] == df_sort["BuildingLevel"].max()]["BuildingLevel"].reset_index().at[0,"BuildingLevel"]

       

        self.dataframe['ActualBarrackLevel'] = self.dataframe.apply(lambda row: self.barrackLevel if row["ProductionBuilding"] == "Barrack" else self.darkBarrackLevel, axis=1)
        self.dataframe['ActualLaboratoryLevel'] = self.dataframe.apply(lambda row: self.laboratoryLevel , axis=1)
        self.dataframe['ActualMaxSpellForgeLevel'] = self.dataframe.apply(lambda row:self.assign_actual_max_spell_forge_level(row,min_TownHallLevelRequired_SpellForge,min_TownHallLevelRequired_MiniSpellFactory),axis=1)
        self.dataframe["ActualMaxSiegeWorkshopLevel"] = self.dataframe.apply(lambda row: self.assign_actual_max_siege_workshop_level(row,min_TownHallLevelRequired_SiegeWorkshop), axis=1)
        self.dataframe["ActualMaxPetHouseLevel"] = self.dataframe.apply(lambda row: self.assign_actual_max_pet_shop_level(row,min_TownHallLevelRequired_Pet_House), axis=1)
        self.dataframe['ActualMaxUnitLevel'] = self.dataframe.apply(lambda row:self.assign_actual_max_unit_level(row),axis=1)
        # print(self.dataframe[self.dataframe["ProductionBuilding"]== "SiegeWorkshop"])
        

    def assign_actual_max_spell_forge_level(self,row,min_TownHallLevelRequired_SpellForge,min_TownHallLevelRequired_MiniSpellFactory):
        if row["ProductionBuilding"] == "Spell Forge" or row["ProductionBuilding"] == "Mini Spell Factory":
            if (self.townHallLevel < min_TownHallLevelRequired_SpellForge if row["ProductionBuilding"] == "Spell Forge" else self.townHallLevel < min_TownHallLevelRequired_MiniSpellFactory):
                self.spellForgesLevels = 0
            else: 
                th_arr = self.game_buildings[(self.game_buildings["Name"]==row["ProductionBuilding"])]
                df_sort = th_arr.iloc[(th_arr['TownHallLevel']-self.townHallLevel).abs().argsort()[:2]]
                self.spellForgesLevels = df_sort[df_sort["TownHallLevel"] == df_sort["TownHallLevel"].max()]["BuildingLevel"].max()
            return self.spellForgesLevels
           
    def assign_actual_max_siege_workshop_level(self,row,min_TownHallLevelRequired_SiegeWorkshop):
        if row["ProductionBuilding"] == "SiegeWorkshop":
            if (self.townHallLevel < min_TownHallLevelRequired_SiegeWorkshop):
                self.siegeWorkshop = 0
            else: 
                th_arr = self.game_buildings[self.game_buildings["Name"] == row["ProductionBuilding"]]
                df_sort = th_arr.iloc[(th_arr['TownHallLevel']-self.townHallLevel).abs().argsort()[:3]]
                self.siegeWorkshop = df_sort[df_sort["TownHallLevel"] == df_sort["TownHallLevel"].max()]["BuildingLevel"].max()
            return self.siegeWorkshop

    def assign_actual_max_pet_shop_level(self, row,min_townHallLevelRequired_petShop):
        if row["ProductionBuilding"] == "Pet House":
            if (self.townHallLevel < min_townHallLevelRequired_petShop):
                self.petHouseLevel = 0
            else: 
                th_arr = self.game_buildings[self.game_buildings["Name"] == "Pet Shop"]
                # df_sort = th_arr.iloc[(th_arr['TownHallLevel']-self.townHallLevel).argsort()]
                df_sort = th_arr[th_arr['TownHallLevel'] <=self.townHallLevel]
                # [["TroopName","TownHallLevel"]].toxarray()
                # .findLastIndex((element) =>{element <=0})
               
                self.petHouseLevel = df_sort[df_sort["TownHallLevel"] == df_sort["TownHallLevel"].max()]["BuildingLevel"].max()
            return self.petHouseLevel
    
    def assign_actual_max_unit_level(self,row):
        if row["ProductionBuilding"] == "Barrack" or row["ProductionBuilding"] == "Dark Elixir Barrack": 
            if np.int8(row["ActualBarrackLevel"]) < row["BarrackLevelRequired"]:
                return 0
            unit = self.game_troops[self.game_troops["TroopName"] == row["TroopName"]]
            max_level = unit[unit["LaboratoryLevelRequired"] <= np.int8(row["ActualLaboratoryLevel"])]["TroopLevel"].max()
            return max_level
        elif row["ProductionBuilding"] == "Spell Forge" or row["ProductionBuilding"] == "Mini Spell Factory":
            if np.int8(row["ActualMaxSpellForgeLevel"] < row["SpellForgeLevelRequired"]):
                return 0
            unit = self.game_spells[self.game_spells["TroopName"] == row["TroopName"]]
            max_level = unit[unit["LaboratoryLevelRequired"] <= np.int8(row["ActualLaboratoryLevel"])]["TroopLevel"].max()
            return max_level
        elif row["ProductionBuilding"] == "SiegeWorkshop":
            if np.int8(row["ActualMaxSiegeWorkshopLevel"] < row["BarrackLevelRequired"]) and row["ActualLevel"] == 0:
                return 0

            unit = self.game_troops[self.game_troops["TroopName"] == row["TroopName"]]
            max_level = unit[unit["LaboratoryLevelRequired"] <= np.int8(row["ActualLaboratoryLevel"])]["TroopLevel"].max()
            return max_level
        elif row["ProductionBuilding"] == "Hero":
            hero = self.game_heroes[(self.game_heroes["TroopLevel"]==1 )& (self.game_heroes["TroopName"]==row["TroopName"])]
            if self.townHallLevel < hero["RequiredTownHallLevel"].min():
                return 0
            else:
                maxLevel = self.game_heroes[(self.game_heroes["RequiredTownHallLevel"]==self.townHallLevel)]["TroopLevel"].max()
                return maxLevel
        elif row["ProductionBuilding"] == "Pet House":
            unit = self.game_pets[self.game_pets["TroopName"] == row["TroopName"]].max()

            if np.int8(row["ActualMaxPetHouseLevel"]) < row["BarrackLevelRequired"]:
                return 0
            else:
                return unit["TroopLevel"]

    
    def assign_lock_type(self,row):
        
        if row["ProductionBuilding"] == "Barrack" or row["ProductionBuilding"] == "Dark Elixir Barrack":
            if row["ActualLevel"] == 0:
                if row["ActualBarrackLevel"] < row["BarrackLevelRequired"]:
                    return 1
                elif row["ActualBarrackLevel"] == row["BarrackLevelRequired"]:
                    return 2
            else:
                return 0
        elif row["ProductionBuilding"] == "Spell Forge" or row["ProductionBuilding"] == "Mini Spell Factory":
            if row["ActualLevel"] == 0:
                if row["ActualMaxSpellForgeLevel"] < row["SpellForgeLevelRequired"]:
                    return 1
                elif row["ActualMaxSpellForgeLevel"] == row["SpellForgeLevelRequired"]:
                    return 2
            else:
                return 0
        elif row["ProductionBuilding"] == "SiegeWorkshop":
            if row["ActualLevel"] == 0:
                if row["ActualMaxSiegeWorkshopLevel"] < row["BarrackLevelRequired"]:
                    return 1
                elif row["ActualMaxSiegeWorkshopLevel"] == row["BarrackLevelRequired"]:
                    return 2
            else:
                return 0
        elif row["ProductionBuilding"] == "Pet House":
            if row["ActualLevel"] == 0:
                if row["ActualMaxPetHouseLevel"] < row["BarrackLevelRequired"]:
                    return 1
                elif row["ActualMaxPetHouseLevel"] >= row["BarrackLevelRequired"]:
                    return 2
                else:
                    return 
            else:
                return 0
        else:
            if row["ActualLevel"] == 0:
                if row["ActualMaxUnitLevel"] == 0:
                    return 1
                else:
                    return 2
            else:
                return 0
                
    def assign_locked_units(self):
        ###
        #   LockType:
        #               - 0 : Troop unlocked
        #               - 1 : Troop Locked (Low level)
        #               - 2 : Troop Locked (Not upgraded) 
        # ###
        self.dataframe['LockType'] = self.dataframe.apply(lambda row: self.assign_lock_type(row), axis=1)

    def assign_power_attack(self):
        def actual_attack(row):
            match row["LockType"]:
                case 0:
                    return np.float16(row["ActualLevel"])/np.float16(row["ActualMaxUnitLevel"]) 
                case 1:
                    return np.NaN
                case 2:
                    return np.float16(row["ActualLevel"])/np.float16(row["ActualMaxUnitLevel"])
        def total_attack(row):
            return np.float16(row["ActualLevel"])/np.float16(row["MaxLevel"]) 
            
        self.dataframe["Total"] = self.dataframe.apply(lambda row: total_attack(row),axis=1)
        self.dataframe["Actual"] = self.dataframe.apply(lambda row: actual_attack(row),axis=1)


    def remove_super_troops(self, df1):
        traduction = pd.read_csv(cred.get_credentials()['texts_csv'],sep=';', encoding="ISO-8859-1", usecols=["TID", "EN"])
        troops = pd.read_csv(cred.get_credentials()['troops_csv'],skiprows=[i for i in range(1,2)],sep=';', encoding="ISO-8859-1", usecols=['Name', 'TID','DisableProduction','DisableDonate','VillageType','EnabledBySuperLicence'])
        super_troops = troops[(troops["VillageType"] == 0) & (troops["DisableProduction"] == False) & (troops["DisableDonate"] != True) & (troops["EnabledBySuperLicence"] == True)]
        super_troops = pd.DataFrame.merge(traduction, super_troops, on="TID")\
            .drop(columns=["TID","VillageType","Name","DisableDonate","DisableProduction","EnabledBySuperLicence"])\
            .rename(columns={"EN":"TroopName","Level":"TroopLevel"})

        df = df1.merge(super_troops.rename(columns={"Name":"TroopName"}), on='TroopName',how='outer', indicator=True,suffixes=[".player", ".game"])\
            .query('_merge =="left_only"').drop('_merge',axis=1)        
        return df

    def set_dataframe(self):
        self.dataframe = self.remove_super_troops()

    def set_mean_power_attack(self):

        self.totalPowerAttack=self.dataframe["Total"].mean()
        self.actualPowerAttack=self.dataframe[self.dataframe["LockType"] != 1]["Actual"].mean()
        
     
    

if __name__ == '__main__':
    player = Player(DEBUG=False,tag="%2329L0VJ2JY")
    # print(player.dataframe)
    # player.get_max_barracks_and_lab_levels()