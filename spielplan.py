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
driver.get("https://www.sfl.ch/spielplan/")
driver.implicitly_wait(2)


#scroll down & press 'Mehr anzeigen'
scroll_origin = ScrollOrigin.from_viewport(0,0)
for i in range(1,3):
    for i in range(1,15):
        ActionChains(driver)\
            .scroll_from_origin(scroll_origin, 0, 500)\
            .perform()
        time.sleep(1)

    try:
        mouse = ActionChains(driver)
        show_more = driver.find_element(By.LINK_TEXT, 'Mehr anzeigen')
        mouse.move_to_element(show_more).click().perform()
        time.sleep(1)
    except:
        print("1")

#make the soap
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')

#get all href
all_urls = [a['href']
            for a in soup('a')
            if a.has_attr('href')]

#print(str(all_urls))

#filter for relevant ones
includes_start = r"^https://www.sfl.ch/spieldetail/detail/"

relevant_urls = [url 
                 for url in all_urls
                 if re.match(includes_start, url)]

#print(str(relevant_urls))
#print(str(relevant_urls[0]))
#print(len(relevant_urls))

#take away the duplicates
relevant_urls = list(set(relevant_urls))
print(len(relevant_urls))

time.sleep(5)

#open csv file
try:
    d = open("spielplan.csv","w")
except:
    print("Dateizugriff nicht erfolgreich")
    sys.exit(0)

# get the actual referees from the page
for i in range(len(relevant_urls)):
    driver.get(relevant_urls[i])
    page_source2 = driver.page_source
    soup2 = BeautifulSoup(page_source2, 'html.parser')
    try:
        ref_tag = soup2.find('strong', string="SCHIEDSRICHTER")
        #print(ref_tag)
        ref1 = ref_tag.next_sibling.next_sibling
        ref2 = ref1.next_sibling.next_sibling
        ref3 = ref2.next_sibling.next_sibling
        ref4 = ref3.next_sibling.next_sibling
        datum = soup2.find('div', class_="c-matchdetail-hero__date u-text-semibold u-text-center").next.next.next
        datum = (''.join(datum.splitlines())).lstrip()
        runde = soup2.find('div', class_="c-matchdetail-hero__round u-text-center u-text-semibold").next
        home = soup2.find('p', class_="u-visible-md-up").next
        away = home.find_next('p', class_="u-visible-md-up").next
        

        d.write(runde + "," + datum + "," + home + "," + away + "," +  ref1 + "," + ref2 + "," + ref3 + "," + ref4 + "\n")
    except:
        pass

d.close

driver.quit()

