from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

def get_links():
    driver = webdriver.Chrome(executable_path='C:/Users/pedro/selenium/chromedriver.exe')
    driver.get('https://www.foxsports.com./soccer/schedule?competition=4&season=2019&round=1&week=0&group=0&sequence=1')
    myElem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="wisfoxbox"]/section[3]/div[1]/div/div[1]/div[2]/a')))
    html=driver.page_source
    soup=BeautifulSoup(html, 'lxml')
    urls=soup.find_all('td', {'class':'wisbb_gameInfo'})
    links=['https://www.foxsports.com.'+item.find('a')['href'] for item in urls if item.find('span', {'class':'wisbb_status'}).text == 'FINAL']
    driver.quit()
    return links