from flask import Flask, Response
import os
import sys
sys.path.insert(1, os.getcwd()+str("/classes"))
import db
import clash_data as cd
import power as power
import player as player




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
            SET totalpowerattack = %s, actualpowerattack = %s
            WHERE tag = %s
            """
            for p in list(rows):
                member = player.Player(tag=p[2])
                cursor.execute(query,(member.totalPowerAttack,member.actualPowerAttack, p[2]))

            conn.commit()
            cursor.close()
            return Response(f"Players updated...")

            # print(list(rows))
        

        
    # members=p.Power().

      
        
    



if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True,host='0.0.0.0', port=port)
