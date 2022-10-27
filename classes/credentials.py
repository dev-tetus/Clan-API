import sys

def get_credentials():

    if sys.platform == "Linux":
        f = open('credentials-linux.txt', 'r')
    else:
        f = open('credentials.txt', 'r')
    content = f.readlines()
    credentials = {
        'username': content[0].split(' ')[1].strip(),
        'password': content[1].split(' ')[1].strip(),
        'api_key': content[2].split(' ')[1].strip(),
        'base_url': content[3].split(' ')[1].strip(),
        'clan_tag': content[4].split(' ')[1].strip(),
        'spells_csv': content[5].split(' ')[1].strip(),
        'troops_csv': content[6].split(' ')[1].strip(),
        'heroes_csv': content[7].split(' ')[1].strip(),
        'buildings_csv': content[8].split(' ')[1].strip(),
        'texts_csv': content[9].split(' ')[1].strip(),
        'pets_csv': content[10].split(' ')[1].strip(),
        'mysql_ip' : content[11].split(' ')[1].strip(),
        'db_user' : content[12].split(' ')[1].strip(),
        'db_pass' : content[13].split(' ')[1].strip(),
    }
    return credentials
