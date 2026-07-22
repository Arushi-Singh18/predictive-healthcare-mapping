import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

st.set_page_config(page_title="Predictive Health Mapping", page_icon="🏥", layout="wide")

# Custom CSS to make the dashboard look premium
st.markdown("""
    <style>
    .main {background-color: #f8fafc;}
    .stAlert {border-radius: 10px;}
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-left: 5px solid #06b6d4;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_mock_data():
    """Generates mock data for clinics around Lucknow for prototype demonstration."""
    # Central Lucknow coordinates: 26.8467° N, 80.9462° E
    np.random.seed(42)
    
    # Generate 5 random clinic locations around Lucknow
    lats = np.random.uniform(26.80, 26.90, 5)
    lons = np.random.uniform(80.90, 81.00, 5)
    
    clinics = pd.DataFrame({
        'Clinic Name': ['Sector 4 Outpost', 'Gomti Nagar Main', 'Aliganj Hub', 'Hazratganj Center', 'Chowk ER'],
        'lat': lats,
        'lon': lons,
        'Vulnerability Index': np.random.uniform(0.4, 0.9, 5), # Sociological layer
        'Asthma_Inhaler_Stock': np.random.randint(10, 500, 5),
        'Dengue_Kits_Stock': np.random.randint(5, 200, 5)
    })
    return clinics

clinics_df = load_mock_data()

st.title("🏥 Predictive Healthcare Resource Mapping")
st.markdown("**Transdisciplinary Forecasting Dashboard - Lucknow District**")

st.sidebar.header("Control Panel")
selected_threat = st.sidebar.selectbox(
    "Select Predictive Threat Model:",
    ["Air Quality (Respiratory)", "Monsoon/Humidity (Vector-borne)"]
)
forecast_window = st.sidebar.slider("Forecast Window (Days)", 7, 90, 14)

st.sidebar.markdown("---")
st.sidebar.info("Model Status: Active\n\nData Sources: OpenWeather API, Local SDOH Census")

st.subheader("Live District Overview")

col1, col2 = st.columns([2, 1])

with col1:
    # Display the map using Streamlit's built-in map function
    st.map(clinics_df, zoom=11, use_container_width=True)

with col2:
    st.subheader("Automated Logistics Alerts")
    
    if selected_threat == "Air Quality (Respiratory)":
        st.error("🚨 **CRITICAL ALERT: Sector 4 Outpost**\n\n"
                 "**Predictive Trigger:** PM2.5 levels forecasted to spike > 150 AQI in 72 hours.\n\n"
                 "**Sociological Risk:** High Density, Low Income.\n\n"
                 "**Forecast:** 60% surge in pediatric asthma admissions.")
        
        st.markdown("<div class='metric-card'>"
                    "<h4>Recommended Action</h4>"
                    "<p>Lateral transfer of <b>200 Pediatric Inhalers</b> from <i>Gomti Nagar Main</i> to <i>Sector 4 Outpost</i>.</p>"
                    "</div>", unsafe_allow_html=True)
        
        if st.button("Approve Transfer", type="primary"):
            st.success("Transfer order dispatched to logistics network.")
            
    else:
        st.warning("⚠️ **WARNING: Chowk ER**\n\n"
                 "**Predictive Trigger:** Stagnant water accumulation post-monsoon detected via satellite & humidity metrics.\n\n"
                 "**Forecast:** 45% probability of Dengue cluster in 14 days.")
        
        st.markdown("<div class='metric-card'>"
                    "<h4>Recommended Action</h4>"
                    "<p>Deploy <b>150 Dengue Rapid Test Kits</b> from Central Warehouse to <i>Chowk ER</i>.</p>"
                    "</div>", unsafe_allow_html=True)
        
        if st.button("Approve Dispatch", type="primary"):
            st.success("Dispatch order routed to Central Warehouse.")

st.markdown("---")
st.subheader("Predictive Demand Curve")

# Generate fake time-series data for the chart
dates = [datetime.today() + timedelta(days=i) for i in range(forecast_window)]
baseline_demand = np.random.randint(20, 30, size=forecast_window)

# Add a spike in the middle to simulate a crisis
crisis_peak = forecast_window // 2
spike = np.exp(-((np.arange(forecast_window) - crisis_peak) ** 2) / 5) * 50
predicted_demand = baseline_demand + spike

chart_data = pd.DataFrame({
    'Date': dates,
    'Baseline Demand (Historical)': baseline_demand,
    'Predicted Demand (AI Forecast)': predicted_demand
}).set_index('Date')

st.line_chart(chart_data
