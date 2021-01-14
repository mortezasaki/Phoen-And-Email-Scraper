import re
import requests

url = input('Please enter url: ')

req = requests.get(url)

phone_regex = r"(\+\d{1})?[\s.-]?\(?\d{3}\)?[\s.-]?\d{3}[\s.]?\d{4}"

if req.status_code == 200:
    source_page = req.text
    mails = re.findall(r'[\w\.-]+@[\w\.-]+', source_page)

    with open('mails.txt','a') as mails_list:
        mails_list.write('\n'.join(mails)+'\n')
        print(mails)
        

    print('mails save on mails.txt')

    with open('phones.txt','a') as phones_list:
        matches = re.finditer(phone_regex, source_page)
        for matchNum, match in enumerate(matches, start=1):
            if match.group().startswith('09') or match.group().startswith('9'):
                phones_list.write(match.group()+'\n')


    print('phones save on mails.txt')

