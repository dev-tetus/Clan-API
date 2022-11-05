import time
from flask import Blueprint, Response, request
import db
import clash_data as cd
import power as power
import player as player



clan_routes = Blueprint('clan_routes', __name__)



@clan_routes.route('/clan/player/add',methods=['POST'])
def add_clan_player():
    with db.get_connection() as conn:
        query = "INSERT INTO player(username, tag, joindate, townhall,totalpowerattack,actualpowerattack,clan,role) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        data = request.get_json(force=True)
        p = player.Player(tag=data['tag'])
        print(data)
        cursor = conn.cursor()
        result = cursor.execute(query, (data['username'], data['tag'].replace("%23","#"),time.strftime('%Y-%m-%d %H:%M:%S'),p.townHallLevel,p.totalPowerAttack,p.actualPowerAttack,1,p.role) )
        conn.commit()
        cursor.close()
        return Response(f"{result} players updated")

@clan_routes.route('/clan/player/<string:name>/vote', methods=['POST'])
def add_player_vote(name):
    query = "UPDATE player SET numvotes = numvotes + 1, has_voted = 1 WHERE username = %s and has_voted = 0"
    with db.get_connection() as conn:
        cursor = conn.cursor()
        result = cursor.execute(query,name)
        conn.commit()
        cursor.close()
        return Response(f"Vote to player with name = {name} added" if result > 0 else f"{name} already voted")
    
@clan_routes.route('/clan/player/votes/reset', methods=['POST'])
def clan_votes_reset():
    with db.get_connection() as conn:
        cursor = conn.cursor()
        query = "UPDATE player SET has_voted = 0"
        cursor.execute(query)
        conn.commit()
        cursor.close()
        return Response(f"Votes reset")
        
@clan_routes.route('/clan/members/update')
def update_clan_members():
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM player")
        rows= cursor.fetchall()
        player_list = []

        if len(rows) == 0:
            query = """
            INSERT INTO player(username,tag,townhall,totalpowerattack,actualpowerattack,clan,role)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
            """
            for p in cd.ClashData().get_clan_members():
                member=player.Player(tag=p['tag'])
                player_list.append((p['name'],p['tag'],member.townHallLevel,member.totalPowerAttack,member.actualPowerAttack,1,member.role))

            result = cursor.executemany(query,player_list)
            conn.commit()
            cursor.close()

            return Response(f"{result} players updated")
        else:
            query ="""
            UPDATE player
            SET totalpowerattack = %s, actualpowerattack = %s, townhall = %s, clan = %s, role = %s
            WHERE tag = %s
            """

            for p in cd.ClashData().get_clan_members():
                member=player.Player(tag=p['tag'])
                cursor.execute(query,(member.totalPowerAttack,member.actualPowerAttack, member.townHallLevel,1,member.role,p['tag']))

            conn.commit()
            cursor.close()
            return Response(f"Players updated...")