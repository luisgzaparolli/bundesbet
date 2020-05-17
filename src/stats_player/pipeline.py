import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


def get_players_link():
    url = 'https://fmdataba.com/20/l/191/bundesliga/best-players/'
    hdr = {'User-Agent': 'Mozilla/5.0'}
    html = requests.get(url, headers=hdr).content
    soup = BeautifulSoup(html, 'lxml')
    teams = soup.find_all('table', {'class': 'table table-striped'})[1].find_all('td')
    url_teams = [item.find('a')['href'] for item in teams]
    url_list = []
    for team in url_teams:
        html = requests.get(team, headers=hdr).content
        soup = BeautifulSoup(html, 'lxml')
        players = soup.find('table', {'id': 'tablo61'}).find_all('td', {'style': 'font-size:12px;'})
        url_players = [item.find('a')['href'] for item in players]
        url_list.append(url_players)
    url_list = [item for x in url_list for item in x]
    return url_list

def get_data(url):
    hdr = {'User-Agent': 'Mozilla/5.0'}
    html = requests.get(url, headers=hdr).content
    soup=BeautifulSoup(html, 'lxml')
    name=soup.find('span', {'itemprop':'name'}).text
    posicao=pd.read_html(html)[3].loc[23,1]
    df=pd.DataFrame({'name':name, 'posicao':posicao}, index=[0])
    for i in range(7,10):
        df_aux=pd.read_html(html)[7].T
        df_aux.columns=df_aux.iloc[0,:]
        df_aux=df_aux.loc[1,:]
        df_aux=pd.DataFrame(df_aux).T
        df_aux=df_aux.reset_index(drop=True)
        df=pd.concat([df,df_aux], axis=1)
    print(url)
    return df,posicao

df_player=pd.DataFrame()
df_gk=pd.DataFrame()
urls = get_players_link()
print(len(urls))
for url in urls:
    attmp=0
    while attmp < 10:
        try:
            df_aux, posicao = get_data(url)
            break
        except:
            attmp+=1
            time.sleep(attmp*10)
    if posicao == 'GK':
        df_gk=pd.concat([df_gk,df_aux])
    else:
        df_player=pd.concat([df_player,df_aux])
df_player.to_csv('../../data/player_stats.csv', index=False)
df_gk.to_csv('../../data/gk_stats.csv', index=False)
