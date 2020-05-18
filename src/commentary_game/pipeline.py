from src.commentary_game.data_preparation import get_links
from src.commentary_game.data_gathering import make_comments
import pandas as pd
from src.params import Params


def update():
    """
    Function to find the data saved, and compare with actually data to set if want's to update or not
    """
    # get a data storage, and find links on site
    df = pd.read_csv(Params.comments_data)
    links_worked = sorted(get_links())
    links_save = sorted(list(set(df['url'])))
    # compare if links stored equals links on site
    if links_save == links_worked:
        return
    else:
        # get links are in site and not in storage data, works on this links and update data
        urls = list(set(links_worked) - set(links_save))
        df = make_comments(df, urls)
        df.to_csv(Params.comments_data, index=False)
