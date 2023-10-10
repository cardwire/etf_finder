import streamlit as st
import ipywidgets
import streamlit_elements
import pandas as pd
import matplotlib as mpl
from matplotlib import pyplot as plt
import seaborn as sns

def app():
   df = pd.read_csv('database.csv')
   df = pd.DataFrame()
    
   # Step 0: Define filter_set
   filter_set = df[['investment_strategy', 'asset_class', 'asset_region', 'subsegment', 'esg_rating']]
   df_target = df[['ticker', 'investment_strategy', 'asset_class', 'asset_region', 'subsegment', 'esg_rating']]    
   df_filtered = df_target
    
   st.title("ETF Finder")
   st.markdown('### __This is the ETF Finder Page__ ')   
   st.markdown(f'### __set the filters to select your ETFs__ ')
   st.markdown('__Note: all ETFs provide data on every filter. The number of ETFs that provide data on a specific filter is shown in this barplot__') 
    


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

   ''' st.write("Current Session State:")
       st.write(st.session_state)

    
    #Control: Display the current session state for filters
    st.write("Current Session State:")
    st.write(st.session_state)
    st.write("Current Query String:")
    st.write(query_str)'''
