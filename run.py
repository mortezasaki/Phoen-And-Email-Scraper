from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import re
import requests
import json
from time import sleep


browser = webdriver.Chrome(executable_path='./chromedriver') # Chrome driver
browser.get('https://divar.ir/my-divar/my-posts')

WebDriverWait(browser,60).until(EC.presence_of_element_located((By.CLASS_NAME, 'login-message__login-btn')))

btn = browser.find_element_by_class_name('login-message__login-btn')
btn.click()
input("Login then press enter...")

cookies_list = browser.get_cookies()
cookies_dict = {}
for cookie in cookies_list:
    cookies_dict[cookie['name']] = cookie['value']

token = {'token':cookies_dict['token']}
print(token)

input("For Get All number from this page press enter")
html_page = browser.page_source
soup = BeautifulSoup(html_page,'html.parser')

links = []

for link in soup.findAll('a', attrs={'href': re.compile("^/v/")}):
    links.append(link.get('href'))
with open('phones.txt','a') as f:
    for link in links:
        url = 'https://api.divar.ir/v5/posts/{0}/contact'.format(link.split('/')[-1])
        req = requests.get(url,cookies=token)
        if req.status_code == 200:
            response =json.loads(req.text)
            phone = response['widgets']['contact']['phone']
            if re.match('^(09)\d{9}$',phone):
                f.write('{0}\n'.format(phone))
                print(phone)
        sleep(5)

browser.close()