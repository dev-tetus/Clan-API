
from flask import Blueprint, Response, request
import message_diffusion as md
import db
import clash_data as cd

clan_league = Blueprint('clan_league', __name__)

def get_clan_war_data(clan_data, opponent_data, war_id,cursor):
    for member in clan_data['members']:
        print(member)
        member_war_attack_query = "SELECT * FROM leagueattack WHERE war_id = %s and player_id = (SELECT id from player where tag = %s)"
        if cursor.execute(member_war_attack_query, (war_id, member['tag'])) == 0: #No attacks registered in db
            if 'attacks' in member:
                attacks = member['attacks'][0]
                add_member_attack_query = "INSERT into leagueattack(war_id, player_id, player, op_tag, stars, destructionpercentage, duration, op_townhall_level, has_attacked) VALUES(%s,(SELECT id from player where tag =%s) ,(SELECT username from player where tag =%s), %s, %s, %s, %s, %s,1)"
                result = cursor.execute(add_member_attack_query,(war_id, member['tag'],
                                                        member['tag'],
                                                        attacks['defenderTag'],
                                                        attacks['stars'],
                                                        attacks['destructionPercentage'],
                                                        attacks['duration'],
                                                        next(opponent['townhallLevel'] for opponent in opponent_data['members'] if opponent["tag"] == attacks['defenderTag'])
                                                        ))
                print(f'{result} player attack added')
            else:
                print(member)
                add_member_without_attack_query = "INSERT INTO leagueattack(war_id, player_id, player) VALUES(%s,(SELECT id from player where tag =%s) ,(SELECT username FROM player WHERE tag = %s))"
                result = cursor.execute(add_member_without_attack_query,(war_id, member['tag'],member['tag']))
                print(f'{result} empty player attack added')
        else:
            member_war_attack = cursor.fetchone()
            print(member_war_attack)
            if member_war_attack[9] == 0:
                if 'attacks' in member:
                    attacks = member['attacks'][0]
                    update_member_attack_query = "UPDATE leagueattack SET op_tag=%s, stars=%s, destructionpercentage=%s, duration=%s, op_townhall_level=%s, has_attacked=1 WHERE player_id =(SELECT id from player where tag =%s) and war_id = %s"
                    result = cursor.execute(update_member_attack_query,(attacks['defenderTag'],
                                                        attacks['stars'],
                                                        attacks['destructionPercentage'],
                                                        attacks['duration'],
                                                        next(opponent['townhallLevel'] for opponent in opponent_data['members'] if opponent["tag"] == attacks['defenderTag']),
                                                        member['tag'],
                                                        war_id
                                                        ))
                    print(f'{result} player attack updated')

@clan_league.route('/clan/league/add')
def add_clan_league():
    pass
@clan_league.route('/clan/league/wars/update')
def update_league_wars():
    data = cd.ClashData()
    league_war_tags = data.get_league_war_tags()
    clan_league_wars = data.get_clan_league_war_tags(league_war_tags)
    
    #Check if current league season is in db
    league_season_query = "SELECT * FROM league_season where season = %s"

    with db.get_connection() as conn:
        league_season = data.get_league_season()
        cursor = conn.cursor()
        league_season_db = cursor.execute(league_season_query, league_season)
        current_season_league = cursor.fetchone()

        if league_season is not None:                                           # if clan is in league
            if league_season_db == 0:                                           # if league season is not already saved
                add_league_season_query = "INSERT INTO league_season(season) VALUES(%s)"
                cursor.execute(add_league_season_query, league_season)
                conn.commit()

            for i,tag in enumerate(clan_league_wars):
                if cursor.execute("SELECT * FROM leaguewar WHERE war_tag = %s", tag) == 0:
                    add_war_query = "INSERT INTO leaguewar(season, day, war_tag) VALUES(%s,%s,%s)"
                    cursor.execute(add_war_query, (current_season_league[0],i+1,tag ))
                    conn.commit()

                war = data.get_league_war_info(tag)
                cursor.execute("SELECT id FROM leaguewar WHERE war_tag = %s", tag)
                war_id = cursor.fetchone()[0]

                if war['clan']['name'] == 'SN3T':
                    clan_data = war['clan']
                    opponent_data = war['opponent']
                    get_clan_war_data(clan_data, opponent_data,war_id,cursor)
                else:
                    print(war['opponent'],war['clan'])
                    clan_data = war['opponent']
                    opponent_data = war['clan']
                    get_clan_war_data(clan_data=clan_data, opponent_data=opponent_data, war_id=war_id,cursor=cursor)
            conn.commit()    
            cursor.close()
            return Response("Success")

                

        else:
            return  Response("Clan not in league this season")