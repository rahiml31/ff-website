import pandas as pd
from espn_api.football import League
import json


# Retrieves necessary data for each team and returns a dictionary with said data
def format_data(team, year):
    num_games = team.wins + team.losses + team.ties
    data = {
        'Year': year,
        'Final Rank': team.final_standing,
        'Regular Season Rank': team.standing,
        'Team Name': team.team_name,
        'Owner': ' '.join([team.owners[0]['firstName'], team.owners[0]['lastName']]).title(),
        'Wins': team.wins,
        'Losses': team.losses,
        'Ties': team.ties,
        'Win_Percentage': round(team.wins / num_games, 3),
        'Points For': team.points_for,
        'Points Against': team.points_against,
        'PF/Game': round(team.points_for / num_games, 1),
        'PA/Game': round(team.points_against / num_games, 1)
    }
    return data


if __name__ == "__main__":
    
    secrets = json.load(open('config/secrets.json'))
    years = [2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]

    # Creates a DataFrame containing the final standings for the historical seasons
    yearly_data = []
    for year in years:
        league = League(league_id=401991, year=year, espn_s2=secrets['espn_s2'], swid=secrets['swid'])
        for team in league.standings():
            data = format_data(team, year)
            yearly_data.append(data)
    pdf = pd.DataFrame(yearly_data)

    # Exports the historical records to a CSV
    pdf.to_csv('config/historical_records.csv', index=False)