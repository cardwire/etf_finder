import streamlit as st
from streamlit_option_menu import option_menu
import yfinance as yf
import plotly.express as px
import pandas as pd
import numpy as np

# Try importing pages dynamically
try:
    import pages.home.app
    import pages.finder.app
    import pages.visualization.app
    import pages.database.app
except ModuleNotFoundError as e:
    st.error(f"Module not found: {e.name}")

# Streamlit Page Configuration
st.set_page_config(
    page_title='ETF-Master-2000',
    page_icon=':chart_with_upwards_trend:',
    layout="wide",
    initial_sidebar_state="expanded"
)

class MultiApp:
    def __init__(self):
        self.apps = {
            'home': pages.home.app,
            'finder': pages.finder.app,
            'visualization': pages.visualization.app,
            'database': pages.database.app
        }

    def run(self):
        with st.sidebar:
            app = option_menu(            
                menu_title="Navigation", 
                options=['home', 'finder', 'visualization', 'database'],
                icons=['house-fill', 'search', 'bar-chart', 'table'],
                menu_icon='chat-text-fill',
                default_index=0,
                styles={"container": {"padding": "5!important", "background_color": "white"},
                    "icon": {"color": "#CBD914", "font-size": "28px"},
                    "nav-link": {"color": "#CBD914", "font-size": "20px"},
                    "nav-link:hover": {"color": "black", "font-size": "22px"},
                    "nav-link-selected": {"background-color": "#8F00FF", "font-size": "20px"}
                }
            )

        if app in self.apps:
            self.apps[app].app()  # Call the selected page's app function
        else:
            st.error("Page not found")

if __name__ == "__main__":
    app = MultiApp()
    app.run()
