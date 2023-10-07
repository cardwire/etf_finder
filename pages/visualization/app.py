# pages/visualization/app.py
import streamlit as st
import pandas as pd
import plotly.express as px


# load data
df = pd.read_csv('app_df1.csv')



def app():
    st.title("ETF-Visualizer")
    
    st.markdown("### __You don't want to see just another table or barchart?__ ")
    
    
    st.markdown("## Explore our entire database with our 3D-interactive ETF-map")

    st.divider()
    
    #Define color scales for different features
    color_scales = {
    "dividend_yield_qtl": "Plot3",
    "esg_rating": "Prism",
    "quality_score_qtl": "PiYG",
    "carbon_intensity_qtl": "Bold",
    "aum_qtl": "Viridis",
    "grade": "Set2",
    "investment_strategy": "Plotly",
    "asset_class": "Dark2",
    "asset_region": "Viridis",
    "subsegment": "light24",
    }

    # log transform aum for better plotting
    #df.aum = np.log(df.aum_cat)
    #color_scales.aum_cat = color_scales.aum_cat

    # Streamlit UI
    st.markdown("### Each dot on the map represents a specific ETF. You can get all information hovering over the datapoints")
    
    
    # Instructions
    st.write("""The 3D-map was created using an state of the art unsupervised machine learning classification technique named UMAP*,
             as consequence ETFs which share a lot of similar features are layouted near to each other. So if you are looking at an
             interesting ETF, you will find the most similar alternatives in the direct neighbourhood.""")
    
    st.divider()

         # Dropdown for selecting color feature
    selected_feature = st.selectbox("Select a feature:", list(color_scales.keys()))
    st.write("You selected:", selected_feature)

    # Scatter plot
# Create a 3D scatter plot
    fig = px.scatter_3d(df,
    x='UMAP1', y='UMAP2', z='UMAP3',
    opacity=0.7,
    color=selected_feature,
    color_continuous_scale=color_scales[selected_feature],
    hover_data=['ticker', 'esg_rating', 'dividend_yield']
)

# Update the marker size for the data points
    fig.update_traces(marker=dict(size=2))

# Update the 3D scene to thicken the gridlines
    fig.update_scenes(
    xaxis=dict(gridwidth=2, gridcolor='gray'),  # Adjust gridline thickness and color for the x-axis
    yaxis=dict(gridwidth=2, gridcolor='gray'),  # Adjust gridline thickness and color for the y-axis
    zaxis=dict(gridwidth=2, gridcolor='gray'),  # Adjust gridline thickness and color for the z-axis
    aspectmode="cube"  # Make sure the aspect ratio is consistent for all axes
)

# Set the initial camera position
    fig.update_layout(
    scene_camera=dict(eye=dict(x=1.5, y=1.5, z=1.5))
)

# Set the layout size to 1200x1200
    fig.update_layout(
    width=1200,
    height=1200
)

# Render the Plotly figure in Streamlit
    st.plotly_chart(fig)
