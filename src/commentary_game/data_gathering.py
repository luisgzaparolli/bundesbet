from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd

def get_comments(driver,df,id,url):
    driver.get(url)
    myElem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="fullCommentary"]')))
    element = driver.find_element_by_id('fullCommentary')
    driver.execute_script("arguments[0].click();", element)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    home = soup.find_all('span', {'class': 'wisbb_bsName'})[0].text
    away = soup.find_all('span', {'class': 'wisbb_bsName'})[1].text
    commentarys = soup.find('table', {'class': 'wisbb_bsCPbpSmallTable'}).find_all('tr')
    img_home = commentarys[0].find('img')['src']
    infos = {}
    id_game = id
    urls, ids, time, team, comm= [], [], [], [], []
    for comments in commentarys:
        urls.append(url)
        ids.append(id_game)
        time_aux = comments.find('td', {'class': 'wisbb_bsSoccerPbpTimeCol'}).text.replace("'", '').split('+')
        time.append(sum([int(item) for item in time_aux]))
        team.append(home if comments.find('img')['src'] == img_home else away)
        comm.append(comments.find('span', {'class': 'wisbb_bsSoccerPbpDesc'}).text)
    infos['url']=urls
    infos['id_game'] = ids
    infos['time'] = time
    infos['team'] = team
    infos['comm'] = comm
    df_aux=pd.DataFrame(infos)
    df=pd.concat([df,df_aux])
    return df

def make_comments(df, links):
    driver = webdriver.Chrome(executable_path='C:/Users/pedro/selenium/chromedriver.exe')
    id = df['id'].max()
    for url in links:
        try:
            df = get_comments(driver, df, id, url)
        except Exception as e:
            print(e)
            print(f'Link with error: {url}')
            driver.quit()
            driver = webdriver.Chrome(executable_path='C:/Users/pedro/selenium/chromedriver.exe')
            pass
        id += 1
    print(id)
    driver.quit()
    return df