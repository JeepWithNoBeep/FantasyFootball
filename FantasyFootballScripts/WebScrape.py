import polars as pl
import numpy as np
import smtplib
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import sys
import re
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless') # ensure GUI is off
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options = chrome_options)

# HEADERS = {} 

index = sys.argv[1]
driver.implicitly_wait(20)
URL2 = 'https://fantasy.espn.com/football/leaders?statSplit=singleScoringPeriod&scoringPeriodId=' + str(index)
driver.get(URL2)
driver.implicitly_wait(20)

def Table1(stored_,elements_):
  for j in elements_:
    stored_.append((re.findall(r'([A-Z].*)\n(?:(O|IR|Q|D|SSPD)\n)?([A-Za-z]{2,3})\n([A-Za-z]{2})\n(@?\*?[A-Za-z]{2,3}\*?|-{2})\n([A-Z]\s[0-9]{1,2}\-[0-9]{1,2}|-{2})?\n?([0-9]{1,2}\.[0-9]{1}|-{2})',
                       j.text))[0])
  return stored_

def Table2(stored_,elements_):
  for j in elements_:
    stored_.append((re.findall(r'([0-9]{1,2}/[0-9]{1,2}|-{2}/-{2})\n(-?[0-9]{1,3}|-{2})\n([0-9]{1,2}|-{2})\n([0-9]|-{2})\n([0-9]{1,2}|-{2})\n(-?[0-9]{1,3}|-{2})\n([0-9]{1,2}|-{2})\n([0-9]{1,2}|-{2})\n(-?[0-9]{1,3}|-{2})\n([0-9]{1,2}|-{2})\n([0-9]{1,2}|-{2})\n([0-9]{1,2}|-{2})\n([0-9]{1,2}|-{2})\n([0-9]|-{2})',
                    j.text))[0])
  return stored_

def Table3(stored_, elements_):
  for j in elements_:
    stored_.append(j.text)
  return stored_

tableBodyPath = '//*[@id="fitt-analytics"]/div/div[5]/div[2]/div[3]/div/div/div/div/div/div/table[1]/tbody'
tableBodyPath2 = '//*[@id="fitt-analytics"]/div/div[5]/div[2]/div[3]/div/div/div/div/div/div/div/div[2]/table/tbody'
tableBodyPath3 = '//*[@id="fitt-analytics"]/div/div[5]/div[2]/div[3]/div/div/div/div/div/div/table[2]/tbody'

driver.implicitly_wait(20)
TableBody = driver.find_elements(By.XPATH, tableBodyPath + '//descendant::tr')
time.sleep(1)
driver.implicitly_wait(20)
driver.implicitly_wait(20)
TableBody2 = driver.find_elements(By.XPATH, tableBodyPath2 + '//descendant::tr')
time.sleep(1)
driver.implicitly_wait(20)
TableBody3 = driver.find_elements(By.XPATH, tableBodyPath3 + '//descendant::tr')
time.sleep(1)
driver.implicitly_wait(20)

print("Getting Tables")
stored = Table1([], TableBody)
stored2 = Table2([], TableBody2)
stored3 = Table3([], TableBody3)

# LOOPS TO THE 20TH TABLE (at index 21)
for i in range(2,22):
  print("Getting Table ", i)
  driver.implicitly_wait(30)
  driver.find_element(By.XPATH, '//*[@id="fitt-analytics"]/div/div[5]/div[2]/div[3]/div/div/div/div/nav/button[2]').click()
  driver.implicitly_wait(30)
  time.sleep(1)
  if i != 21:
    stored  = Table1(stored,TableBody)
    stored2 =  Table2(stored2,TableBody2)
    stored3 = Table3(stored3,TableBody3)

stored  = Table1(stored,TableBody[0:5])
stored2 =  Table2(stored2,TableBody2[0:5])
stored3 = Table3(stored3,TableBody3[0:5])


stored = np.asarray(stored)
stored2 = np.asarray(stored2)
stored3 = np.asarray(stored3)

df = pl.DataFrame(
    {'PLAYER NAME': stored[:,0],
     'PLAYER TEAM': stored[:,2],
     'PLAYER POSITION': stored[:,3],
     'OPP': stored[:,4],
     'STATUS': stored[:,5],
     'PROJ': stored[:,6],
     'PASSING C/A': stored2[:,0],
     'PASSING YDS': stored2[:,1],
     'PASSING TD': stored2[:,2],
     'PASSING INT': stored2[:,3],
     'RUSHING CAR': stored2[:,4],
     'RUSHING YDS': stored2[:,5],
     'RUSHING TD': stored2[:,6],
     'RECEIVING REC': stored2[:,7],
     'RECEIVING YDS': stored2[:,8],
     'RECEIVING TD': stored2[:,9],
     'RECEIVING TAR': stored2[:,10],
     'MISC 2PC': stored2[:,11],
     'MISC FUML': stored2[:,12],
     'MISC TD': stored2[:,13],
     'TOTAL': stored3,
     } )


path = 'FF_Week' + str(index) + '.csv'
df.write_csv(file = path , has_header = True)

driver.quit()
