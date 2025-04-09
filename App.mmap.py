import streamlit as st
import folium
import json
import branca.colormap as cm
from streamlit_folium import st_folium
import pandas as pd

def render_map(df):
    st.subheader("🗺️ Kenya County Choropleth Map")

    with open("kenya.geojson", "r", encoding="utf-8") as f:
        kenya_geo = json.load(f)
    
    data = df.groupby("county_name")["value"].sum().reset_index()
    
    data["county"] = data["county_name"].str.replace(" County", "", case=False).str.upper()
    
    county_mapping = {
        "ELEGEYO-MARAKWET": "ELGEYO MARAKWET",
        "MURANG'A": "MURANGA",
        "THARAKA - NITHI": "THARAKA NITHI"
    }
    
    value_dict = dict(zip(data["county"], data["value"]))
    
    min_value = data["value"].min()
    max_value = data["value"].max()
    
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
    
    color_scale.caption = 'Value'
    m.add_child(color_scale)
    

    geojson_counties = []
    for f in kenya_geo["features"]:
        county_name = f["properties"].get("COUNTY_NAM")
        if county_name is not None:
            geojson_counties.append(county_name.upper())
        else:
            geojson_counties.append("")
    
    
    st_folium(m, width=800, height=600)
