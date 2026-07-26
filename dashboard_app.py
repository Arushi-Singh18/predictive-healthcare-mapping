import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

st.set_page_config(page_title="FrostFit & AI Resource Mapping", page_icon="🏥", layout="wide")

# Custom CSS for a premium, software-engineer level UI
st.markdown("""
    <style>
    .main {background-color: #000000;}
    .alert-box {
        padding: 20px;
        border-radius: 10px;
        background-color: #334155;
        border-left: 6px solid #ef4444;
        margin-bottom: 20px;
    }
    .action-box {
        padding: 20px;
        border-radius: 10px;
        background-color: #334155;
        border-left: 6px solid #22c55e;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_clinic_data():
    """Mock GIS data for clinics around Lucknow"""
    return pd.DataFrame({
        'Clinic': ['Gomti Nagar Main', 'Chowk ER', 'Aliganj Outpost', 'Hazratganj Center', 'Indira Nagar Hub'],
        'lat': [26.8530, 26.8680, 26.8850, 26.8500, 26.8750],
        'lon': [80.9900, 80.9120, 80.9430, 80.9400, 80.9960],
        'Vulnerability_Index': [0.3, 0.9, 0.6, 0.4, 0.5], # 0-1 scale based on Sociology/SDOH
        'Asthma_Inhalers': [300, 12, 150, 200, 180],
        'Dengue_Kits': [150, 5, 80, 120, 90]
    })

clinics_df = load_clinic_data()

st.sidebar.title("⚙️ System Control")
st.sidebar.markdown("Target Region: **Lucknow, UP**")

threat_model = st.sidebar.radio(
    "Select AI Predictive Model:",
    ["Air Quality Surge (Respiratory)", "Post-Monsoon (Vector-Borne)"]
)

forecast_days = st.sidebar.slider("Forecast Window (Days):", 7, 30, 14)

st.sidebar.markdown("---")
st.sidebar.success("✅ System Online\n\nData Streams: Active")

st.title("🏥 Transdisciplinary Healthcare Resource Mapping")
st.markdown("Proactive Supply Chain Optimization Dashboard")

col1, col2, col3 = st.columns(3)
col1.metric("Current Lucknow AQI", "165 (Unhealthy)", "+15 since yesterday")
col2.metric("Current Humidity", "78%", "+5%")
col3.metric("System Status", "Predictive Mode", "Running ARIMA/LSTM")

st.markdown("---")

map_col, alert_col = st.columns([2, 1.2])

with map_col:
    st.subheader("Live District Vulnerability Map")
    # Streamlit's native map tool automatically reads 'lat' and 'lon' columns
    st.map(clinics_df, zoom=11, use_container_width=True)

with alert_col:
    st.subheader("Automated AI Alerts")
    
    if threat_model == "Air Quality Surge (Respiratory)":
        st.markdown("""
        <div class="alert-box">
            <h4 style="color: #b91c1c; margin-top:0;">🚨 CRITICAL: Chowk ER</h4>
            <p><b>Sociological Risk:</b> High Density, Poor Ventilation.</p>
            <p><b>Epidemiological Trigger:</b> AQI forecasted to exceed 300 in 48 hours.</p>
            <p><b>Inventory:</b> Only 12 Inhalers remaining (Stockout imminent).</p>
        </div>
        <div class="action-box">
            <h4 style="color: #15803d; margin-top:0;">⚡ Recommended Logistics Action</h4>
            <p>Dynamic Transfer: Move <b>100 Inhalers</b> from <i>Gomti Nagar Main</i> to <i>Chowk ER</i>.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Approve Lateral Transfer", type="primary", use_container_width=True):
            st.toast('Transfer order dispatched to logistics network!', icon='✅')
            
    else:
        st.markdown("""
        <div class="alert-box">
            <h4 style="color: #b91c1c; margin-top:0;">⚠️ WARNING: Aliganj Outpost</h4>
            <p><b>Sociological Risk:</b> High stagnant water proximity.</p>
            <p><b>Epidemiological Trigger:</b> Sustained 80%+ humidity post-monsoon.</p>
            <p><b>Forecast:</b> 65% probability of Dengue cluster in 10 days.</p>
        </div>
        <div class="action-box">
            <h4 style="color: #15803d; margin-top:0;">⚡ Recommended Logistics Action</h4>
            <p>Anticipatory Push: Dispatch <b>150 Dengue Kits</b> from Central Warehouse.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Approve Warehouse Dispatch", type="primary", use_container_width=True):
            st.toast('Dispatch order routed to Central Warehouse!', icon='✅')

st.markdown("---")
st.subheader("Predictive Demand Curve (Time-Series Forecast)")

# Generate realistic-looking time series data for the chart
dates = [datetime.today() + timedelta(days=i) for i in range(forecast_days)]
baseline = np.random.randint(10, 20, size=forecast_days)
# Create a surge based on the selected forecast window to simulate AI prediction
surge = np.exp(-((np.arange(forecast_days) - (forecast_days // 2)) ** 2) / 10) * 80
predicted_demand = baseline + surge

chart_df = pd.DataFrame({
    'Date': dates,
    'Historical Baseline (Reactive)': baseline,
    'AI Predicted Demand (Proactive)': predicted_demand
}).set_index('Date')

st.line_chart(chart_df, color=["#94a3b8", "#ef4444"])
