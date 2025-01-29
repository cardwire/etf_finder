import streamlit as st
import yfinance as yf
import plotly.express as px

def app():
    st.title("ETF Database")

    #get all tickers from yfinance ETF list
    all_etfs = yf.Tickers(" ").tickers
    etf_tickers = [etf.ticker for etf in all_etfs]
    etf_tickers.sort()

    #select ETF
    ticker = st.selectbox("Select ETF", etf_tickers)

    #get ETF data
    etf = yf.Ticker(ticker)
    data = etf.history(period="1y")

    #plot ETF data
    fig = px.line(data, x=data.index, y="Close", title=f"{ticker} Closing Price")
    st.plotly_chart(fig)

    #display ETF information
    info = etf.info
    st.subheader(f"{ticker} Information")
    st.write(info)
