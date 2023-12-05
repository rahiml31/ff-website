import pandas as pd
from espn_api.football import League


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
    
    espn_s2 = 'AEChd7Nj9HjsCFN9ut0Cl9PushSfDj%2FgGpRDzGJdtDZ47bEcLsQAwFOVzhy0Ui8xRlDJkWWOxLJHSEa8NgS7sc%2F%2BtzLkwgC%2FhIbX5YwzqSQDWGi7mwNu0iU1btyXh04gCYz50DrbfnTk1KrtC44SFhKXh0ajGhfCCzEjJoxLGoa4gfTMsL5YD2yA17HNCvv7vCLApqZ1RM52cUIwDUvR1CDsj6ZwvN9AXuiZ%2F8hDn222h1tJ68gGAyUjVxXOnmYGjVu76RycLF83Bcp5A%2BMc%2B4pm'
    swid = '{AA3E68CA-5D8E-46B6-BD21-3CA1A769BC3A}'
    years = [2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]

    # Creates a DataFrame containing the final standings for the historical seasons
    yearly_data = []
    for year in years:
        league = League(league_id=401991, year=year, espn_s2=espn_s2, swid=swid)
        for team in league.standings():
            data = format_data(team, year)
            yearly_data.append(data)
    pdf = pd.DataFrame(yearly_data)
    
    # Exports the historical records to a CSV
    pdf.to_csv('data/historical_records.csv')