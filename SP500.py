import pandas as pd
import yfinance as yf
import streamlit as st
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import ssl
import base64
# -----------------------------------------------------------------
st.set_option('deprecation.showPyplotGlobalUse', False)
ssl._create_default_https_context = ssl._create_unverified_context
# -----------------------------------------------------------------

st.title('S&P 500 App')

st.markdown("""
This app scrapes the list of the **S&P 500** from (Wikipedia)
* **Python libraries:** base64, pandas, streamlit, numpy, matplotlib, seaborn
* **Data Source:**[Wikipedia](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies)


""")

st.sidebar.header("User Input Features")

# Web scraping S&P500

@st.cache
def load_data():
    """
    This func scrapes/reads the html of the SP500 companies on Wiki.

    return: dataframe
    """
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    html = pd.read_html(url,header=0)
    df = html[0]
    return df


df = load_data()

sector = df.groupby('GICS Sector')
# Sidebar - Sector selection
sorted_sector_unique = sorted( df['GICS Sector'].unique() )
selected_sector = st.sidebar.multiselect('Sector', sorted_sector_unique, sorted_sector_unique)


# Filtering data
df_selected_sector = df[ (df['GICS Sector'].isin(selected_sector)) ]
st.header('Display Companies in Selected Sector')
st.write('Data Dimension: ' + str(df_selected_sector.shape[0]) + ' rows and ' + str(df_selected_sector.shape[1]) + ' columns.')
st.dataframe(df_selected_sector)



# Download S&P500 data
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
def filedownload(df):
    """
    This function takes a dataframe and encodes it with base64 then passes it through  a href tag.
    :param df:
    :return:
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="SP500.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(df_selected_sector), unsafe_allow_html=True)


# https://pypi.org/project/yfinance/

data = yf.download(
        tickers = list(df_selected_sector[:10].Symbol),
        period = "ytd",
        interval = "1d",
        group_by = 'ticker',
        auto_adjust = True,
        prepost = True,
        threads = True,
        proxy = None
)

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

add_bg_from_local("wallstreet2.jpeg")

# Plot Closing Price of Query Symbol
def price_plot(symbol):
    """
    This function filters out the symbol , sets the index to column Date
    rotates xticks,plots labels and returns a plot(s).
    :param symbol: 
    :return: the data plotted
    """
    df = pd.DataFrame(data[symbol].Close)
    df['Date'] = df.index
    plt.fill_between(df.Date, df.Close, color='blue', alpha=0.3)
    plt.plot(df.Date, df.Close, color='skyblue', alpha=0.8)
    plt.xticks(rotation=90)
    plt.title(symbol, fontweight='bold')
    plt.xlabel('Date', fontweight='bold')
    plt.ylabel('Closing Price', fontweight='bold')
    return st.pyplot()



num_company = st.sidebar.slider('Number of Companies', 1, 5)

if st.button('Show Plots'):
    st.header('Stock Closing Price')
    for i in list(df_selected_sector.Symbol)[:num_company]:
        price_plot(i)