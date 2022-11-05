from flask import Blueprint, Response, request
import db
import clash_data as cd



clan = Blueprint('clan', __name__)


@clan.route('/clan')
def get_clan_players():
    members = cd.ClashData().get_clan_members()
    print(members)
    return members

@clan.route('/clan/update')
def update_clan():
    with db.get_connection() as conn:
        cursor = conn.cursor()
        query = """
        UPDATE clan
        INNER JOIN (select AVG(totalpowerattack) total, AVG(actualpowerattack) actual, clan FROM player GROUP BY clan) p
        ON p.clan = clan.id
        SET totalpowerattack = total,
        actualpowerattack = actual"""
