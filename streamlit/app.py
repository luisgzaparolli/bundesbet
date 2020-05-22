import streamlit as st
import pandas as pd
import numpy as np
from league_stats import ger_table, ger_final_results, first_final_round, last_games,stats_home_away,get_positions
import seaborn as sns
import matplotlib.pyplot as plt
#from get_inputs import find_games_today


df=pd.read_csv('C:/Users/pedro/Projetos/bundesbet/src/data/game_stats.csv')

def capa():
    pass

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

    add_selectbox2 = st.sidebar.selectbox(
        'Estatísticas',
        ('Resumo Campeonato','Resumo por time'))

    if add_selectbox2 == 'Resumo por time':
        team=st.selectbox('Select the team:', sorted(list(df['home_team'].unique())))
        rnd = df['round'].max()
        st.title('Posição na tabela')
        st.dataframe(ger_table(rnd,df).style.apply(lambda x: ["color: red" if v == team else "" for v in x], axis = 1),height=1000)
        st.title('Evolução no Campeonato')
        st.plotly_chart(get_positions(df,team))
        st.title('Últimos 5 jogos')
        st.dataframe(last_games(df,team).style.apply(lambda x: ["color: red" if v == team else "" for v in x], axis = 1) )
        st.title('Estatística Casa/Fora')
        st.dataframe(stats_home_away(df,team))
        
    elif add_selectbox2 == 'Resumo Campeonato':
        st.title('Estatísticas do campeonato')
        st.plotly_chart(ger_final_results(df))
        st.plotly_chart(first_final_round(df))
        tabela()
 
if __name__ == '__main__':
    main()