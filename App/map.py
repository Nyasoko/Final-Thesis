import streamlit as st
import folium
import json
import branca.colormap as cm
from streamlit_folium import st_folium
import pandas as pd

def render_map(df):
    """
    Renders a choropleth map of Kenya counties with health commodity distribution data
    using Folium, with commodity type filters on the right side.
    
    Parameters:
    df (pandas.DataFrame): Dataset containing county-level distribution data
    """
    
    # Create a layout with map on the left and checkboxes on the right
    col1, col2 = st.columns([0.8, 0.2])
    
    # Get unique commodity types
    unique_commodities = sorted(df["dataelement_name"].unique())
    
    # In the right column, create vertical checkboxes for commodity types
    with col2:
        st.write("**Filter by Commodity:**")
        
        # Create a dictionary to hold checkbox states, defaulting to all True
        selected_commodities = {}
        for commodity in unique_commodities:
            selected_commodities[commodity] = st.checkbox(
                commodity, 
                value=True,  # Default all selected
                key=f"map_commodity_{commodity}"
            )
        
        # Get list of selected commodities
        commodities_to_show = [c for c, selected in selected_commodities.items() if selected]
        
        # Show selection summary
        if len(commodities_to_show) == len(unique_commodities):
            st.info("Showing all commodities")
        else:
            st.info(f"Showing {len(commodities_to_show)} of {len(unique_commodities)} commodities")
    
    # Filter data based on selected commodities
    filtered_df = df[df["dataelement_name"].isin(commodities_to_show)]
    
    # In the left column, render the map
    with col1:
        try:
            with open("C:/Users/Admin/Documents/CT/school/PF/Data/kenya.geojson", "r", encoding="utf-8") as f:
                kenya_geo = json.load(f)
           
            # Aggregate data by county based on filtered commodities
            data = filtered_df.groupby("county_name")["value"].sum().reset_index()
           
            data["county"] = data["county_name"].str.replace(" County", "", case=False).str.upper()
           
            # Add county name mappings for inconsistencies between dataset and GeoJSON
            county_mapping = {
                "ELEGEYO-MARAKWET": "ELGEYO MARAKWET",
                "MURANG'A": "MURANGA",
                "THARAKA - NITHI": "THARAKA NITHI"
            }
           
            value_dict = dict(zip(data["county"], data["value"]))
           
            min_value = data["value"].min() if not data.empty else 0
            max_value = data["value"].max() if not data.empty else 100
           
            colors = ['#ffffb2', '#fecc5c', '#fd8d3c', '#f03b20', '#bd0026']
            color_scale = cm.LinearColormap(colors, vmin=min_value, vmax=max_value)
           
            m = folium.Map(location=[0.0236, 37.9062], zoom_start=6, tiles="cartodbpositron")
           
            def style_function(feature):
                county_name = feature["properties"].get("COUNTY_NAM", "")
               
                if county_name is None:
                    county_name = ""
                   
                county_name = county_name.upper()
                if county_name in county_mapping:
                    county_name = county_mapping[county_name]
               
                value = value_dict.get(county_name, 0)
               
                color = color_scale(value)
               
                return {
                    'fillColor': color,
                    'color': 'black',
                    'weight': 1,
                    'fillOpacity': 0.7
                }
           
            def highlight_function(feature):
                return {
                    'weight': 3,
                    'color': '#666',
                    'dashArray': '',
                    'fillOpacity': 0.9
                }
           
            def tooltip_function(feature):
                county_name = feature["properties"].get("COUNTY_NAM", "Unknown")
               
                if county_name is None:
                    county_name = "Unknown"
                    county_name_upper = ""
                else:
                    county_name_upper = county_name.upper()
               
                if county_name_upper in county_mapping:
                    county_name_upper = county_mapping[county_name_upper]
               
                value = value_dict.get(county_name_upper, 0)
               
                return f"{county_name}: {value:,.0f}"
           
            folium.GeoJson(
                kenya_geo,
                style_function=style_function,
                highlight_function=highlight_function,
                tooltip=folium.GeoJsonTooltip(
                    fields=["COUNTY_NAM"],
                    aliases=["County:"],
                    localize=True,
                    sticky=True,
                )
            ).add_to(m)
           
            color_scale.caption = 'Total Units Dispensed'
            m.add_child(color_scale)
           
            # Display the map using streamlit-folium
            st_folium(m, width=700, height=600)
            
        except FileNotFoundError:
            st.error("❌ Error: Kenya GeoJSON file not found. Please make sure 'kenya.geojson' is in the same directory as the application.")
            st.info("📝 Note: You need to place the Kenya counties GeoJSON file in the project directory. The file should be named 'kenya.geojson'.")