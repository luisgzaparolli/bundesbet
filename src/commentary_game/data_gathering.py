from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
from src.params import Params


def get_comments(driver: object, df: pd.DataFrame, id_game: str, url: str) -> pd.DataFrame:
    """
    This function make a get in web drive selenium, catch commentaries from game on foxsports site,
    and concat the results to df input and return df with the input
    :param driver: Web driver from selenium
    :param df: Data Frame with the commentaries of previous game
    :param id_game: Last unique id to identify games
    :param url: the url from foxsports site with the commentaries
    :return: return a Data Frame after concat the input df and info's of url
    """
    # make a get in url of game and save the page source to work
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="fullCommentary"]')))
    element = driver.find_element_by_id('fullCommentary')
    driver.execute_script("arguments[0].click();", element)
    html = driver.page_source
    # read the html with BeautifulSoup and get the name of teams
    soup = BeautifulSoup(html, 'lxml')
    home = soup.find_all('span', {'class': 'wisbb_bsName'})[0].text
    away = soup.find_all('span', {'class': 'wisbb_bsName'})[1].text
    home_goals_final = int(soup.find_all('td', {'class': 'wisbb_bsTotal'})[0].text.strip())
    away_goals_final = int(soup.find_all('td', {'class': 'wisbb_bsTotal'})[1].text.strip())
    # save all commentaries in one list to work, and set the home image to select what team is the commentary
    commentaries = soup.find('table', {'class': 'wisbb_bsCPbpSmallTable'}).find_all('tr')
    img_home = commentaries[0].find('img')['src']
    # make empty lists, and work in each commentary to save commentary, team, and time of commentary
    urls, ids, time, team, comm = [], [], [], [], []
    for comments in commentaries:
        urls.append(url)
        ids.append(id_game)
        time_aux = comments.find('td', {'class': 'wisbb_bsSoccerPbpTimeCol'}).text.replace("'", '').split('+')
        time.append(sum([int(item) for item in time_aux]))
        team.append(home if comments.find('img')['src'] == img_home else away)
        comm.append(comments.find('span', {'class': 'wisbb_bsSoccerPbpDesc'}).text)
    infos = {'url': urls, 'id_game': ids, 'time': time, 'team': team,
             'home_goals_final': home_goals_final, 'away_goals_final' : away_goals_final, 'comm': comm}
    # save infos in Data Frame and concat with previous Data Frame
    df_aux = pd.DataFrame(infos)
    df = pd.concat([df, df_aux])
    return df


def make_comments(df: pd.DataFrame, links: list) -> pd.DataFrame:
    """
    With all links of foxsports site, we work link by link, and save append results in data frame
    :param df: data frame with previous commentaries
    :param links: links of games to work
    :return: data frame after concatenate all links
    """
    # make a driver to create a section were we going to work, and get the last game id to set news id's
    driver = webdriver.Chrome(executable_path=Params.path_crome)
    try:
        id_game = df['id_game'].max()+1
    except:
        id_game = 0
    # work in each url in links list, to append results in Data Frame, randle error to pass link
    for url in links:
        try:
            df = get_comments(driver, df, id_game, url)
        except Exception as e:
            print(e)
            print(f'Link with error: {url}')
            driver.quit()
            driver = webdriver.Chrome(executable_path=Params.path_crome)
            pass
        id_game += 1
    print(id_game)
    # quit driver and return a Data Frame
    driver.quit()
    return df
