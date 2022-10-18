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
        self.set_players_power_attack(ClashData().get_player_tags(clan_tag=clan_tag))
        self.total_clan_power_attack = None
        self.actual_clan_power_attack = None
        self.set_clan_power_attack()

    def set_players_power_attack(self, players):
        print(players.__len__())
        for player in players:
            member = Player(tag=player[1])
            self.players_power_attack = pd.concat([self.players_power_attack,\
            pd.DataFrame.from_dict({
                "Player":[player[0]],
                "ActualPowerAttack": [member.actualPowerAttack],
                "TotalPowerAttack": [member.totalPowerAttack],
                })])
    
    def set_clan_power_attack(self):
        self.total_clan_power_attack = np.format_float_positional(self.players_power_attack["TotalPowerAttack"].mean() * 100, precision=2)
        self.actual_clan_power_attack = np.format_float_positional(self.players_power_attack["ActualPowerAttack"].mean()* 100, precision=2)


if __name__ == '__main__':
    p1 = Power(clan_tag="#2PC82L0PR")
    p2 = Power()
    # print(p.dataframe)
    print(p1.players_power_attack)
    print(str("Puissance d'attaque totale ")+p1.total_clan_power_attack+'%')
    print(str("Puissance d'attaque actuelle ")+p1.actual_clan_power_attack+'%')


    print(p2.players_power_attack)
    print(str("Puissance d'attaque totale ")+p2.total_clan_power_attack+'%')
    print(str("Puissance d'attaque actuelle ")+p2.actual_clan_power_attack+'%')