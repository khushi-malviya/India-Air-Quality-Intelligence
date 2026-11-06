
import streamlit as st

st.set_page_config(
    page_title="India Air Quality Intelligence",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling
st.markdown("""
<style>
    .main-title {
        font-size: 2.6rem;
        font-weight: 800;
        color: #1F2937;
        margin-bottom: 0.2rem;
    }

    .subtitle {
        font-size: 1.1rem;
        color: #64748B;
        margin-bottom: 1.5rem;
    }

    .hero {
        padding: 2rem;
        border-radius: 16px;
        background: linear-gradient(120deg, #102A43, #1D5D72);
        color: white;
        margin: 1rem 0 2rem 0;
    }

    .hero h2 {
        color: white;
        font-size: 1.8rem;
    }

    .hero p {
        color: #E2E8F0;
        font-size: 1rem;
    }

    .section-title {
        font-size: 1.35rem;
        font-weight: 700;
        margin-top: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown(
    '<div class="main-title">🌍 India Air Quality Intelligence</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Transforming air quality data into actionable insights</div>',
    unsafe_allow_html=True
)

# Hero section
st.markdown("""
<div class="hero">
    <h2>Understand Pollution. Explore Trends. Forecast AQI.</h2>
    <p>
        An interactive data intelligence platform exploring historical
        air quality patterns across Indian cities, identifying pollution
        hotspots and forecasting AQI 24 hours ahead.
    </p>
</div>
""", unsafe_allow_html=True)

# Dataset information
st.markdown('<div class="section-title">About This Project</div>',
            unsafe_allow_html=True)

st.write("""
This platform analyzes historical air quality observations from
monitoring stations across India between 2017 and 2023.

It combines exploratory data analysis, statistical testing,
feature engineering and machine learning to uncover pollution
patterns and support data-driven environmental insights.
""")

st.markdown('<div class="section-title">Explore the Dashboard</div>',
            unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.info(
        "**National Overview**\n\n"
        "Explore national AQI patterns, category distributions "
        "and historical pollution indicators."
    )

    st.info(
        "**City Risk Assessment**\n\n"
        "Compare cities, identify pollution hotspots "
        "and explore seasonal risk patterns."
    )

with col2:
    st.info(
        "**Historical Analysis**\n\n"
        "Investigate monthly, seasonal, annual "
        "and hourly AQI trends."
    )

    st.info(
        "**AQI Forecasting**\n\n"
        "Explore 24-hour AQI predictions generated "
        "by the trained machine learning model."
    )

st.markdown("---")

st.caption(
    "Data coverage: January 2017 – December 2023 | "
    "Historical dataset, not a live AQI monitoring service."
)
