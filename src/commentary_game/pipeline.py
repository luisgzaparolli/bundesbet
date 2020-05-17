from data_preparation import get_links
from data_gathering import make_comments
import pandas as pd

def update():
    df_read=pd.read_csv('../../data/comments.csv')
    links_worked=sorted(get_links())
    links_save=sorted(list(set(df_read['url'])))
    if links_save == links_worked:
        return
    else:
        urls = list(set(links_worked) - set(links_save))
        df=make_comments(df_read, urls)
        df.to_csv('../../data/comments.csv', index=False)
