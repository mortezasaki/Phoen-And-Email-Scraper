from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

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

print(cookies_dict)

browser.close()