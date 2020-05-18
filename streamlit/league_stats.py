import pandas as pd
import numpy as np

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
