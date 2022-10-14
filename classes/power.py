import pandas as pd
import numpy as np
import os, sys


from player import Player
from game_data import GameData
from clash_data import ClashData



pd.options.display.float_format = "{:,.2f}".format



class Power(GameData):
    def __init__(self,DEBUG=False,players=None,clan_tag=None):
        super().__init__()
        self.players_power_attack = pd.DataFrame(columns=['Player', 'ActualPowerAttack',"TotalPowerAttack"])
        self.clan_dataframe = self.set_players_power_attack(ClashData().get_player_tags(clan_tag=clan_tag))
        self.total_clan_power_attack = None
        self.actual_clan_power_attack = None
        self.set_clan_power_attack()

    def set_players_power_attack(self, players):
        
        for player in players:
            member = Player(tag=player[1])
            # print(member.dataframe[member.dataframe["Total"] == np.inf])

            self.players_power_attack = pd.concat([self.players_power_attack,\
            pd.DataFrame.from_dict({
                "Player":[player[0]],
                "ActualPowerAttack": [np.float64(member.actualPowerAttack)],
                "TotalPowerAttack": [np.float64(member.totalPowerAttack)],
                })])
    
    def set_clan_power_attack(self):
        print(self.players_power_attack["TotalPowerAttack"])
        self.total_clan_power_attack = np.format_float_positional(self.players_power_attack["TotalPowerAttack"].unique()[0] * 100, precision=2)
        self.actual_clan_power_attack = np.format_float_positional(self.players_power_attack["ActualPowerAttack"].unique()[0]* 100, precision=2)


if __name__ == '__main__':
   
    p = Power(clan_tag="#2QYPUV9RG")
    # print(p.dataframe)
    print(p.players_power_attack)
    print(str("Puissance d'attaque totale ")+p.total_clan_power_attack+'%')
    print(str("Puissance d'attaque actuelle ")+p.actual_clan_power_attack+'%')