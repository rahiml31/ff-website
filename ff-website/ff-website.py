# Makes the website
# Has 2 tabs: current, historical
# current showcases the current season stats (standings, power rankings etc.)
# make power rankings into a bump chart
# historical showcases the overall records for all players of the league
# have a trophy for number of champs etc.

import pandas as pd
import streamlit as st


# Depicts the standings, power rankings, and current weekly scorebard for the current season
def current():
    st.write('current season')


# Depicts the overall statistics for players who have played in the League
def historical():
    hist = pd.read_csv('data/historical_records.csv')
    years_played = hist.groupby('Owner')['Year'].count().reset_index().sort_values(by=['Year', 'Owner'], ascending=[False, True]).reset_index(drop=True)
    st.write('Years played per player')
    st.table(years_played)
    # for each owner, go into new function and create the data requiredto create the final chart
    st.table(hist)


# Takes the Owner filtered historical records and creates the overall table depicting the results of that Owner
def historical_filtering(df):
    pass


if __name__ == "__main__":
    
    st.write('# Punchaat Committee Fantasy Football Website')
    tab1, tab2 = st.tabs(['Current', 'Historical'])

    with tab1:
        historical()
    
    with tab2:
        current()

    
    """
    Notes to remember:
    For adding images/emoji trophies in historical
        https://discuss.streamlit.io/t/add-image-and-header-to-streamlit-dataframe-table/36065/3
    
    """