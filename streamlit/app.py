import streamlit as st
import pandas as pd
import numpy as np
from league_stats import ger_table, ger_final_results, first_final_round
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
        ('Tabela','Resumo Campeonato','Teste'))

    if add_selectbox2 == 'Tabela':
        tabela()
    elif add_selectbox2 == 'Resumo Campeonato':
        st.title('Estatísticas do campeonato')
        st.plotly_chart(ger_final_results(df))
        st.plotly_chart(first_final_round(df))




if __name__ == '__main__':
    main()