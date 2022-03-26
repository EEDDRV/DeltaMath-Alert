import requests
import hashlib
import Config
from processPreloginFactor import processPreloginFactor
import json, sys, os, time
from email.message import EmailMessage
import smtplib
from datetime import datetime

def Get_Data(verbose_level=0):
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

def send_email(subject, body, to):
	msg = EmailMessage()
	msg.set_content(body)
	msg['subject'] = subject
	msg['to'] = to
	user = Config.Send_Email
	msg['from'] = user
	password = Config.Send_Email_Password
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(user, password)
	server.send_message(msg)
	server.quit()


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
    Original_Data = Get_Data(verbose_level)
    while True:
        Data = Get_Data(verbose_level)
        if Data != Original_Data:
            print("[*] Data has changed!")
            send_email("DeltaMath Alert", "Data has changed!", Config.Email_Send)
            Original_Data = Data

        time.sleep(10)