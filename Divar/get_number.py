import requests
import json
from time import sleep
import re

f = open('token.txt', 'r')
token = f.readline()
f.close()

token = {'token':token}
print(token)
f = open('contacts.txt','r')
contacts = f.readlines()
f.close()

with open('phones.txt','a') as f:
    for contact in contacts:
        url = 'https://api.divar.ir/v5/posts/{0}/contact'.format(contact.replace('\n',''))
        req = requests.get(url,cookies=token)
        if req.status_code == 200:
            response =json.loads(req.text)
            phone = response['widgets']['contact']['phone']
            if re.match('^(09)\d{9}$',phone):
                f.write('{0}\n'.format(phone))
                print(phone)
        sleep(5)