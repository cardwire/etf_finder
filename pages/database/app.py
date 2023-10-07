import streamlit as st
import pandas as pd
import yahooquery as yq
import plotly.express as px

# Load data
df = pd.read_csv('database.csv')
t_list = df['ticker'].tolist()

def get_holdings(selected_ticker):
    fund = yq.Ticker(selected_ticker)
    holdings_info = fund.fund_holding_info[selected_ticker]
    
    if 'holdings' in holdings_info:
        holdings = pd.DataFrame(holdings_info['holdings'])
        return holdings
    else:
        st.warning(f"No holdings information available for {selected_ticker}")
        return None

def get_sector_weightings(selected_ticker):
    fund = yq.Ticker(selected_ticker)
    sector_weightings = fund.fund_sector_weightings.reset_index()
    sector_weightings = pd.DataFrame(sector_weightings)
    sector_weightings.columns = ['sector', 'weight']
    return sector_weightings

def app():
    st.title("ETF Database")
    st.subheader('Here you can explore our Database')

    st.divider()

    st.dataframe(df)
    
    st.divider()
    
    st.markdown('## With ydata_profiling you can explore our Database by detailed statistical Analysis')
    
    st.markdown('### __Select an ETF to see its statistical features__ ')
    selected_ticker = st.selectbox("Select an ETF:", t_list)
    
    # Call the function and check if holdings is not None before creating the chart
    holdings = get_holdings(selected_ticker)

    if holdings is not None:
        fig = px.bar(holdings, y='holdingPercent', x='symbol', title=f'{selected_ticker} Holdings', color='symbol')
        st.plotly_chart(fig)
    else:
        st.write("No holdings information available for", selected_ticker)
    

    # Call the function to get sector weightings
    sector_weightings = get_sector_weightings(selected_ticker)

    if sector_weightings is not None:
        fig = px.bar(sector_weightings, y='weight', x='sector', title=f'{selected_ticker} Sector Weightings', color='sector')
        st.plotly_chart(fig)
    else:
        st.write("No sector weightings information available for", selected_ticker)
        
# Call the app function
app()
