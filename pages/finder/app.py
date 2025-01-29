import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px

def app():
    st.title("ETF Data Visualization App")
    st.write("Analyze and visualize ETF data with this interactive tool!")

    # Sidebar for user inputs
    st.sidebar.header("Input ETF Tickers")
    tickers = st.sidebar.text_area("Enter ETF tickers (comma-separated):", "SPY, QQQ, DIA")

    # Convert user input to a list of tickers
    ticker_list = [ticker.strip().upper() for ticker in tickers.split(",") if ticker.strip()]

    # Function to fetch data for each ETF
    def fetch_etf_data(ticker):
        try:
            etf = yf.Ticker(ticker)
            return etf
        except Exception as e:
            st.error(f"Error fetching data for {ticker}: {e}")
            return None

    # Fetch ETF information
    st.sidebar.write("Click the button below to fetch ETF data.")
    etf_data = {}

    if st.sidebar.button("Fetch Data"):
        st.markdown(f"Fetching data for: {', '.join(ticker_list)}")
        
        for ticker in ticker_list:
            etf = fetch_etf_data(ticker)
            if etf:
                info = etf.info
                history = etf.history(period="1y")  # Fetch last 1 year of data
                
                etf_data[ticker] = {
                    "info": info,
                    "history": history,
                    "yield5y": info.get('fiveYearAverageReturn', "N/A"),
                    "yield3y": info.get('threeYearAverageReturn', "N/A"),
                    "return_ytd": info.get('ytdReturn', "N/A"),
                    "category": info.get('category', "N/A"),
                    "totalAssets": info.get('totalAssets', "N/A"),
                    "beta3y": info.get('beta3Year', "N/A"),
                    "fundDescription": info.get('longBusinessSummary', "N/A"),
                    "eqHold": info.get('holdings', "N/A"),
                    "secWeights": info.get('sectorWeightings', "N/A"),
                    "topHolds": info.get('topHoldings', "N/A")
                }

        # Display fetched data
        for ticker, data in etf_data.items():
            st.subheader(f"{ticker} Information")
            st.write(f"**Category:** {data['category']}")
            st.write(f"**Total Assets:** {data['totalAssets']}")
            st.write(f"**3-Year Yield:** {data['yield3y']}")
            st.write(f"**5-Year Yield:** {data['yield5y']}")
            st.write(f"**Beta (3Y):** {data['beta3y']}")
            st.write(f"**YTD Return:** {data['return_ytd']}")
            st.write(f"**Fund Description:** {data['fundDescription']}")

            # Display historical price chart
            st.subheader(f"{ticker} Price Chart (1-Year)")

            if not data["history"].empty:
                fig = px.line(data["history"].reset_index(), x="Date", y="Close", title=f"{ticker} Closing Prices")
                st.plotly_chart(fig)
            else:
                st.warning(f"No historical data available for {ticker}.")

    # Step 1: Initialize session state for filters
    if 'investment_strategy' not in st.session_state:
        st.session_state.investment_strategy = []
    if 'asset_class' not in st.session_state:
        st.session_state.asset_class = []
    if 'asset_region' not in st.session_state:
        st.session_state.asset_region = []
    if 'subsegment' not in st.session_state:
        st.session_state.subsegment = []
    if 'esg_rating' not in st.session_state:
        st.session_state.esg_rating = []
    if 'query_str' not in st.session_state:
        st.session_state.query_str = ""
    if 'df_filtered' not in st.session_state:
        st.session_state.df_filtered = pd.DataFrame()  # Initialize as empty DataFrame

