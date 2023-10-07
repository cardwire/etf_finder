import numpy as np
import pandas as pd 
import streamlit as st
import streamlit_elements

from streamlit_option_menu import option_menu

def app():
    
    # URL of the image on GitHub
    image_url = "https://raw.githubusercontent.com/cardwire/da_capstone_group3/main/Team3_App/data/g4231.png"

    # Display the image in your Streamlit app
    st.image(image_url, caption='Your Image', use_column_width=True)
    
    st.markdown('### __Invest in the in the best - Apply your personal requirements for sustainable assets__ ')

    st.divider()
    
    st.markdown("### - Explore our Database of over 3000 ETFs and find the ones that fit your needs.")
           
    st.divider()       
                
    st.markdown("### - You don't want to read another giant table? Explor our Database in our 3D ETF-Landscape")
    
    st.divider() 
                
    st.markdown(" ### - Get statistical features, KPIs and statistical reports for all ETFs that state such.")
    
    st.divider()
                   
    st.markdown(" ### - Find the ETFs that fit you best using our ETF-finder module and customize performance and sustainability.")
    
    st.divider()
                   
    st.markdown(" ### - Use a variety of forecasting methods to on your personal top5 ETFs, to help you with your final choice.")
    
    st.divider()
    
    

        
