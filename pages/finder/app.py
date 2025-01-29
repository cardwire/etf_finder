import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px

def app():
    st.title("ETF Data Visualization App")
    st.write("Analyze and visualize ETF data with this interactive tool!")

    # Sidebar Inputs
    st.sidebar.header("Input ETF Tickers")
    tickers = st.sidebar.text_area("Enter ETF tickers (comma-separated):", "SPY, QQQ, DIA")
    ticker_list = [ticker.strip().upper() for ticker in tickers.split(",") if ticker.strip()]

    # Function to Fetch ETF Data
    def fetch_etf_data(ticker):
        try:
            etf = yf.Ticker(ticker)
            return {
                "info": etf.info,
                "history": etf.history(period="1y")  # Fetch last 1 year of data
            }
        except Exception as e:
            st.error(f"Error fetching data for {ticker}: {e}")
            return None

    # Fetch ETF Information
    st.sidebar.write("Click the button below to fetch ETF data.")
    etf_data = {}

    if st.sidebar.button("Fetch Data"):
        st.markdown(f"Fetching data for: {', '.join(ticker_list)}")
        
        for ticker in ticker_list:
            data = fetch_etf_data(ticker)
            if data:
                info = data["info"]
                history = data["history"]
                
                etf_data[ticker] = {
                    "category": info.get('category', "N/A"),
                    "totalAssets": info.get('totalAssets', "N/A"),
                    "yield3y": info.get('threeYearAverageReturn', "N/A"),
                    "yield5y": info.get('fiveYearAverageReturn', "N/A"),
                    "beta3y": info.get('beta3Year', "N/A"),
                    "return_ytd": info.get('ytdReturn', "N/A"),
                    "description": info.get('longBusinessSummary', "N/A"),
                    "history": history
                }

        # Display ETF Data
        for ticker, data in etf_data.items():
            st.subheader(f"{ticker} Information")
            st.write(f"**Category:** {data['category']}")
            st.write(f"**Total Assets:** {data['totalAssets']}")
            st.write(f"**3-Year Yield:** {data['yield3y']}")
            st.write(f"**5-Year Yield:** {data['yield5y']}")
            st.write(f"**Beta (3Y):** {data['beta3y']}")
            st.write(f"**YTD Return:** {data['return_ytd']}")

            # Expandable Fund Description
            with st.expander(f"Fund Description of {ticker}"):
                st.write(data['description'])

            # ETF Historical Price Chart
            if not data["history"].empty:
                st.subheader(f"{ticker} Price Chart (1-Year)")
                fig = px.line(data["history"].reset_index(), x="Date", y="Close", title=f"{ticker} Closing Prices")
                st.plotly_chart(fig)
            else:
                st.warning(f"No historical data available for {ticker}.")

    # ETF Comparison Table
    if etf_data:
        st.subheader("ETF Comparison Table")
        df_comparison = pd.DataFrame(etf_data).T
        df_comparison = df_comparison.drop(columns=["description", "history"])  # Remove non-numeric columns
        st.dataframe(df_comparison)



