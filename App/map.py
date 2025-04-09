import streamlit as st
import folium
import json
import branca.colormap as cm
import pandas as pd
import streamlit.components.v1 as components

def render_map(df):
    """
    Renders a choropleth map of Kenya counties with health commodity distribution data
    """
    
    # Create a layout with map on the left and checkboxes on the right
    col1, col2 = st.columns([0.8, 0.2])
    
    # Get unique commodity types
    unique_commodities = sorted(df["dataelement_name"].unique())
    
    # In the right column, create vertical checkboxes for commodity types
    with col2:
        st.write("**Filter by Commodity:**")
        
        # Create a dictionary to hold checkbox states
        selected_commodities = {}
        for commodity in unique_commodities:
            selected_commodities[commodity] = st.checkbox(
                commodity, 
                value=True,
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
            # Load GeoJSON file
            with open("Data/kenya.geojson", "r", encoding="utf-8") as f:
                kenya_geo = json.load(f)

            # Aggregate data by county
            data = filtered_df.groupby("county_name")["value"].sum().reset_index()
            data["county"] = data["county_name"].str.replace(" County", "", case=False).str.upper()
           
            # County name mappings
            county_mapping = {
                "ELEGEYO-MARAKWET": "ELGEYO MARAKWET",
                "MURANG'A": "MURANGA",
                "THARAKA - NITHI": "THARAKA NITHI"
            }
           
            value_dict = dict(zip(data["county"], data["value"]))
           
            min_value = data["value"].min() if not data.empty else 0
            max_value = data["value"].max() if not data.empty else 100
           
            # Create the base map with explicit tile provider
            m = folium.Map(
                location=[0.0236, 37.9062], 
                zoom_start=6, 
                tiles="CartoDB positron"
            )
            
            # Create color scale
            colors = ['#ffffb2', '#fecc5c', '#fd8d3c', '#f03b20', '#bd0026']
            color_scale = cm.LinearColormap(colors, vmin=min_value, vmax=max_value)
           
            # Style functions
            def style_function(feature):
                county_name = feature["properties"].get("COUNTY_NAM", "")
                if county_name is None:
                    county_name = ""
                county_name = county_name.upper()
                if county_name in county_mapping:
                    county_name = county_mapping[county_name]
                value = value_dict.get(county_name, 0)
                return {
                    'fillColor': color_scale(value),
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
            
            # Add GeoJSON layer
            tooltip = folium.GeoJsonTooltip(
                fields=["COUNTY_NAM"],
                aliases=["County:"],
                localize=True,
                sticky=True,
                style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")
            )
            
            folium.GeoJson(
                kenya_geo,
                style_function=style_function,
                highlight_function=highlight_function,
                tooltip=tooltip,
                name="Kenya Counties"
            ).add_to(m)
           
            # Add color scale
            color_scale.caption = 'Total Units Dispensed'
            m.add_child(color_scale)
            
            # Get the HTML representation of the map
            map_html = m._repr_html_()
            
            # Display the map using components.html instead of st_folium
            components.html(map_html, height=600)
            
        except FileNotFoundError:
            st.error("❌ Error: Kenya GeoJSON file not found. Please make sure 'kenya.geojson' is in the Data directory.")
        except Exception as e:
            st.error(f"❌ Error rendering map: {str(e)}")
            st.info("Try refreshing the page or check console for more details.")
