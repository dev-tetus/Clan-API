import requests
import utils

credentials = utils.get_credentials()
coc_routes= ('')
headers = {
    'content-type': 'application/json',
    'Authorization': 'Bearer {api}'.format(api=credentials["api_key"])
    }

def get_clan_members_count():
    response= requests.get('https://api.clashofclans.com/v1/clans/%232LV9J8VLQ/members', headers=headers)
    return response.json()["items"].__len__()

#Debug
if __name__ == '__main__':
    get_clan_members_count()