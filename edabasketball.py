import pandas as pd
#import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np
import ssl
import base64
ssl._create_default_https_context = ssl._create_unverified_context


def add_bg_from_local(image_file):
    """

    :param image_file:
    :return: image as backgroung
    """
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
add_bg_from_local("top4.jpeg")

st.title('NBA Player Stats Explorer')


st.markdown("""
This app performs simple webscraping of NBA player stats data!
* **Python Libraries:** base64, pandas, streamlit
* **Data Source:** https://www.basketball-reference.com

""")

st.sidebar.header('User input Features')
selected_year = st.sidebar.selectbox('Year',list(reversed(range(1950,2023))))





@st.cache
def load_data(year):
    """
    This function scrapes nba data off a website, fills na with 0
    drops a column then returns a dataframe.
    :param year:
    :return: dataframe
    """
    url = "https://www.basketball-reference.com/leagues/NBA_" + str(year) + "_per_game.html"
    html = pd.read_html(url, header=0)
    df = html[0]
    raw = df
    raw = raw.fillna(0)
    playerstats = raw.drop(['Rk'], axis=1)
    return playerstats
playerstats = load_data(selected_year)


# Sidebar - Team selection
sorted_unique_team = sorted(playerstats.Tm.unique())
selected_team = st.sidebar.multiselect('Team', sorted_unique_team, sorted_unique_team)


# Sidebar - Position selection
unique_pos = ['C','PF','SF','PG','SG']
selected_pos = st.sidebar.multiselect('Position', unique_pos, unique_pos)

# Filtering data
df_selected_team = playerstats[(playerstats.Tm.isin(selected_team)) & (playerstats.Pos.isin(selected_pos))]

st.header('Display Player Stats of Selected Team(s)')
st.write('Data Dimension: ' + str(df_selected_team.shape[0]) + ' rows and ' + str(df_selected_team.shape[1]) + ' columns.')
st.dataframe(df_selected_team)


# Download NBA player stats data

# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806

def filedownload(df):

    """
    This is how you download a file via streamlit
    :param df:
    :return: file
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(df_selected_team), unsafe_allow_html=True)

# Heatmap
if st.button('Intercorrelation Heatmap'):
    st.header('Intercorrelation Matrix Heatmap')
    df_selected_team.to_csv('output.csv',index=False)
    df = pd.read_csv('output.csv')

    corr = df.corr()
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True
    with sns.axes_style("dark"):
        fig, ax = plt.subplots(figsize=(7, 5))
        ax = sns.heatmap(corr, mask=mask, vmax=1, square=True)
    st.pyplot(fig)