import requests
import hashlib
import Config
from processPreloginFactor import processPreloginFactor
import json, sys, os
from datetime import datetime

if __name__ == "__main__":
    verbose_level = 0
    if len(sys.argv) > 1:
        if sys.argv[1] == "-v":
            verbose_level = 1
        elif sys.argv[1] == "-vv":
            verbose_level = 2
    else:
        verbose_level = 0
    print("Verbose level: " + str(verbose_level))
    headers = {
        'authority': 'www.deltamath.com',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
        'dnt': '1',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'accept': '*/*',
        'origin': 'https://www.deltamath.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.deltamath.com/',
        'accept-language': 'fr-FR,fr;q=0.9',
    }
    # Create a session
    session = requests.Session()
    if verbose_level >= 1: print("[*] Sending prelogin request...")
    response = session.post('https://www.deltamath.com/api/prelogin', headers=headers, json={'email': Config.email})
    if verbose_level == 2: print("[*] Received prelogin response...")
    login_data = {
        'email': Config.email,
        'password': hashlib.md5(("deltamath"+Config.password).encode('utf-8')).hexdigest(),
        'prelogin_factor': processPreloginFactor(response.json()['number']),
        'prelogin_token': response.json()['token'],
    }
    if verbose_level >= 1: print("[*] Sending login request...")
    response2 = session.post('https://www.deltamath.com/api/login', headers=headers, json=login_data)
    if verbose_level == 2: print("[*] Received login response...")
    if verbose_level >= 1: print('[*] Sending "get_student_details" request...')
    raw_data = session.post('https://www.deltamath.com/api/get_student_details', headers=headers, json={'student_id': None, 'termOrClass': 'current', 'version': 401})
    if verbose_level == 2: print('[*] Received "get_student_details" response...')
    if verbose_level >= 1: print('[*] Dumping student data to "student_details.json"...')
    with open('student_details.json', 'w') as outfile:
        json.dump(raw_data.json(), outfile, indent=4)