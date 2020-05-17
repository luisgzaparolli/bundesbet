from data_gathering import get_stats_game
from data_preparation import get_games
import pandas as pd
from selenium import webdriver

def update():
    df_read=pd.read_csv('../../data/game_stas.csv')
    links_save=sorted((df_read['url']))
    links_worked=sorted(get_games())
    if links_save == links_worked:
        return
    else:
        urls = list(set(links_worked) - set(links_save))
        driver = webdriver.Chrome(executable_path='C:/Users/pedro/selenium/chromedriver.exe')
        for url in urls:
            df = get_stats_game(driver, url, df)
        driver.quit()
        df.to_csv('../../data/game_stas.csv', index=False)



if __name__ == '__main__':
    update()
