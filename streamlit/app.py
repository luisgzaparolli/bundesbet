import streamlit as st
import pandas as pd
import numpy as np
from league_stats import ger_table
from get_inputs import find_games_today

df=pd.read_csv('C:/Users/pedro/Projetos/bundesbet/src/data/game_stats.csv')

def capa():
    st.title('Bundesliga')
    st.header(find_games_today())

def tabela():
    list_select = np.arange(df['round'].max(),0,-1)
    rnd=st.selectbox('Rodada', (list_select))
    st.dataframe(ger_table(rnd,df),height=1000)

def main():

    add_selectbox = st.sidebar.selectbox(
        'Menu',
        ('Home','Tabela'))

    if add_selectbox == 'Home':
        capa()

    elif add_selectbox == 'Tabela':
        tabela()



if __name__ == '__main__':
    main()