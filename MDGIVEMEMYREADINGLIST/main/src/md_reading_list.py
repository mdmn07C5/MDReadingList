import requests
import os
import time
import getpass
from pandas import DataFrame

def login(payload):
    try:
        auth = requests.post('https://api.mangadex.org/auth/login', json=payload).json()
        return auth['token']['session']
    except:
        print('Incorrect username/password pair')
        return None

# return user's following list
def get_follow_list(token):
    header = {'Authorization': f'Bearer {token}'}
    limit = 100
    initial = requests.get(
        'https://api.mangadex.org/user/follows/manga',
        headers=header,
        params={'limit': limit}
    ).json()

    follows = [{'id': x['data']['id'],
                'title': x['data']['attributes']['title']['en'],
                'mu_id': x['data']['attributes']['links'].get('mu')
                if x['data']['attributes']['links']
                else None}
                for x in initial['results']]
    total = initial['total']

    for offset in range(limit, total, limit):
        body = {'limit': limit, 'offset': offset}
        request = requests.get(
            'https://api.mangadex.org/user/follows/manga',
            headers = header,
            params = body
        ).json()
        for r in request['results']:
            follows.append({'id': r['data']['id'],
                            'title': r['data']['attributes']['title']['en'],
                            'mu_id': r['data']['attributes']['links'].get('mu')
                            if r['data']['attributes']['links']
                            else None})
    
    return DataFrame(follows)

# get the last read ids for each manga in the user's follow list
def get_last_read(token, follows, batch_size=150):
    header = {'Authorization': f'Bearer {token}'}
    res = []
    for i in range(0, len(follows), batch_size):
        request = requests.get(
            'https://api.mangadex.org/manga/read',
            headers=header,
            params={'ids[]': follows[i:i+batch_size], 'grouped': 'true'}
        ).json()
        for r in request['data']:
            res.append({'id':r, 'last_read':request['data'][r][-1]})
    return res

# returns human readable (i.e. chapter number and chapter title) details for the last read chapters
def get_chapter_detail(chapter_list):
    for item in chapter_list:
        try:
            r = requests.get(f'https://api.mangadex.org/chapter/{item["last_read"]}').json()
            item['last_read'] = r['data']['attributes']['chapter']
            item['chapter_title'] = r['data']['attributes']['title']
        except KeyError:
            if r['errors'][0]['status'] == 404:
                item['last_read'] = 'chapter not found (series probably nuked from database)'
            else:
                item['last_read'] = 'forbidden (whatever the fuck that means)'
        except:
            print('something else went wrong, log it')
    return DataFrame(chapter_list)


if __name__=='__main__':
    username = input('Username: ')
    password = getpass.getpass('Password: ')
    os.system('cls' if os.name=='nt' else 'clear')
    payload = {'username': username, 'password': password}

    while ((session_token := login(payload)) == None):
        username = input('Username: ')
        password = getpass.getpass('Password: ')
        os.system('cls' if os.name=='nt' else 'clear')
        payload = {'username': username, 'password': password}
    start = time.time()
    follows = get_follow_list(session_token)
    read_chapters = get_last_read(session_token, follows['id'].tolist())
    last_read_chapter = get_chapter_detail(read_chapters)
    print(f'Elapsed time: {time.time() - start}')

    reading_list = follows.join(last_read_chapter.set_index('id'), on='id')
    reading_list.to_csv(os.path.dirname(os.path.realpath(__file__))+'/reading_list.csv')