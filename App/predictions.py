import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle
import os
from pathlib import Path

def download_file(data, filename, file_format="csv"):
    """
    Create a download button for exporting data
    
    Args:
        data: DataFrame to be downloaded
        filename: Name for the downloaded file
        file_format: Format for download (csv or json)
    """
    if file_format.lower() == "csv":
        data_str = data.to_csv(index=False)
        mime = "text/csv"
        file_ext = "csv"
    else:
        data_str = data.to_json(orient="records")
        mime = "application/json"
        file_ext = "json"
    
    st.download_button(
        label=f"Download {file_format.upper()}",
        data=data_str,
        file_name=f"{filename}.{file_ext}",
        mime=mime
    )

def load_model():
    """Load the trained model from file"""
    model_path = Path("data/your_model.pkl")
    
    if not model_path.exists():
        st.error(f"Model file not found at {model_path}. Please train a model first.")
        return None
        
    try:
        with open(model_path, "rb") as f:
            model = pickle.load(f)
        return model
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None

def make_prediction(model, input_data):
    """Make a prediction using the loaded model"""
    try:
        prediction = model.predict(input_data)
        return prediction
    except Exception as e:
        st.error(f"Prediction error: {str(e)}")
        return None

def generate_feature_importance(model, feature_names):
    """Generate feature importance DataFrame"""
    try:
        # Check if model has feature_importances_ attribute
        if hasattr(model, 'feature_importances_'):
            importance = model.feature_importances_
            # Create DataFrame of features and their importance
            importance_df = pd.DataFrame({
                'Feature': feature_names,
                'Importance': importance
            })
            return importance_df.sort_values('Importance', ascending=False)
        else:
            return None
    except Exception as e:
        st.error(f"Error generating feature importance: {str(e)}")
        return None

def show_predictions_page(df):
    """Display the predictions page in the Streamlit app"""
    st.title("Model Predictions")
    
    # Load model
    model = load_model()
    if model is None:
        st.stop()
    
    # Display dataframe info
    st.subheader("Dataset Overview")
    st.write(f"Dataset shape: {df.shape[0]} rows, {df.shape[1]} columns")
    st.dataframe(df.head())
    
    # Create input form with relevant features
    st.subheader("Input Parameters")
    
    county = st.selectbox("County", sorted(df['county_name'].unique()))
    
    # Filter subsequent dropdowns based on previous selections
    sub_counties = df[df['county_name']==county]['sub_county_name'].unique()
    sub_county = st.selectbox("Sub County", sorted(sub_counties))
    
    wards = df[(df['county_name']==county) & 
              (df['sub_county_name']==sub_county)]['ward_name'].unique()
    ward = st.selectbox("Ward", sorted(wards))
    
    facilities = df[(df['county_name']==county) & 
                   (df['sub_county_name']==sub_county) & 
                   (df['ward_name']==ward)]['facility_name'].unique()
    facility = st.selectbox("Health Facility", sorted(facilities))
    
    dataelement = st.selectbox("DMPA Type", sorted(df['dataelement_name'].unique()))
    year = st.selectbox("Year", sorted(df['year'].unique()))
    month = st.slider("Month", 1, 12, 1)
    
    # Create input data frame
    input_data = pd.DataFrame({
        'county_name': [county],
        'sub_county_name': [sub_county],
        'ward_name': [ward],
        'facility_name': [facility],
        'dataelement_name': [dataelement],
        'month': [month],
        'year': [year]
    })
    
    # One-hot encode the input data (must match the format used during training)
    # Get all columns from the training data
    training_columns = model.feature_names_in_
    
    # Create a DataFrame with zeros for all training columns
    input_encoded = pd.DataFrame(0, index=[0], columns=training_columns)
    
    # Set the appropriate columns to 1 based on the input data
    for feature in input_data.columns:
        feature_value = input_data[feature].iloc[0]
        feature_col = f"{feature}_{feature_value}"
        if feature_col in training_columns:
            input_encoded[feature_col] = 1
        elif feature in ['month', 'year']:  # Numeric features
            if feature in training_columns:
                input_encoded[feature] = input_data[feature].iloc[0]
    
    # Make prediction button
    if st.button("Predict"):
        prediction = make_prediction(model, input_encoded)
        
        if prediction is not None:
            st.success(f"Predicted DMPA Value: {prediction[0]:.2f}")
            
            # Optional: Visualize the prediction
            st.subheader("Prediction Visualization")
            fig, ax = plt.subplots()
            ax.bar(["Predicted Value"], prediction)
            ax.set_ylabel("DMPA Value")
            st.pyplot(fig)
            
            # Show historical data for context
            historical_data = df[
                (df['county_name'] == county) &
                (df['sub_county_name'] == sub_county) &
                (df['ward_name'] == ward) &
                (df['facility_name'] == facility) &
                (df['dataelement_name'] == dataelement)
            ].sort_values(by=['year', 'month'])
            
            if not historical_data.empty:
                st.subheader("Historical Data")
                st.dataframe(historical_data)
                
                # Plot historical trend
                if len(historical_data) > 1:
                    fig, ax = plt.subplots(figsize=(10, 6))
                    historical_data['date'] = pd.to_datetime(historical_data[['year', 'month']].assign(day=1))
                    ax.plot(historical_data['date'], historical_data['value'], marker='o', linestyle='-')
                    ax.set_title(f"Historical DMPA Values for {facility}")
                    ax.set_xlabel("Date")
                    ax.set_ylabel("Value")
                    plt.xticks(rotation=45)
                    st.pyplot(fig)
            
            # Generate feature importance
            feature_names = input_encoded.columns.tolist()
            importance_df = generate_feature_importance(model, feature_names)
            
            if importance_df is not None:
                st.subheader("Feature Importance")
                st.dataframe(importance_df.head(10))  # Show top 10 features
                
                # Visualize top 10 feature importance
                fig, ax = plt.subplots(figsize=(10, 6))
                importance_df.head(10).plot.barh(x='Feature', y='Importance', ax=ax)
                ax.set_xlabel('Importance')
                ax.set_title('Top 10 Feature Importance')
                st.pyplot(fig)
            
            # Export options
            st.subheader("Export Results")
            export_format = st.radio("Select export format:", ("CSV", "JSON"))
            
            if st.button("Export"):
                result_df = pd.DataFrame({
                    'county': [county],
                    'sub_county': [sub_county],
                    'ward': [ward],
                    'facility': [facility],
                    'dataelement': [dataelement],
                    'month': [month],
                    'year': [year],
                    'predicted_value': [prediction[0]]
                })
                
                # Use the download_file function
                download_file(result_df, "prediction_results", export_format.lower())
