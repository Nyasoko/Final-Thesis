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
        <h1 style="color: white; text-align: center;"> Welcome to the Health Commodity Dashboard</h1>
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
    
    # Map section with explicit height and styling
    st.markdown("<h3 style='text-align: center; margin-bottom: 15px;'>Geographic Distribution Map</h3>", unsafe_allow_html=True)
    
    # Create a container with fixed height for the map
    map_container = st.container()
    with map_container:
        # Apply CSS to ensure the map is visible with appropriate dimensions
        st.markdown("""
        <style>
        .map-container {
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            padding: 10px;
            margin-bottom: 20px;
            height: 600px; /* Explicit height for map */
        }
        </style>
        <div class="map-container">
        """, unsafe_allow_html=True)
        
        # Debug statement before map rendering
        st.write("Loading map visualization...")
        
        # Render the map
        render_map(df)
        
        # Debug statement after map rendering
        st.write("Map should be visible above. If not, check for errors in the console.")
        
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
