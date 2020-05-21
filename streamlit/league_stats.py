import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.preprocessing import Normalizer
import plotly.express as px
import plotly.graph_objects as go


def get_games(team, rnd, df):
    """
    Function that takes the number of games a team played until the determined round
    :param team: Team we want to find games
    :param rnd: Limit round that we will seek
    :param df: Data Frame with games
    :return: A integer number with number of games
    """
    mask1 = ((df['home_team'] == team) | (df['away_team'] == team)) & (df['round'] <= rnd)
    return len(df.loc[mask1, 'round'])


def get_wins(team, rnd, df):
    """
    Function that takes the number of victories of a team until the determined round
    :param team: Team we want to find wins
    :param rnd: Limit round that we will seek
    :param df: Data Frame with games
    :return: A integer number with number of wins
    """
    mask1 = (df['home_team'] == team) & (df['final_result'] == 'Home') & (df['round'] <= rnd)
    mask2 = (df['away_team'] == team) & (df['final_result'] == 'Away') & (df['round'] <= rnd)
    return len(df.loc[mask1 | mask2, 'round'])


def get_draws(team, rnd, df):
    """
    Function that takes the number of draws of a team until the determined round
    :param team: Team we want to find draws
    :param rnd: Limit round that we will seek
    :param df: Data Frame with games
    :return: A integer number with number of draws
    """
    mask1 = ((df['home_team'] == team) | (df['away_team'] == team)) & (df['final_result'] == 'Draw') & (
            df['round'] <= rnd)
    return len(df.loc[mask1, 'round'])


def get_loses(team, rnd, df):
    """
    Function that takes the number of loses of a team until the determined round
    :param team: Team we want to find loses
    :param rnd: Limit round that we will seek
    :param df: Data Frame with games
    :return: A integer number with number of loses
    """
    mask1 = (df['home_team'] == team) & (df['final_result'] == 'Away') & (df['round'] <= rnd)
    mask2 = (df['away_team'] == team) & (df['final_result'] == 'Home') & (df['round'] <= rnd)
    return len(df.loc[mask1 | mask2, 'round'])


def gp(team, rnd, df):
    """
    Function that takes the number of goals scores by team until the determined round
    :param team: Team we want to find goals scores
    :param rnd: Limit round that we will seek
    :param df: Data Frame with games
    :return: A integer number with number of goals scores
    """
    goals = df.query(f'home_team == "{team}" & round <= {rnd}')['goals_home_final'].sum() + \
            df.query(f'away_team == "{team}" & round <= {rnd}')['goals_away_final'].sum()
    return goals


def gc(team, rnd, df):
    """
    Function that takes the number of conceded goals by team until the determined round
    :param team: Team we want to find conceded goals
    :param rnd: Limit round that we will seek
    :param df: Data Frame with games
    :return: A integer number with number of conceded goals
    """
    goals = df.query(f'away_team == "{team}" & round <= {rnd}')['goals_home_final'].sum() + \
            df.query(f'home_team == "{team}" & round <= {rnd}')['goals_away_final'].sum()
    return goals


def get_points(row):
    """
    Function get's number of points of each team based on number of wins and draws
    :param row:row of dataframe, who get's columns wins and draws
    :return: number of points of each team
    """
    points = row['wins'] * 3 + row['draws']
    return points


def ger_table(rnd, df):
    """
    Main function who want's to generate a table of league
    :param rnd: round we want's to limit the visualization
    :param df: dataframe with the info of games
    :return: dataframe with the table
    """
    # make a dictionary to create each column with a function
    data = {}
    data['teams'] = list(df['home_team'].unique())
    data['games'] = [get_games(team, rnd, df) for team in data['teams']]
    data['wins'] = [get_wins(team, rnd, df) for team in data['teams']]
    data['draws'] = [get_draws(team, rnd, df) for team in data['teams']]
    data['loses'] = [get_loses(team, rnd, df) for team in data['teams']]
    data['gp'] = [gp(team, rnd, df) for team in data['teams']]
    data['gc'] = [gc(team, rnd, df) for team in data['teams']]
    # generate a data frame from dict
    table = pd.DataFrame(data)
    # make a balance of goals by the diff of scored and conceded goals
    table['sg'] = table['gp'] - table['gc']
    # work in column of points with a function
    table['points'] = table.apply(lambda row: get_points(row), axis=1)
    # order table by points, set new index and return table with data frame
    table = table.sort_values(by=['points'], ascending=False).reset_index(drop=True)
    table.index = np.arange(1, len(table) + 1)
    return table

def ger_final_results(df):
    final_result=df.groupby('final_result')['final_result'].count()
    total=final_result.sum()
    final_result=(final_result/total).round(2)
    fig=px.bar(x=final_result.index,y=final_result,  labels={'x':'Final Results', 'y':'% of rounds'},text=final_result,title='Percents of Final Results', color=['red','green','blue'],)
    fig.update_traces(texttemplate='%{text:%}')
    fig.update_layout(showlegend=False)
    return(fig)

def first_final_round(df):
    df_aux=pd.crosstab(index=df['1half_result'], columns=df['final_result']).reset_index()
    df_aux.loc[:,['Away','Home','Draw']] = Normalizer(norm='l1').fit_transform(df_aux.loc[:,['Away','Home','Draw']])
    df_aux=df_aux.round(2)
    fig1 = go.Figure(go.Bar(x=df_aux['1half_result'], y=df_aux['Away'], name='Away',text=df_aux['Away'],textposition='inside'))
    fig1.add_trace(go.Bar(x=df_aux['1half_result'], y=df_aux['Draw'], name='Draw',text=df_aux['Draw'],textposition='inside'))
    fig1.add_trace(go.Bar(x=df_aux['1half_result'], y=df_aux['Home'], name='Home',text=df_aux['Home'],textposition='inside'))
    fig1.update_traces(texttemplate='%{text:%}')
    fig1.update_layout(title='Result of First time x Final Result',barmode='stack', xaxis={'categoryorder':'array'},
                yaxis_title='Final Result', xaxis_title='First time Result')
    return(fig1)

def last_games(df,team):
    df_show=df.drop(columns=['url'])
    df_show=df_show.query(f'(home_team == "{team}") | (away_team == "{team}")').sort_values(by=['round'], ascending=False)
    df_show.set_index('round', inplace=True)
    df_show=df_show[['home_team','goals_home_final','goals_away_final','away_team']]
    #df_show=df_show.style.apply(lambda x: ["background: red" if v == team else "" for v in x], axis = 0, inplace=True)
    return df_show.head(5)