# import streamlit as st
# import plotly.express as px

# def show_visualizations_page(df):
#     """
#     Display the visualizations page with interactive charts and filters
    
#     Parameters:
#     df (pandas.DataFrame): The dataset to visualize
#     """
#     st.title("📊 Health Commodity Distribution Visualizer")
#     st.markdown("Use the filters below to explore dispensed family planning commodities.")

#     # Create a centered container with reduced padding for all visualizations content
#     col1, content_col, col2 = st.columns([0.1, 0.8, 0.1])
    
#     with content_col:
#         # Tab Filters for County, Sub-County, Facility
#         tab1, tab2, tab3 = st.tabs(["County", "Sub-County", "Facility"])

#         with tab1:
#             selected_county = st.selectbox("Select County", df["county_name"].unique())

#         filtered_df = df[df["county_name"] == selected_county]

#         with tab2:
#             selected_sub_county = st.selectbox("Select Sub-County", filtered_df["sub_county_name"].unique())

#         filtered_df = filtered_df[filtered_df["sub_county_name"] == selected_sub_county]

#         with tab3:
#             selected_facility = st.selectbox("Select Facility", filtered_df["facility_name"].unique())

#         filtered_df = filtered_df[filtered_df["facility_name"] == selected_facility]

#         # Visualizing Dispensed Units Over Time
#         time_series = filtered_df.groupby("period")["value"].sum().reset_index()
#         fig = px.line(
#             time_series, x="period", y="value", markers=True,
#             title=f"Dispensed Units Over Time ({selected_facility})",
#             labels={"value": "Dispensed Units", "period": "Period"}
#         )
#         # Make plotly chart use the full width
#         st.plotly_chart(fig, use_container_width=True)

#         # Commodity Selection - Checkboxes
#         st.subheader("📦 Select Commodities to Compare")
#         # Use columns to display checkboxes more efficiently
#         checkbox_cols = st.columns(3)
#         unique_commodities = filtered_df["dataelement_name"].unique()
#         selected_commodities = []
        
#         for i, commodity in enumerate(unique_commodities):
#             with checkbox_cols[i % 3]:
#                 if st.checkbox(commodity, value=True):
#                     selected_commodities.append(commodity)

#         # Commodity Trend Visualization
#         if selected_commodities:
#             commodity_df = filtered_df[filtered_df["dataelement_name"].isin(selected_commodities)]
#             commodity_trend = commodity_df.groupby(["period", "dataelement_name"])["value"].sum().reset_index()

#             fig = px.line(
#                 commodity_trend, x="period", y="value", color="dataelement_name",
#                 markers=True, title="Trends for Selected Commodities",
#                 labels={"value": "Dispensed Units", "period": "Period"}
#             )
#             # Make plotly chart use the full width
#             st.plotly_chart(fig, use_container_width=True)

#         # Optional raw data display
#         if st.checkbox("Show Raw Data"):
#             display_df = filtered_df.copy()
#             if 'Unnamed: 0' in display_df.columns:
#                 display_df = display_df.drop("Unnamed: 0", axis=1)
#             display_df = display_df.reset_index(drop=True)
#             st.dataframe(display_df.sort_values("period"), use_container_width=True)

import streamlit as st
import plotly.express as px

def show_visualizations_page(df):
    """
    Display the visualizations page with interactive charts and filters
    
    Parameters:
    df (pandas.DataFrame): The dataset to visualize
    """
    # Apply custom header with gradient background
    st.markdown("""
    <div style="background: linear-gradient(to right, #00b09b, #96c93d); padding: 2px; border-radius: 10px; margin-bottom: 5px;">
        <h1 style="color: white; text-align: center;">📊 Health Commodity Distribution Visualizer</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Create a subtitle
    st.markdown("""
    <div style="background-color: white; padding: 2px; border-radius: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); margin-bottom: 5px;">
        <p style="color: #333; text-align: center; font-size: 18px;">Use the filters below to explore dispensed family planning commodities.</p>
    </div>
    """, unsafe_allow_html=True)

    # Create a centered container with reduced padding for all visualizations content
    col1, content_col, col2 = st.columns([0.05, 0.9, 0.05])
    
    with content_col:
        # Create a card-like container for filters
        st.markdown("""
        <div style="background-color: white; padding: 2px; border-radius: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); margin-bottom: 5px;">
        """, unsafe_allow_html=True)
        
        # Tab Filters for County, Sub-County, Facility
        tab1, tab2, tab3 = st.tabs(["County", "Sub-County", "Facility"])

        with tab1:
            selected_county = st.selectbox("Select County", df["county_name"].unique())

        filtered_df = df[df["county_name"] == selected_county]

        with tab2:
            selected_sub_county = st.selectbox("Select Sub-County", filtered_df["sub_county_name"].unique())

        filtered_df = filtered_df[filtered_df["sub_county_name"] == selected_sub_county]

        with tab3:
            selected_facility = st.selectbox("Select Facility", filtered_df["facility_name"].unique())

        filtered_df = filtered_df[filtered_df["facility_name"] == selected_facility]
        
        st.markdown("</div>", unsafe_allow_html=True)  # Close the card container

        # Create a card-like container for the first chart
        st.markdown("""
        <div style="background-color: white; padding: 2px; border-radius: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); margin-bottom: 5px;">
            <h3 style="color: #2c3e50; border-bottom: 2px solid #4CAF50; padding-bottom: 10px;">Dispensed Units Over Time</h3>
        """, unsafe_allow_html=True)
        
        # Visualizing Dispensed Units Over Time
        time_series = filtered_df.groupby("period")["value"].sum().reset_index()
        fig = px.line(
            time_series, x="period", y="value", markers=True,
            title=f"Dispensed Units Over Time ({selected_facility})",
            labels={"value": "Dispensed Units", "period": "Period"}
        )
        
        # Enhance chart styling
        fig.update_layout(
            plot_bgcolor="rgba(255,255,255,0.9)",
            paper_bgcolor="rgba(255,255,255,0)",
            font=dict(color="#2c3e50"),
            title_font=dict(size=20, color="#2c3e50"),
            xaxis=dict(showgrid=True, gridcolor="#eee"),
            yaxis=dict(showgrid=True, gridcolor="#eee"),
            margin=dict(l=20, r=20, t=60, b=20),
        )
        
        # Enhance line style
        fig.update_traces(
            line=dict(width=3, color="#4CAF50"),
            marker=dict(size=8, color="#4CAF50")
        )
        
        # Make plotly chart use the full width
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True)  # Close the card container

        # Create a card-like container for commodity comparison
        st.markdown("""
        <div style="background-color: white; padding: 2px; border-radius: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); margin-bottom: 5px;">
            <h3 style="color: #2c3e50; border-bottom: 2px solid #FFA726; padding-bottom: 10px;">
                <span style="font-size: 24px;">📦</span> Select Commodities to Compare
            </h3>
        """, unsafe_allow_html=True)
        
        # Use columns to display checkboxes more efficiently
        checkbox_cols = st.columns(3)
        unique_commodities = filtered_df["dataelement_name"].unique()
        selected_commodities = []
        
        for i, commodity in enumerate(unique_commodities):
            with checkbox_cols[i % 3]:
                # Custom styled checkbox container
                if st.checkbox(commodity, value=True, key=f"viz_checkbox_{commodity}"):
                    selected_commodities.append(commodity)

        # Commodity Trend Visualization
        if selected_commodities:
            st.markdown("""
            <div style="background-color: #f5f5f5; padding: 2px; border-radius: 8px; margin: 5px 0;">
                <h4 style="color: #2c3e50; margin-top: 0;">Trends for Selected Commodities</h4>
            </div>
            """, unsafe_allow_html=True)
            
            commodity_df = filtered_df[filtered_df["dataelement_name"].isin(selected_commodities)]
            commodity_trend = commodity_df.groupby(["period", "dataelement_name"])["value"].sum().reset_index()

            fig = px.line(
                commodity_trend, x="period", y="value", color="dataelement_name",
                markers=True,
                labels={"value": "Dispensed Units", "period": "Period", "dataelement_name": "Commodity"}
            )
            
            # Enhance chart styling
            fig.update_layout(
                plot_bgcolor="rgba(255,255,255,0.9)",
                paper_bgcolor="rgba(255,255,255,0)",
                font=dict(color="#2c3e50"),
                xaxis=dict(showgrid=True, gridcolor="#eee"),
                yaxis=dict(showgrid=True, gridcolor="#eee"),
                legend_title_font=dict(size=14),
                legend=dict(
                    bgcolor="rgba(255,255,255,0.8)",
                    bordercolor="#dddddd",
                    borderwidth=1,
                    orientation="h"
                ),
                margin=dict(l=20, r=20, t=20, b=20),
            )
            
            # Enhance line style
            fig.update_traces(
                line=dict(width=2.5),
                marker=dict(size=6)
            )
            
            # Make plotly chart use the full width
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.markdown("""
            <div style="background-color: #fff3e0; padding: 2px; border-radius: 8px; margin: 5px 0; border-left: 4px solid #FF9800; text-align: center;">
                <p style="margin: 0;"><span style="font-size: 20px;">⚠️</span> Please select at least one commodity to see trends.</p>
            </div>
            """, unsafe_allow_html=True)

        # Optional raw data display
        show_data = st.checkbox("Show Raw Data", value=False)
        if show_data:
            st.markdown("""
            <div style="background-color: #f5f5f5; padding: 2px; border-radius: 8px; margin: 5px 0;">
                <h4 style="color: #2c3e50; margin-top: 0;">Raw Data</h4>
            </div>
            """, unsafe_allow_html=True)
            
            # Drop the 'Unnamed: 0' column and reset index before displaying
            display_df = filtered_df.copy()
            if 'Unnamed: 0' in display_df.columns:
                display_df = display_df.drop("Unnamed: 0", axis=1)
            display_df = display_df.reset_index(drop=True)
            st.dataframe(display_df.sort_values("period"), use_container_width=True)
            
        st.markdown("</div>", unsafe_allow_html=True)  # Close the card container
        
        # Add footer with info
        st.markdown("""
        <div style="margin-top: 10px; text-align: center; color: #666; font-size: 14px;">
            <p>Try selecting different facilities or commodities to explore the data in more detail.</p>
        </div>
        """, unsafe_allow_html=True)