import pandas as pd
import numpy as np

def get_wins(team, rnd, df):
    mask1 = (df['home_team'] == team) & (df['final_result'] == 'Home') & (df['round'] <= rnd)
    mask2 = (df['away_team'] == team) & (df['final_result'] == 'Away') & (df['round'] <= rnd)
    return len(df.loc[mask1 | mask2, 'round'])


def get_games(team, rnd, df):
    mask1 = ((df['home_team'] == team) | (df['away_team'] == team)) & (df['round'] <= rnd)
    return len(df.loc[mask1, 'round'])


def get_draws(team, rnd, df):
    mask1 = ((df['home_team'] == team) | (df['away_team'] == team)) & (df['final_result'] == 'Draw') & (
                df['round'] <= rnd)
    return len(df.loc[mask1, 'round'])


def get_loses(team, rnd, df):
    mask1 = (df['home_team'] == team) & (df['final_result'] == 'Away') & (df['round'] <= rnd)
    mask2 = (df['away_team'] == team) & (df['final_result'] == 'Home') & (df['round'] <= rnd)
    return len(df.loc[mask1 | mask2, 'round'])


def gp(team, rnd, df):
    goals = df.query(f'home_team == "{team}" & round <= {rnd}')['goals_home_final'].sum() + \
            df.query(f'away_team == "{team}" & round <= {rnd}')['goals_away_final'].sum()
    return goals


def gc(team, rnd, df):
    goals = df.query(f'away_team == "{team}" & round <= {rnd}')['goals_home_final'].sum() + \
            df.query(f'home_team == "{team}" & round <= {rnd}')['goals_away_final'].sum()
    return goals


def get_points(row):
    points = row['wins'] * 3 + row['draws']
    return points


def ger_table(rnd, df):
    data = {}
    data['teams'] = list(df['home_team'].unique())
    data['games'] = [get_games(team, rnd, df) for team in data['teams']]
    data['wins'] = [get_wins(team, rnd, df) for team in data['teams']]
    data['draws'] = [get_draws(team, rnd, df) for team in data['teams']]
    data['loses'] = [get_loses(team, rnd, df) for team in data['teams']]
    data['gp'] = [gp(team, rnd, df) for team in data['teams']]
    data['gc'] = [gc(team, rnd, df) for team in data['teams']]
    table = pd.DataFrame(data)
    table['sg'] = table['gp'] - table['gc']
    table['points'] = table.apply(lambda row: get_points(row), axis=1)
    table = table.sort_values(by=['points'], ascending=False).reset_index(drop=True)
    table.index = np.arange(1, len(table) + 1)
    return table
