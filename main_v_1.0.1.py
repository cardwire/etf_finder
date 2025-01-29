import streamlit as st
from packaging import version
import yfinance as yf
import plotly.express as px
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from datetime import timedelta

# Import the option_menu for sidebar navigation
from streamlit_option_menu import option_menu

# Try importing pages with error handling for missing modules
try:
    import pages.home.app
    import pages.finder.app
    import pages.visualization.app
    import pages.database.app
    # import pages.forecast.app  # Uncomment if forecast page is available
except ModuleNotFoundError as e:
    st.error(f"Module not found: {e.name}. Please check if the page file exists in the 'pages' folder.")

# Set page configuration
st.set_page_config(
    page_title='ETF-Master-2000',
    page_icon=':chart_with_upwards_trend:',
    layout="wide",
    initial_sidebar_state="expanded")

# Define MultiApp class for handling navigation
class MultiApp:
    def __init__(self):
        self.apps = {
            'home': pages.home.app,
            'finder': pages.finder.app,
            'visualization': pages.visualization.app,
            'database': pages.database.app,
            # 'forecast': pages.forecast.app  # Uncomment if forecast page is available
        }

    def run(self):
        # Sidebar with menu
        with st.sidebar:
            app = option_menu(
                menu_title="Navigation", 
                options=['home', 'finder', 'visualization', 'database', 'forecast'],
                icons=['house-fill', 'search', 'bar-chart', 'table', 'calendar'],
                menu_icon='chat-text-fill',
                default_index=0,
                styles={"container": {"padding": "5!important", "background_color": "white"},
                        "icon": {"color": "#CBD914", "font-size": "28px"},
                        "nav-link": {"color": "#CBD914", "font-size": "20px"},
                        "nav-link:hover": {"color": "black", "font-size": "22px"},
                        "nav-link-selected": {"background-color": "#8F00FF", "font-size": "20px"}
                }
            )
        # Run the selected app
        if app in self.apps:
            self.apps[app].app()  # Call the app function of the selected page
        else:
            st.error("Page not found")

# Initialize the app
if __name__ == "__main__":
    app = MultiApp()
    app.run()  # Run the app
