import pandas as pd
import numpy as np
import classes.credentials as cred
import functools as ft
class GameData():
    def __init__(self):
        self.game_troops = self.get_game_troops()
        self.game_heroes = self.get_game_heroes()
        self.game_spells = self.get_game_spells()
        self.game_buildings = self.get_game_buildings()
        self.game_pets = self.get_game_pets()
        

    def get_game_troops(self):
        traduction = pd.read_csv(cred.get_credentials()['texts_csv'],sep=';', encoding="ISO-8859-1", usecols=["TID", "EN"])
        troops = pd.read_csv(cred.get_credentials()['troops_csv'],skiprows=[i for i in range(1,2)],sep=';', encoding="ISO-8859-1", usecols=['Name', 'TID', 'ProductionBuilding','TroopLevel','LaboratoryLevel','BarrackLevel','ProductionBuilding','DisableProduction','IsSecondaryTroop','VillageType','DisableDonate','EnabledBySuperLicence'])
        troops = troops[(troops["VillageType"] == 0) & (troops["DisableProduction"] == False) & (troops["DisableDonate"] != True) & (troops["IsSecondaryTroop"] == False) & (troops["EnabledBySuperLicence"] != True)]
        troops = pd.DataFrame.merge(traduction,troops, on="TID")\
            .drop(columns=["TID","Name","DisableProduction","IsSecondaryTroop","VillageType","DisableDonate","EnabledBySuperLicence"])\
            .rename(columns={"EN":"TroopName","BarrackLevel" :"BarrackLevelRequired","LaboratoryLevel":"LaboratoryLevelRequired"})
        return troops

    def get_game_heroes(self):
        traduction = pd.read_csv(cred.get_credentials()['texts_csv'],sep=';', encoding="ISO-8859-1", usecols=["TID", "EN"])
        heroes = pd.read_csv(cred.get_credentials()['heroes_csv'],skiprows=[i for i in range(1,2)],sep=';', encoding="ISO-8859-1",usecols=["Name","Level","TID","VillageType","RequiredTownHallLevel"])
        heroes = heroes[heroes["VillageType"] == 0]
        heroes = pd.DataFrame.merge(traduction, heroes, on="TID")\
            .drop(columns=["TID","VillageType"])\
            .rename(columns={"EN":"TroopName","Level":"TroopLevel"})

        heroes = heroes.assign(ProductionBuilding = "Hero")
        return heroes

    def get_game_spells(self):
        traduction = pd.read_csv(cred.get_credentials()['texts_csv'],sep=';', encoding="ISO-8859-1", usecols=["TID", "EN"])
        spells = pd.read_csv(cred.get_credentials()['spells_csv'],skiprows=[i for i in range(1,2)],sep=';', encoding="ISO-8859-1", usecols=['Name','Level', 'DisableProduction','TID', 'ProductionBuilding',"SpellForgeLevel",'LaboratoryLevel',"ProductionBuilding","VillageType"])
        spells = spells[(spells["VillageType"] == 0) & (spells["DisableProduction"] == False)]
        spells = pd.DataFrame.merge(traduction, spells, on="TID")\
            .drop(columns=["TID","Name","VillageType","DisableProduction"])\
            .rename(columns={"EN":"TroopName","Level":"TroopLevel","SpellForgeLevel":"SpellForgeLevelRequired","LaboratoryLevel":"LaboratoryLevelRequired"})
        return spells
    
    def get_game_buildings(self):
        # traduction = pd.read_csv(cred.get_credentials()['texts_csv'],sep=';', encoding="ISO-8859-1", engine='python',usecols=["TID", "EN"])
        buildings = pd.read_csv(cred.get_credentials()['buildings_csv'],skiprows=[i for i in range(1,2)],sep=';', encoding="ISO-8859-1", usecols=['Name','BuildingLevel','BuildingClass','TownHallLevel','TID',"VillageType"])
        buildings = buildings[(buildings["BuildingClass"] == "Army") & (buildings["VillageType"] == 0)]
        # buildings = pd.DataFrame.merge(traduction, buildings, on="TID")\
        #     .drop(columns=["TID","Name","VillageType"])\
        #     .rename(columns={"EN":"Name","BarrackLevel" :"BarrackLevelRequired"})
        return buildings
    
    def get_game_pets(self):
        traduction = pd.read_csv(cred.get_credentials()['texts_csv'],sep=';', encoding="ISO-8859-1", usecols=["TID", "EN"])
        pets = pd.read_csv(cred.get_credentials()['pets_csv'],skiprows=[i for i in range(1,2)],sep=';', encoding="ISO-8859-1", usecols=['Name','TroopLevel', 'Deprecated','DisableProduction','TID', 'ProductionBuilding','BarrackLevel',"VillageType"])
        pets = pets[pets["Deprecated"] != True]
        pets = pd.DataFrame.merge(traduction, pets, on="TID")\
            .drop(columns=["TID","Name","VillageType","DisableProduction","Deprecated"])\
            .rename(columns={"EN":"TroopName","BarrackLevel" :"BarrackLevelRequired"})
        return pets
if __name__ == "__main__":
    g = GameData()
    print(g.game_buildings[(g.game_buildings["Name"]=="Barrack")&(g.game_buildings["TownHallLevel"] <= 15)].max()["BuildingLevel"])
    
