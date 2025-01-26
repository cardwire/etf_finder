import streamlit as st
import ipywidgets
import streamlit_elements
import pandas as pd
import numpy as np
import datetime
from time import sleep
import yfinance as yf
import plotly.graph_objs as go
import plotly.express as px


def app():

    st.title("ETF Data Visualization App")
    st.write("Analyze and visualize ETF data with this interactive tool!")

    # Sidebar for user inputs
    st.sidebar.header("Input ETF Tickers")
    tickers = st.sidebar.text_area("Enter ETF tickers (comma-separated):", "SPY, QQQ, DIA")
    
    # Convert user input to a list of tickers
    ticker_list = [ticker.strip() for ticker in tickers.split(",")]

    
    # Function to fetch data for each ticker
    def fetch_etf_data(ticker):
        try:
            data = yf.Ticker(ticker)
            return data
        except Exception as e:
            st.error(f"Error fetching data for {ticker}: {e}")
            return None


 # Fetch information for each ETF
    st.sidebar.write("Click the button below to fetch ETF data.")
    if st.sidebar.button("Fetch Data"):
        st.markdown(f"# Fetching data for: {', '.join(ticker_list)}")

        etf_data = {}
        for ticker in ticker_list:
            etf = fetch_etf_data(ticker)
            if etf:
                etf_data[ticker] = {
                    "info": etf.info,
                    "history": etf.history(period="1y"),
                }
        
        # Display information and visualizations
        for ticker, data in etf_data.items():
            st.subheader(f"{ticker} Information")
            st.write(data["info"])

            st.subheader(f"{ticker} Price Chart (1-Year)")
            if not data["history"].empty:
                fig = px.line(
                    data["history"].reset_index(),
                    x="Date",
                    y="Close",
                    title=f"{ticker} Closing Prices",
                )
                st.plotly_chart(fig)
            else:
                st.warning(f"No historical data available for {ticker}.")

    
    '''
    
    

    try:
        df = pd.read_csv('database.csv')
    except FileNotFoundError:
        st.error("Error: CSV file not found. Please check the file path.")
        df = pd.DataFrame()
   
    
    # Step 0: Define filter_set
    filter_set = df[['investment_strategy', 'asset_class', 'asset_region', 'subsegment', 'esg_rating']]
    df_target = df[['ticker', 'investment_strategy', 'asset_class', 'asset_region', 'subsegment', 'esg_rating']]    
    df_filtered = df_target

     '''

    
  #  st.title("ETF Finder")
   # st.markdown('### __This is the ETF Finder Page__ ')   
   # st.markdown(f'### __set the filters to select your ETFs__ ')
    #st.markdown('__Note: all ETFs provide data on every filter. The number of ETFs that provide data on a specific filter is shown in this barplot__') 
    
  


   

    # Step 1: Initialize session state for filters if not already present
    
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
        st.session_state.df_filtered = df_filtered

    # Step 2: Create Streamlit widgets for filters
    investment_strategy = st.multiselect('Investment Strategy', options=['standard', 'leveraged', 'inverse'], default=st.session_state.investment_strategy)
    asset_class = st.multiselect('asset_class', options=['equity', 'fixed_income', 'commodities', 'asset_allocation','currency', 'alternatives', 'asset_allocations'], default=st.session_state.asset_class)
    asset_region = st.multiselect('asset_region', options=['us', 'dev_markets', 'emerg_markets', 'global', 'europe','asia_pacific_wo_brics', 'brics', 'america_wo_us', 'mid_east','africa_wo_brics'], default=st.session_state.asset_region)
    subsegment = st.multiselect('subsegment', options=['large_cap', 'total_market', 'broad_based', 'mid_cap', 'small_cap','not_specified', 'high_dividend_yield', 'government', 'corporate','extended_market', 'other', 'low carbon', 'industry_and_tech'], default=st.session_state.subsegment)
    esg_rating = st.multiselect('esg_rating', options=['AAA', 'AA', 'A', 'BBB', 'BB', 'B', 'CCC', 'CC', 'C'], default=st.session_state.esg_rating)
   
    # Step 3: Define the callback function to update session state
    def on_change():
        st.session_state.investment_strategy = investment_strategy
        st.session_state.asset_class = asset_class
        st.session_state.asset_region = asset_region
        st.session_state.subsegment = subsegment
        st.session_state.esg_rating = esg_rating
        st.session_state.df_filtered = df_filtered
       

    # Step 4: Create the "Apply Filters" button to trigger filtering
    
    if st.button('Filter the Database'):
        on_change()

        # Construct a dynamic query string based on session state values
        query_str = ""

        if st.session_state.investment_strategy:
            query_str += f"(investment_strategy in {st.session_state.investment_strategy})"

            if st.session_state.asset_class:
                if query_str:
                    query_str += " and "
                query_str += f"(asset_class in {st.session_state.asset_class})"

            if st.session_state.asset_region:
                if query_str:
                    query_str += " and "
                query_str += f"(asset_region in {st.session_state.asset_region})"

            if st.session_state.subsegment:
                if query_str:
                    query_str += " and "
                query_str += f"(subsegment in {st.session_state.subsegment})"

            if st.session_state.esg_rating:
                if query_str:
                    query_str += " and "
                query_str += f"(esg_rating in {st.session_state.esg_rating})"
            
            
            

        

        if query_str == "":
            df_filtered = df_target
        else:
            df_filtered = df_target.query(query_str)

        # Display the count of unique tickers and the list of tickers
        n = df_filtered['ticker'].count()  # Use the total count from unfiltered data
        st.title(f"You selected: {n} ETFs")
        st.write("List of tickers:")
        List = df_filtered['ticker'].tolist()
        st.write('Here is a ticker list of your selection')
        st.write(List)
        
        st.session_state.query_str = query_str
        st.session_state.df_filtered = df_filtered
        

        
    st.divider()

    # Use the filtered_df for further processing or display
    st.write("Your Selection:")
    st.write(df_filtered.head())
    
