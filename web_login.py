# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 13:35:46 2020

@author: sbergmann

Copyright@Hach Lange GmbH 
"""
import requests
LOGINURL = 'http://10.130.25.90/'
PROTECTEDPAGE = 'http://10.130.25.90/cgi-bin/SC1000?Mode=9&UserID=1&AUTO_REFRESH=1'
url = 'https://www.google.de/'

payload = {"password": "MAX1000"}
payload = {
    "q": "wetter",
    }
session_requests = requests.Session()
r = session_requests.get(LOGINURL) 
r.cookies
r = requests.post(LOGINURL,data=payload)
session_requests.post(
	LOGINURL, 
	data = payload, )

session_requests.get(PROTECTEDPAGE)
session_requests.auth = ('','MAX1000')


r = requests.get('https://api.github.com')

from requests.utils import dict_from_cookiejar
cookies = dict_from_cookiejar(r.cookies)

r.status_code
r.content
r.text
r.json()
r.headers
r.headers['Content-Type']
r.json()['data']

response = requests.get(
    'https://api.github.com/search/repositories',
    params={'q': 'requests+language:python'},
)

# Inspect some attributes of the `requests` repository
json_response = response.json()
repository = json_response['items'][0]
print(f'Repository name: {repository["name"]}')  # Python 3.6+
print(f'Repository description: {repository["description"]}')  # Python 3.6+

LOGINURL = 'http://10.130.25.90/cgi-bin/SC1000?Mode=0'
LOGINURL = 'http://10.130.25.90/cgi-bin/SC1000?Mode=9&UserID=1&AUTO_REFRESH=1'

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

chromedriver = 'C:\\chromedriver.exe'
browser = webdriver.Chrome(chromedriver)
browser.get(LOGINURL)

# username = selenium.find_element_by_id("username")
password = browser.find_element_by_name("password")
word = browser.find_element_by_name("BMenu")
password.send_keys("MAX1000")


# username.send_keys("YourUsername")
button = browser.find_elements_by_xpath('//input[@type="submit"]')[0]
button.click()
browser.find_element_by_link_text("submit").click()

import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'
    }

login_data = {
    'password': 'MAX1000',
    'submit': 'OK'
    }

with requests.Session() as s:
    url = 'http://10.130.22.122/cgi-bin/SC1000?Mode=0'
    r = s.get(url,headers=headers)
    print(r.content)
    soup = BeautifulSoup(r.content, 'html5lib')
    soup.find('input', attrs={'name':'password'})
    
    
    
LOGINURL = 'http://10.130.22.122/cgi-bin/SC1000'
PROTECTEDPAGE = 'http://10.130.22.122/cgi-bin/SC1000?Mode=9&UserID=1&AUTO_REFRESH=1'


login_data = {
    'Mode': '1',
    'SetLanguage': '1',
    'password': 'MAX1000',
    }
session_requests = requests.Session()
r = session_requests.get(LOGINURL) 
# r.cookies
r = session_requests.post(LOGINURL,data=login_data)
r = session_requests.get(PROTECTEDPAGE)
    