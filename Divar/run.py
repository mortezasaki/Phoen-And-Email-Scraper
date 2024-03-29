from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import re
import os
import requests
import json
from time import sleep

chromedriver_path = '.{0}chromedriver'.format(os.sep)

browser = webdriver.Chrome(executable_path=chromedriver_path) # Chrome driver
browser.get('https://divar.ir/my-divar/my-posts')

WebDriverWait(browser,60).until(EC.presence_of_element_located((By.CLASS_NAME, 'login-message__login-btn')))

btn = browser.find_element_by_class_name('login-message__login-btn')
btn.click()
input("Login to Divar, then press enter...")

cookies_list = browser.get_cookies()
cookies_dict = {}
for cookie in cookies_list:
    cookies_dict[cookie['name']] = cookie['value']

token = {'token':cookies_dict['token']}
# f = open('token.txt','w')
# f.write(cookies_dict['token'])
# f.close()

input("For Get links from this page press enter then scroll page...")

if os.path.exists('contacts.txt'):
    os.remove('contacts.txt')

links = []

try:
    while True:
        html_page = browser.page_source
        soup = BeautifulSoup(html_page,'html.parser')
        for link in soup.findAll('a', attrs={'href': re.compile("^/v/")}):
            _id = link.get('href').split('/')[-1]
            if _id not in links:
                url = 'https://api.divar.ir/v5/posts/{0}/contact'.format(_id)
                req = requests.get(url,cookies=token)
                if req.status_code == 200:
                    response =json.loads(req.text)
                    phone = response['widgets']['contact']['phone']
                    if re.match('^(09)\d{9}$',phone):
                        with open('phones.txt','a') as f:
                            print(phone)
                            f.write("%s\n" %(phone))
                    else:
                        print(phone)
                links.append(_id)
            # sleep(1)
        browser.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
        # sleep(60*30)
except Exception as e:
    print(str(e))
    browser.close()