from crypt import methods
import time 
from flask import Flask, Response, request
import os
import sys
sys.path.insert(1, os.getcwd()+str("/classes"))
import db
import clash_data as cd
import power as power
import player as player
import message_diffusion as md


app = Flask(__name__)

db.get_connection()

@app.route('/')
def home():
    return "yes"

@app.route('/clan')
def get_clan_players():
    members = cd.ClashData().get_clan_members()
    print(members)
    return members

@app.route('/clan/update')
def update_clan():
    with db.get_connection() as conn:
        cursor = conn.cursor()
        query = """
        UPDATE clan
        INNER JOIN (select AVG(totalpowerattack) total, AVG(actualpowerattack) actual, clan FROM player GROUP BY clan) p
        ON p.clan = clan.id
        SET totalpowerattack = total,
        actualpowerattack = actual"""

@app.route('/clan/player/add',methods=['POST'])
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

@app.route('/clan/player/<string:name>/vote', methods=['POST'])
def add_player_vote(name):
    query = "UPDATE player SET numvotes = numvotes + 1, has_voted = 1 WHERE username = %s and has_voted = 0"
    with db.get_connection() as conn:
        cursor = conn.cursor()
        result = cursor.execute(query,name)
        conn.commit()
        cursor.close()
        return Response(f"Vote to player with name = {name} added" if result > 0 else f"{name} already voted")
    
@app.route('/clan/player/votes/reset', methods=['POST'])
def clan_votes_reset():
    with db.get_connection() as conn:
        cursor = conn.cursor()
        query = "UPDATE player SET has_voted = 0"
        cursor.execute(query)
        conn.commit()
        cursor.close()
        return Response(f"Votes reset")
        
@app.route('/clan/members/update')
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

@app.route('/players/update')
def update_players():
    with db.get_connection() as conn:
        cursor = conn.cursor()
        
        players_in_clan=[player['tag'] for player in cd.ClashData().get_clan_members()]

        query = """
        SELECT * FROM player 
        WHERE tag NOT IN {};
        """.format(tuple(players_in_clan))

        cursor.execute(query)
        rows= cursor.fetchall()

        for p in rows:
            db_player = player.Player(tag=p[2])
            if(p[8] == 1):
                #Check for clan if exists and get id to insert, else get clan and insert new clan then add id to player clan
                if db_player.clan != -1:
                    clan_query = "SELECT * FROM clan WHERE tag = %s"
                    result = cursor.execute(clan_query, db_player.clan)
                    if result == 0:
                        clan_insert_query = "INSERT INTO clan(tag,name) VALUES (%s,%s)"
                        clan = (db_player.clan,cd.ClashData().get_clan_name(tag=db_player.clan))
                        cursor.execute(clan_insert_query,clan)

                    update_player_query = """
                    UPDATE player
                    SET townhall = %s , totalpowerattack = %s, actualpowerattack = %s, clan = (SELECT id from clan WHERE tag= %s), role = %s
                    where tag = %s
                    """
                    result = cursor.execute(update_player_query, (db_player.townHallLevel, db_player.totalPowerAttack, db_player.actualPowerAttack, db_player.clan, db_player.role,p[2]))
                    conn.commit()
                else:
                    update_player_query = """
                    UPDATE player
                    SET townhall = %s , totalpowerattack = %s, actualpowerattack = %s, clan = %s, role = %s
                    WHERE tag = %s
                    """
                    result = cursor.execute(update_player_query, (db_player.townHallLevel, db_player.totalPowerAttack, db_player.actualPowerAttack, db_player.clan, db_player.role, p[2]))
                    conn.commit()
            else:
                
                if(db_player.clan == -1):
                    update_player_query = """
                        UPDATE player
                        SET townhall = %s , totalpowerattack = %s, actualpowerattack = %s, clan = %s, role = %s
                        WHERE tag = %s
                        """
                    result = cursor.execute(update_player_query, (db_player.townHallLevel, db_player.totalPowerAttack, db_player.actualPowerAttack, db_player.clan, db_player.role, p[2]))
                    conn.commit()
                else:  
                    update_player_query = """
                    UPDATE player
                    SET townhall = %s , totalpowerattack = %s, actualpowerattack = %s, clan =(SELECT id from clan WHERE tag like %s), role = %s
                    WHERE tag = %s
                    """
                    result = cursor.execute(update_player_query, (db_player.townHallLevel, db_player.totalPowerAttack, db_player.actualPowerAttack, db_player.clan, db_player.role, p[2]))
                    conn.commit()



        cursor.close()
            
        return Response("Done")

    
@app.route('/clan/diffusion/send')
def send_diffusion():
    try:
        md_controller = md.MessageDiffusion()
        md_controller.start_diffusion()
        return Response("Message sent to servers...")
    except KeyError as e:
        print(e)
        return e



if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True,host='0.0.0.0', port=port)
