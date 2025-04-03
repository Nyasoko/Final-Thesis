# 📊 FP_Data

A data-driven Streamlit web app focused on forecasting Family Planning (FP) commodity needs across Kenya using machine learning and geospatial visualizations.

---

## 📁 Project Structure

```text
FP_Data/
├── App/
│   ├── __pycache__/
│   ├── explainable_ai.py
│   ├── home.py
│   ├── main.py
│   ├── map.py
│   ├── predictions.py
│   ├── styles.css
│   ├── utils.py
│   └── visualizations.py
├── Data/
│   ├── historical_data.csv
│   └── kenya.geojson
├── Models/
│   ├── best_gb_model.pkl
│   └── encoder.pkl
├── venv/
├── .gitattributes
├── .gitignore
├── README.md
└── requirements.txt
```

## Setup Instructions

### Virtual Environment Setup

1. **Create Virtual Environment**
    ```bash
    # For Windows
    python -m venv venv

    # For macOS/Linux
    python3 -m venv venv
    ```

2. **Activate Virtual Environment**
    ```bash
    # For Windows
    venv\Scripts\activate

    # For macOS/Linux
    source venv/bin/activate
    ```

3. **Install Dependencies**

        pip install -r requirements.txt

4. **🚀 Run the App**

        streamlit run App/main.py


