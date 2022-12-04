import yfinance as yf
import streamlit as st
import pandas as pd

st.write("""
# Simple Stock Price App

Shown are the stock **Closing Price** and ***Volume*** of Google!

""")
tickerSymbol = "GOOGL"
tickerData = yf.Ticker(tickerSymbol)

tickerDf =tickerData.history(period='1d', start='2019-1-01', end='2022-1-01')
print(type(tickerDf))
print(tickerDf.info())
st.line_chart(tickerDf.Close)
st.line_chart(tickerDf.Volume)


