credentials = {}

def get_credentials():
    f = open("credentials.txt", "r")
    content = f.readlines()
    credentials = {
        'username': content[0].split(' ')[1].strip(),
        'password': content[1].split(' ')[1].strip(),
        'api_key': content[2].split(' ')[1].strip()
    }
    return credentials

#Debug
if __name__ == '__main__':
    get_credentials()