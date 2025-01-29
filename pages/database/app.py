import streamlit as st
import pandas as pd
import yfinance as yf
import time
import plotly.graph_objects as go
import plotly.express as px

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
                funds_data = etf.get_fundamentals()  # Fetch fundamental fund data
                
                return {
                    "ticker": ticker,
                    "category": info.get("category", "N/A"),
                    "totalAssets": info.get("totalAssets", "N/A"),
                    "yield3y": info.get("threeYearAverageReturn", "N/A"),
                    "yield5y": info.get("fiveYearAverageReturn", "N/A"),
                    "return_ytd": info.get("ytdReturn", "N/A"),
                    "beta3y": info.get("beta3Year", "N/A"),
                    "description": funds_data.get("description", "N/A"),
                    "equity_holdings": funds_data.get("equityHoldings", {}),
                    "fund_overview": funds_data.get("fundOverview", {}),
                    "sector_weightings": funds_data.get("sectorWeightings", {}),
                    "top_holdings": funds_data.get("topHoldings", {}),
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

        # Display Historical Data & Candlestick Chart
        for ticker, data in etf_data.items():
            if data and not data["history"].empty:
                st.subheader(f"{ticker} - Historical Data & Candlestick Chart")

                # Expandable Table for Historical Data
                with st.expander(f"View {ticker} Historical Data"):
                    st.dataframe(data["history"])

                # Candlestick Chart
                hist = data["history"].reset_index()
                fig = go.Figure(data=[
                    go.Candlestick(
                        x=hist["Date"],
                        open=hist["Open"],
                        high=hist["High"],
                        low=hist["Low"],
                        close=hist["Close"],
                        name="Candlestick"
                    )
                ])
                fig.update_layout(title=f"{ticker} Candlestick Chart (1-Year)", xaxis_title="Date", yaxis_title="Price ($)")
                st.plotly_chart(fig)

        # ETF Fund Data Section
        for ticker, data in etf_data.items():
            st.subheader(f"{ticker} - Fund Data")

            # Fund Description
            with st.expander(f"Fund Description of {ticker}"):
                st.write(data["description"])

            # Sector Weightings Pie Chart
            if data["sector_weightings"]:
                sector_df = pd.DataFrame(data["sector_weightings"].items(), columns=["Sector", "Weight"])
                fig = px.pie(sector_df, names="Sector", values="Weight", title=f"{ticker} Sector Weightings")
                st.plotly_chart(fig)

            # Top Holdings Bar Chart
            if data["top_holdings"]:
                holdings_df = pd.DataFrame(data["top_holdings"].items(), columns=["Company", "Weight"])
                fig = px.bar(holdings_df, x="Company", y="Weight", title=f"{ticker} Top Holdings", text_auto=True)
                st.plotly_chart(fig)

            # Equity Holdings Overview
            with st.expander(f"{ticker} - Equity Holdings Overview"):
                st.json(data["equity_holdings"])

            # Fund Overview
            with st.expander(f"{ticker} - Fund Overview"):
                st.json(data["fund_overview"])
