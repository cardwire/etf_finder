
import streamlit as st
import pandas as pd
import yfinance as yf   
from datetime import date
from prophet import Prophet
from prophet.plot import plot_plotly
import matplotlib.pyplot as plt

START = "2015-01-01"
STOP = date.today().strftime("%Y-%m-%d")
methods = ['Prophet', 'XGBoost']

df = pd.read_csv('database.csv')

def app():
    st.title("Forecast Page")
    st.markdown('### __This is the Forecast Page__ ')

    tics = df['ticker'].tolist()
    funds = st.selectbox("Select an ETF to see its time series data:", tics)
    method = st.selectbox("Select a forecasting method:", methods)

    series_etf = funds
    n_years = st.slider('Years of prediction:', 1, 4)
    period = n_years * 365
    
    @st.cache_data
    def load_data(ticker):
        data = yf.download(ticker, START, STOP)
        data.reset_index(inplace=True)
        return data

    data_load_state = st.text('Loading data...')
    data = load_data(series_etf)
    data_load_state.text('Loading data... done!')
        
    st.subheader('Raw data')
    st.write(data.tail())
    
    # Forecasting
    df_train = data[['Date','Close']]
    df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})
        
    m = Prophet()
    m.fit(df_train)
    future = m.make_future_dataframe(periods=period)
    forecast = m.predict(future)
        
    st.subheader('Forecast data')
    st.write(forecast.tail())
        
    st.write(f'Forecast plot for {n_years} years')
    fig1 = plot_plotly(m, forecast)
    fig1.update_xaxes(showline=True, linewidth=1.5, linecolor='white', 
                  gridcolor='grey', gridwidth=1,
                  zeroline=True, zerolinewidth=1.5, zerolinecolor='white'),
    for trace in fig1['data']:
        trace.line.color = 'firebrick'
        
    st.plotly_chart(fig1)
    
    st.write("Forecast components")
    fig2 = m.plot_components(forecast)

    # Update the appearance of the components plot
    colors = ['yellow', 'green', 'hotpink']
    for i, comp in enumerate(fig2.get_axes()):
        comp.lines[0].set_color(colors[i])

        # Update the appearance of the components plot
    colors = ['yellow', 'green', 'hotpink']
    for i, comp in enumerate(fig2.get_axes()):
        comp.lines[0].set_color(colors[i])

    # Update layout for components plot
    plt.savefig('none', transparent=True)  # Make the whole plot transparent
    

    for comp in fig2.get_axes():
        comp.xaxis.label.set_color('white')
        comp.yaxis.label.set_color('white')
        comp.tick_params(axis='x', colors='white')
        comp.tick_params(axis='y', colors='white')

    st.pyplot(fig2)

app()

