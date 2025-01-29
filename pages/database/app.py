import streamlit as st
import pandas as pd
import yfinance as yf
import time

def app():
    st.title("ETF Database")
    st.write("Fetch and display ETF details in a structured database.")

    # Sidebar: Ticker Input
    st.sidebar.header("Enter ETF Tickers")
    tickers = st.sidebar.text_area("Enter tickers (comma-separated):", "SPY, QQQ, DIA")
    ticker_list = [ticker.strip().upper() for ticker in tickers.split(",") if ticker.strip()]

    # Button to Fetch Data
    if st.sidebar.button("Fetch Data"):
        st.write("Fetching ETF data... Please wait.")
        progress_bar = st.progress(0)
        
        etf_data = {}
        total_tickers = len(ticker_list)

        # Function to fetch data for a single ETF
        def fetch_etf_data(ticker):
            try:
                etf = yf.Ticker(ticker)
                info = etf.info
                history = etf.history(period="1y")

                return {
                    "ticker": ticker,
                    "category": info.get("category", "N/A"),
                    "totalAssets": info.get("totalAssets", "N/A"),
                    "yield3y": info.get("threeYearAverageReturn", "N/A"),
                    "yield5y": info.get("fiveYearAverageReturn", "N/A"),
                    "return_ytd": info.get("ytdReturn", "N/A"),
                    "beta3y": info.get("beta3Year", "N/A"),
                    "description": info.get("longBusinessSummary", "N/A"),
                    "history": history
                }
            except Exception as e:
                st.error(f"Error fetching data for {ticker}: {e}")
                return None

        # Fetch ETF Data for Each Ticker
        for i, ticker in enumerate(ticker_list):
            etf_data[ticker] = fetch_etf_data(ticker)
            progress_bar.progress((i + 1) / total_tickers)
            time.sleep(0.5)  # Simulating API delay

        # Convert Data to Pandas DataFrame for Display
        df_summary = pd.DataFrame([
            {
                "Ticker": data["ticker"],
                "Category": data["category"],
                "Total Assets ($)": data["totalAssets"],
                "3Y Yield (%)": data["yield3y"],
                "5Y Yield (%)": data["yield5y"],
                "YTD Return (%)": data["return_ytd"],
                "Beta (3Y)": data["beta3y"]
            }
            for data in etf_data.values() if data is not None
        ])

        # Display ETF Summary Table
        st.subheader("ETF Summary Data")
        st.dataframe(df_summary)

        # Display Historical Data for Each ETF
        for ticker, data in etf_data.items():
            if data and not data["history"].empty:
                st.subheader(f"{ticker} - Historical Price Data")
                st.dataframe(data["history"])

            # Expandable Fund Description
            with st.expander(f"Fund Description of {ticker}"):
                st.write(data["description"])

