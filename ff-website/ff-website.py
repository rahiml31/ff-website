# Makes the website
# Has 2 tabs: current, historical
# current showcases the current season stats (standings, power rankings etc.)
# make power rankings into a bump chart
# historical showcases the overall records for all players of the league
# have a trophy for number of champs etc.

import pandas as pd
import streamlit as st
import json
from espn_api.football import League
import altair as alt


# Depicts the standings, power rankings, and current weekly scorebard for the current season
def current():
    # add a flag for if in playoffs.
    # if not in playoffs: trigger regular_season()
    #   contains bump chart for power rankings, standings, scorebard and more.
    #   add ability to select a team and highlight it on bump chart and on the other stuff too
    # if in playoffs: trigger playoffs()
    #   has matchups and a bracket showcasing path to finals
    # bump chart - https://stackoverflow.com/questions/68095438/how-to-make-a-bump-chart
    # https://altair.streamlit.app/Bump_Chart
    secrets = json.load(open('config/secrets.json'))
    league = League(league_id=secrets['league_id'], year=2023, espn_s2=secrets['espn_s2'], swid=secrets['swid'])
    last_regular_season_week = league.settings.reg_season_count
    current_week = league.current_week
    if current_week > last_regular_season_week:
        playoffs(league)
    else:
        regular_season(league)


# Depicts the Playoff Bracket and percentage chance of winning the championship
def playoffs(league):
    st.write('# playoffs')


# Depicts the current week's scoreboard/matchups and the power rankings for this season
def regular_season(league):
    st.write('# regular season')
    power_ranks_df = get_power_rankings(league)
    st.table(power_ranks_df)

# Gets the power rankings for the entire season in a Data Frame
def get_power_rankings(league):
    cw = league.current_week
    teams = [t.team_name for t in league.teams]
    main = pd.DataFrame(teams, columns=['team_name'])
    for week in range(1, cw):
        pw0 = league.power_rankings(week=week)
        pw1 = [team[1].team_name for team in pw0]
        pw = tuple(zip(pw1, range(1, len(pw1) + 1)))
        df = pd.DataFrame(pw, columns=['team_name', 'week_' + str(week)])
        main = main.merge(df, on='team_name')
    return main

# Depicts the overall statistics for players who have played in the League
def historical():
    hist = pd.read_csv('config/historical_records.csv')
    years_played = hist.groupby('Owner')['Year'].count().reset_index().sort_values(by=['Year', 'Owner'], ascending=[False, True]).reset_index(drop=True)
    owners = years_played.Owner.to_list()
    data = []
    for owner in owners:
        owner_json = historical_filtering(hist[hist.Owner == owner])
        data.append(owner_json)
    data_df = pd.DataFrame(data).sort_values(by=['Years Participated', 'champ_num', 'reg_champ_num', 'Win Percentage'],
                                             ascending=[False, False, False, False]
                                            ).reset_index(drop=True).drop(columns=['champ_num', 'reg_champ_num'])
    st.dataframe(data_df, hide_index=True)


# Takes the Owner filtered historical records and creates the overall table depicting the results of that Owner
def historical_filtering(df):
    champs = df[df['Final Rank'] == 1].groupby('Final Rank')['Year'].apply(list).to_list()
    champ_num = len(champs[0]) if len(champs) > 0 else 0
    champs = ', '.join([str(i) for i in champs[0]]) if len(champs) > 0 else ''
    reg_champs = df[df['Regular Season Rank'] == 1].groupby('Regular Season Rank')['Year'].apply(list).to_list()
    reg_champ_num = len(reg_champs[0]) if len(reg_champs) > 0 else 0
    reg_champs = ', '.join([str(i) for i in reg_champs[0]]) if len(reg_champs) > 0 else ''
    num_years_participated = len(df)
    wins = df.Wins.sum()
    losses = df.Losses.sum()
    ties = df.Ties.sum()
    num_games = wins + losses + ties
    points_for = round(df['Points For'].sum(), 2)
    points_against = round(df['Points Against'].sum(), 2)
    pf_per = round(points_for / num_games, 2)
    pa_per = round(points_against / num_games, 2)
    win_percentage = (wins + (ties * 0.5)) / num_games
    player_name = df.Owner.unique()[0]
    data = {
        'Owner': player_name,
        'Years Participated': num_years_participated,
        'champ_num': champ_num,
        'reg_champ_num': reg_champ_num,
        'Champion': champs,
        'Regular Season Champion': reg_champs,
        'Number Games': num_games,
        'Wins': wins,
        'Losses': losses,
        'Ties': ties,
        'Win Percentage': win_percentage,
        'Total Points For': points_for,
        'Total Points Against': points_against,
        'Total PF/Game': pf_per,
        'Total PA/Game': pa_per
    }
    return data


if __name__ == "__main__":
    
    st.set_page_config(layout="wide")
    st.write('# Punchaat Committee Fantasy Football Website')
    tab1, tab2 = st.tabs(['Current', 'Historical'])

    with tab1:
        current()
    
    with tab2:
        historical()
