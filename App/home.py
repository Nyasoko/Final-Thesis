import streamlit as st
from map import render_map

def show_home_page(df):
    """
    Display the home page with map visualization
    
    Parameters:
    df (pandas.DataFrame): The dataset to visualize
    """
    # Apply custom header with gradient background
    st.markdown("""
    <div style="background: linear-gradient(to right, #4b6cb7, #182848); padding: 20px; border-radius: 10px; margin-bottom: 20px;">
        <h1 style="color: white; text-align: center;">🏠 Welcome to the Health Commodity Dashboard</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Display metrics summary
    col1, col2, col3 = st.columns(3)
    with col1:
        display_metric("Total Commodities", 
                      df["dataelement_name"].nunique(),
                      "📦")
        
    with col2:
        display_metric("Counties Covered", 
                      df["county_name"].nunique(),
                      "🗺️")
        
    with col3:
        display_metric("Total Distributed Units", 
                      f"{df['value'].sum():,.0f}",
                      "📈")
    
    # Create card-like container for the description
    st.markdown("""
    <div style="background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); margin-bottom: 20px;">
        <h3 style="color: #2c3e50; border-bottom: 2px solid #4CAF50; padding-bottom: 10px;">Health Commodity Distribution Overview</h3>
        <p style="color: #333; line-height: 1.6;">
            This interactive map visualizes the distribution of family planning commodities across Kenya's counties. 
            The color intensity represents the total number of distributed units, with darker colors indicating higher volumes. 
            Use the filters on the right to focus on specific commodity types and identify geographic patterns in distribution. 
            This data helps health officials, NGOs, and policymakers target resources where they're most needed and monitor 
            the effectiveness of family planning initiatives throughout the country.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create a centered container with reduced padding for the map in a card-like container
    st.markdown("""
    <div style="background-color: white; padding: 5px; border-radius: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
    """, unsafe_allow_html=True)
    
    col1, map_col, col2 = st.columns([0.05, 0.9, 0.05])
    with map_col:
        # Make map use the column width with minimal padding
        render_map(df)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Add footer with info
    st.markdown("""
    <div style="margin-top: 30px; text-align: center; color: #666; font-size: 14px;">
        <p>Data last updated: April 2024 | Dashboard Version 1.0</p>
    </div>
    """, unsafe_allow_html=True)

def display_metric(label, value, icon):
    """
    Display a metric in a visually appealing card
    """
    st.markdown(f"""
    <div style="background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); text-align: center; height: 150px; display: flex; flex-direction: column; justify-content: center; margin-bottom: 20px;">
        <div style="font-size: 40px; margin-bottom: 10px;">{icon}</div>
        <div style="font-size: 28px; font-weight: bold; color: #4CAF50;">{value}</div>
        <div style="font-size: 16px; color: #666;">{label}</div>
    </div>
    """, unsafe_allow_html=True)