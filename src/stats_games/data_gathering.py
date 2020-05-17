from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

def get_stats_game(driver,url, df):
    driver.get(url)
    myElem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="summary-content"]/div[1]/div[3]/div[2]/span[1]')))
    html=driver.page_source
    soup=BeautifulSoup(html,'lxml')
    infos={}
    infos['url']=url
    infos['round']=int(soup.find('span', {'class':'description__country'}).text.split(' ')[-1])
    infos['home_team']=soup.find('div',{'class':'tname__text'}).text.strip()
    infos['away_team']=soup.find_all('div',{'class':'tname__text'})[1].text.strip()
    infos['goals_home_final']=int(soup.find('span',{'class':'scoreboard'}).text)
    infos['goals_away_final']=int(soup.find_all('span',{'class':'scoreboard'})[1].text)
    infos['final_result'] = 'Away' if infos['goals_home_final'] < infos['goals_away_final'] else 'Home' if infos['goals_home_final'] > infos['goals_away_final'] else 'Draw'
    infos['goals_home_1half']=int(soup.find('span',{'class':'p1_home'}).text)
    infos['goals_away_1half']=int(soup.find('span',{'class':'p1_away'}).text)
    infos['1half_result'] = 'Away' if infos['goals_home_1half'] < infos['goals_away_1half'] else 'Home' if infos['goals_home_1half'] > infos['goals_away_1half'] else 'Draw'
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="a-match-statistics"]'))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="statistics-1-statistic"]/span/a'))).click()
    time.sleep(2)
    html_code = driver.find_element_by_tag_name("body").text.split('\n')
    i=0
    x=html_code.index('Ball possession')
    stat=html_code[x+i*3].lower().replace(' ','_')
    while stat != 'dangerous_attacks':
        stat=html_code[x+i*3].lower().replace(' ','_')
        infos[stat+'home']=int(html_code[x+i*3-1].replace('%',''))
        infos[stat+'away']=int(html_code[x+i*3+1].replace('%',''))
        i+=1
    df_aux = pd.DataFrame(infos, index=[0])
    df=pd.concat([df,df_aux])
    return df


