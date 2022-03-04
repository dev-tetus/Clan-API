

def get_credentials():
    f = open("credentials.txt", "r")
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
        'buildings_csv': content[8].split(' ')[1].strip()
    }
    return credentials