from crypt import methods
import time 
from flask import Flask, Response, request
import datetime
import os
import sys
sys.path.insert(1, os.getcwd()+str("/classes"))
import db
import clash_data as cd
import power as power
import player as player

from routes.clan.clan_members import clan_routes
from routes.clan.clan import clan
from routes.clan.clan_proc import clan_proc
from routes.clan.clan_league import clan_league
app = Flask(__name__)
app.register_blueprint(clan_routes)
app.register_blueprint(clan)
app.register_blueprint(clan_proc)
app.register_blueprint(clan_league)

db.get_connection()

@app.route('/')
def home():
    return "yes"


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

    



if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True,host='0.0.0.0', port=port)
