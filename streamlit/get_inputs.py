from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


def get_text_links(soup):
    games_live = soup.find('div', {'class': 'leagues--live contest--leagues'}).find_all('div', {'title': 'Click for game detail!'})
    games_start, games_not_start, links = [], [], []
    if len(games_live) > 0:
        for game in games_live:
            if game.find('span')['class'] == ['icon', 'icon--preview']:
                games_not_start.append(game)
            else:
                games_start.append(game)
                link='https://www.scoreboard.com/game/' + game['id'].split('_')[2] + '/#game-summary'
                links.append(link)
        result_txt = ''
        if len(games_not_start) > 0:
            result_txt += 'Games today not started: \n'
            for game in games_not_start:
                home = game.find('div', {'class': 'event__participant event__participant--home'}).text
                away = game.find('div', {'class': 'event__participant event__participant--away'}).text
                time = game.find('div', {'class': 'event__time event__time--usFormat'}).text
                result_txt += f'{home} x {away}  ({time}) \n'
            result_txt += '-=-'*20+'\n'
        if len(games_start) > 0:
            result_txt += 'Games today has benn started: \n'
            for game in games_start:
                home = game.find('div', {'class': 'event__participant event__participant--home'}).text
                away = game.find('div', {'class': 'event__participant event__participant--away'}).text
                result_txt += f'{home} x {away}  \n'
            result_txt += '-=-' * 20 + '\n'
    else:
        result_txt = 'No games today!'
    return result_txt, links


def find_games_today():
    driver = webdriver.Chrome(executable_path='C:/Users/pedro/selenium/chromedriver.exe')
    driver.get('https://www.scoreboard.com/soccer/germany/bundesliga/')
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="box-table-type-16"]/div[2]')))
    time.sleep(2)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    text, links = get_text_links(soup)
    driver.quit()
    return text

print(find_games_today())