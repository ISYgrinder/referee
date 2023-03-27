#Ideas:
#1) go the the pages and get
#    date, game, refs
#2) store all in csv file
#3) get past data 
#4) store past data as well
#5) check data - empty lines
#6) run statistics and plots :)

#https://docs.python.org/3/tutorial/venv.html
#In powershell als admin:
#get-ExecutionPolicy
#Set-ExecutionPolicy Unrestricted -Force
##Dann Befehle von unten ausführen. 
#Powershell nochmals öffen als admin und wieder schleissen
#get-ExecutionPolicy
#Set-ExecutionPolicy Restricted -Force
#get-ExecutionPolicy

#To activate the .venv:
#C:\Users\Daniel\Documents\GitHub\referee\.venv\Scripts\Activate.ps1
#*gleiches, einfach mit "deactivate"
#To install packages:
#python -m pip install "XxX"
#To see all packages: 
#python -m pip list 


from bs4 import BeautifulSoup
import sys
import time
import requests
import re
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.mouse_button import MouseButton
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver import ActionChains





driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
driver.maximize_window()
driver.implicitly_wait(5)
driver.get("https://www.sfl.ch/spieldetail/detail/servette-fc-bsc-young-boys-861/")
driver.implicitly_wait(2)


page_source2 = driver.page_source
soup2 = BeautifulSoup(page_source2, 'html.parser')
print(soup2)


datum = soup2.find('div', class_="c-matchdetail-hero__date u-text-semibold u-text-center").next.next.next
datum = (''.join(datum.splitlines())).lstrip()
print(datum)
runde = soup2.find('div', class_="c-matchdetail-hero__round u-text-center u-text-semibold").next
print(runde)
home = soup2.find('p', class_="u-visible-md-up").next
print(home)
away = home.find_next('p', class_="u-visible-md-up").next
print(away)

#<p class="u-visible-md-up">Servette FC</p>


ref_tag = soup2.find('strong', string="SCHIEDSRICHTER")
print(ref_tag)
ref1 = ref_tag.next_sibling.next_sibling
print(ref1)
#ref2 = ref1.next_sibling.next_sibling





driver.quit()

