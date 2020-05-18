from src.stats_games.data_gathering import get_stats_game
from src.stats_games.data_preparation import get_games
import pandas as pd
from selenium import webdriver
from src.params import Params


def update():
    """
    Function to find the data saved, and compare with actually data to set if want's to update or not
    """
    # get a data storage, and find links on site
    df = pd.read_csv(Params.game_stats_data)
    links_save = sorted((df['url']))
    links_worked = sorted(get_games())
    # compare if links stored equals links on site
    if links_save == links_worked:
        return
    else:
        # get links are in site and not in storage data, works on this links and update data
        urls = list(set(links_worked) - set(links_save))
        driver = webdriver.Chrome(executable_path=Params.path_crome)
        print(urls)
        for url in urls:
            print(url)
            df = get_stats_game(driver, url, df)
        driver.quit()
        df.to_csv(Params.game_stats_data, index=False)
