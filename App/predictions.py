import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import io
import os
from datetime import datetime
import lightgbm as lgb

# Function to download files from GitHub
def download_github_file(url, save_path):
    if not os.path.exists(save_path):
        response = requests.get(url)
        response.raise_for_status()
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded {save_path}")
    else:
        print(f"File already exists: {save_path}")

# Download necessary model and data files
model_files = {
    "model.txt": "https://github.com/yourusername/repository/raw/main/model.txt",
    "facility_data.csv": "https://github.com/yourusername/repository/raw/main/facility_data.csv",
    "commodities.csv": "https://github.com/yourusername/repository/raw/main/commodities.csv"
}

for filename, url in model_files.items():
    download_github_file(url, f"./data/{filename}")

# Load data
facility_data = pd.read_csv("./data/facility_data.csv")
commodities = pd.read_csv("./data/commodities.csv")
model = lgb.Booster(model_file="./data/model.txt")

# Set up the Streamlit app
st.set_page_config(page_title="Health Commodity Demand Prediction", layout="wide")

# CSS styles
st.markdown("""
<style>
.header-style {
    background: linear-gradient(to right, #4CAF50, #2196F3);
    padding: 1.5% 1%;
    border-radius: 5px;
    color: white;
}
.card {
    padding: 20px;
    border-radius: 5px;
    margin-bottom: 10px;
    background-color: #f9f9f9;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="header-style"><h1 style="text-align: center;">Health Commodity Demand Prediction</h1></div>', unsafe_allow_html=True)

st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("Location Selection")

# Create location filters
col1, col2 = st.columns(2)

with col1:
    # County selection
    counties = sorted(facility_data['County'].unique())
    county = st.selectbox('County', counties)
    
    # Filtered sub-counties based on county
    sub_counties = sorted(facility_data[facility_data['County'] == county]['Sub-County'].unique())
    sub_county = st.selectbox('Sub-County', sub_counties)

with col2:
    # Filtered wards based on county and sub-county
    wards = sorted(facility_data[(facility_data['County'] == county) & 
                               (facility_data['Sub-County'] == sub_county)]['Ward'].unique())
    ward = st.selectbox('Ward', wards)
    
    # Filtered facilities based on county, sub-county, and ward
    facilities = sorted(facility_data[(facility_data['County'] == county) & 
                                   (facility_data['Sub-County'] == sub_county) & 
                                   (facility_data['Ward'] == ward)]['Facility Name'].unique())
    facility = st.selectbox('Facility', facilities)

st.markdown('</div>', unsafe_allow_html=True)

# Time Period Selection section
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("Time Period Selection")

time_col1, time_col2, time_col3 = st.columns(3)
with time_col1:
    month = st.number_input("Month", min_value=1, max_value=12, value=4)
with time_col2:
    year = st.number_input("Year", min_value=2011, max_value=2030, value=2024)
with time_col3:
    # Replace the static quarter display with a selectbox using full quarter names
    quarter_options = ["Quarter 1", "Quarter 2", "Quarter 3", "Quarter 4"]
    # Default to the calculated quarter based on month
    default_quarter_index = (month-1)//3
    quarter = st.selectbox("Quarter", options=quarter_options, index=default_quarter_index)
    # Extract just the number for the model input
    quarter_value = int(quarter.split()[-1])

st.markdown('</div>', unsafe_allow_html=True)

# Commodity Selection
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("Commodity Selection")

commodity = st.selectbox('Select Commodity', sorted(commodities['Commodity Name'].unique()))
commodity_id = commodities[commodities['Commodity Name'] == commodity]['Commodity ID'].values[0]

st.markdown('</div>', unsafe_allow_html=True)

# Generate Prediction button
predict_btn = st.button('Generate Prediction', type='primary', use_container_width=True)

# Placeholder for prediction results
if predict_btn:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Prediction Results")
    
    # Get facility info
    facility_info = facility_data[(facility_data['County'] == county) & 
                                 (facility_data['Sub-County'] == sub_county) & 
                                 (facility_data['Ward'] == ward) & 
                                 (facility_data['Facility Name'] == facility)].iloc[0]
    
    facility_id = facility_info['Facility ID']
    
    # Create features
    input_data = pd.DataFrame([{
        'facility_id': facility_id,
        'commodity_id': commodity_id,
        'year': year,
        'month': month,
        'quarter': quarter_value,  # Use the numeric value extracted from selection
        'is_hospital': 1 if 'hospital' in facility.lower() else 0,
        'is_dispensary': 1 if 'dispensary' in facility.lower() else 0,
        'is_health_center': 1 if 'health center' in facility.lower() else 0,
    }])
    
    # Time features
    input_data['month_sin'] = np.sin(2 * np.pi * input_data['month'] / 12)
    input_data['month_cos'] = np.cos(2 * np.pi * input_data['month'] / 12)
    
    # Make prediction
    prediction = model.predict(input_data)
    predicted_demand = max(0, round(prediction[0]))  # Ensure non-negative
    
    # Display prediction
    st.markdown(f"<h3>Predicted demand for {commodity} at {facility} for {month}/{year} ({quarter}):</h3>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align: center; color: #2196F3;'>{predicted_demand} units</h2>", unsafe_allow_html=True)
    
    # Visualization (mock historical data for example)
    st.subheader("Historical Demand vs Prediction")
    
    # Create sample historical data
    history_months = 12
    historical_data = np.random.randint(max(0, predicted_demand-100), predicted_demand+100, size=history_months)
    months = [(month-i-1) % 12 + 1 for i in range(history_months)]
    months.reverse()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(range(history_months), historical_data, marker='o', linestyle='-', label='Historical Demand')
    ax.axhline(y=predicted_demand, color='r', linestyle='--', label=f'Prediction: {predicted_demand}')
    ax.set_xlabel('Months')
    ax.set_ylabel('Demand')
    ax.set_title(f'Historical and Predicted Demand for {commodity}')
    ax.set_xticks(range(history_months))
    ax.set_xticklabels([f"{m}" for m in months], rotation=45)
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.7)
    
    st.pyplot(fig)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Confidence information
st.markdown("""
<div class="card">
<h3>About the Prediction Model</h3>
<p>This prediction model uses historical consumption data, facility information, and temporal patterns to forecast demand for health commodities. The predictions are generated using a gradient boosting model trained on historical data from various health facilities across multiple counties.</p>
<p>Predictions should be used as guidance and may be affected by factors not captured in the model such as sudden disease outbreaks, supply chain disruptions, or changes in treatment protocols.</p>
</div>
""", unsafe_allow_html=True)
