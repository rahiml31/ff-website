# Makes the website
# Has 2 tabs: current, historical
# current showcases the current season stats (standings, power rankings etc.)
# make power rankings into a bump chart
# historical showcases the overall records for all players of the league
# have a trophy for number of champs etc.

import pandas as pd
import streamlit as st


def current():
    st.write('current season')


# Depicts the overall statistics for players who have played in the League
def historical():
    hist = pd.read_csv('data/historical_records.csv')
    st.table(hist)


if __name__ == "__main__":
    
    st.write('# Punchaat Committee Fantasy Football Website')
    tab1, tab2 = st.tabs(['Current', 'Historical'])

    with tab1:
        historical()
    
    with tab2:
        current()