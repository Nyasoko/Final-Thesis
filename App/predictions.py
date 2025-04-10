import pickle
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import base64
from pathlib import Path

# Safe import of LightGBM with fallback
try:
    import lightgbm as lgb
    LIGHTGBM_AVAILABLE = True
except ImportError:
    LIGHTGBM_AVAILABLE = False
    st.warning("LightGBM not available. Some functionality may be limited.")

# Path to your model file
MODEL_PATH = Path("./data/your_model.pkl")  # Update this path to your actual model location

def download_file(data, filename, display_text=None):
    """
    Generate a download link for the provided data
    
    Parameters:
    -----------
    data : bytes or string
        The data to be downloaded
    filename : str
        Name of the file to be downloaded
    display_text : str, optional
        Text to display on the download button
    """
    if display_text is None:
        display_text = f"Download {filename}"
    
    # Convert data to bytes if it's not already
    if isinstance(data, str):
        data = data.encode()
    
    b64 = base64.b64encode(data).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="{filename}">{display_text}</a>'
    return st.markdown(href, unsafe_allow_html=True)

def load_model():
    """Load the pre-trained model safely"""
    try:
        with open(MODEL_PATH, "rb") as f:
            model = pickle.load(f)
        return model
    except FileNotFoundError:
        st.error(f"Model file not found at {MODEL_PATH}")
        return None
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None

def make_prediction(model, input_data):
    """Make predictions using the loaded model"""
    if model is None:
        return None
    
    try:
        # Convert input data to the format expected by your model
        # This might need adjustment based on your specific model
        prediction = model.predict(input_data)
        return prediction
    except Exception as e:
        st.error(f"Error making prediction: {str(e)}")
        return None

def generate_feature_importance(model, feature_names):
    """Generate feature importance if model supports it"""
    try:
        if hasattr(model, 'feature_importances_'):
            importances = model.feature_importances_
            indices = np.argsort(importances)[::-1]
            
            # Create a DataFrame for feature importance
            importance_df = pd.DataFrame({
                'Feature': [feature_names[i] for i in indices],
                'Importance': importances[indices]
            })
            return importance_df
        else:
            return None
    except Exception as e:
        st.warning(f"Could not calculate feature importance: {str(e)}")
        return None

def export_prediction_results(input_data, prediction, format='csv'):
    """Export prediction results to downloadable format"""
    # Create a copy of input data
    result = input_data.copy()
    
    # Add prediction to the dataframe
    result['prediction'] = prediction
    
    if format.lower() == 'csv':
        return result.to_csv(index=False).encode('utf-8')
    elif format.lower() == 'json':
        return result.to_json(orient='records').encode('utf-8')
    else:
        return result.to_csv(index=False).encode('utf-8')

def show_predictions_page():
    """Display the predictions page in the Streamlit app"""
    st.title("Model Predictions")
    
    # Load model
    model = load_model()
    if model is None:
        st.stop()
    
    # Create input form
    st.subheader("Input Parameters")
    
    # Replace these with your actual model features
    feature1 = st.slider("Feature 1", 0.0, 10.0, 5.0)
    feature2 = st.slider("Feature 2", 0.0, 100.0, 50.0)
    feature3 = st.selectbox("Feature 3", ["Option A", "Option B", "Option C"])
    
    # Convert categorical features if needed
    if feature3 == "Option A":
        feature3_encoded = 0
    elif feature3 == "Option B":
        feature3_encoded = 1
    else:
        feature3_encoded = 2
    
    # Create input data frame
    input_data = pd.DataFrame({
        'feature1': [feature1],
        'feature2': [feature2],
        'feature3': [feature3_encoded]
    })
    
    # Make prediction button
    if st.button("Predict"):
        prediction = make_prediction(model, input_data)
        
        if prediction is not None:
            st.success(f"Prediction: {prediction[0]:.4f}")
            
            # Optional: Visualize the prediction
            st.subheader("Prediction Visualization")
            fig, ax = plt.subplots()
            ax.bar(["Prediction"], prediction)
            st.pyplot(fig)
            
            # Generate feature importance
            feature_names = input_data.columns.tolist()
            importance_df = generate_feature_importance(model, feature_names)
            
            if importance_df is not None:
                st.subheader("Feature Importance")
                st.dataframe(importance_df)
                
                # Visualize feature importance
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.barh(importance_df['Feature'], importance_df['Importance'])
                ax.set_xlabel('Importance')
                ax.set_title('Feature Importance')
                st.pyplot(fig)
            
            # Export options
            st.subheader("Export Results")
            export_format = st.radio("Select export format:", ("CSV", "JSON"))
            
            export_data = export_prediction_results(input_data, prediction, export_format)
            download_file(
                export_data, 
                f"prediction_results.{export_format.lower()}", 
                f"Download results as {export_format}"
            )

# This allows testing this file directly
if __name__ == "__main__":
    show_predictions_page()
