from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def get_games():
    driver = webdriver.Chrome(executable_path='C:/Users/pedro/selenium/chromedriver.exe')
    driver.get('https://www.scoreboard.com/uk/football/germany/bundesliga/results/')
    while True:
        try:
            WebDriverWait(driver, 120).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="live-table"]/div[1]/div/div/a'))).click()
        except:
            break
    html=driver.page_source
    soup=BeautifulSoup(html, 'lxml')
    games=soup.find_all('div',{'class':'event__match event__match--static event__match--oneLine'})
    games=['https://www.scoreboard.com/uk/match/'+item['id'].split('_')[2]+'/#match-summary' for item in games]
    driver.quit()
    return games



