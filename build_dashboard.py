import streamlit as st
import pandas as pd
from datetime import datetime
import pytz

# Import your chart functions (they should still work as they return Plotly figures)
from task1 import generate_task1_chart
from task2 import generate_task2_chart
from task3 import generate_task3_chart
from task4 import generate_task4_chart
from task5 import generate_task5_chart
from task6 import generate_task6_chart

# -------------------------- Page Config --------------------------
st.set_page_config(
    page_title="Google Play Store Analytics",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------- Load Data --------------------------
@st.cache_data
def load_data():
    return pd.read_csv("data/cleaned_playstore.csv")

data = load_data()

# -------------------------- Sidebar --------------------------
st.sidebar.image("images/playstore_icon.png", width=80)  # optional
st.sidebar.title("Google Play Store Dashboard")
st.sidebar.markdown("### Interactive Analytics")

# Optional: Bring back time-based info (just for fun)
ist = pytz.timezone('Asia/Kolkata')
now = datetime.now(ist)
st.sidebar.caption(f"Current IST time: **{now.strftime('%H:%M')}**")

st.sidebar.markdown("---")
st.sidebar.info(
    "All visualizations are now available 24/7.\n"
    "The original time-window restrictions have been removed."
)

# -------------------------- Main Dashboard --------------------------
st.title("📊 Google Play Store Analytics Dashboard")
st.markdown("### Explore insights from the Play Store dataset")

# Use tabs for a clean, modern layout
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Task 1: Category Analysis",
    "Task 2: Rating Distribution",
    "Task 3: Sentiment Visualization",
    "Task 4: Multilingual Categories",
    "Task 5: Size vs Rating Bubble",
    "Task 6: Cumulative Installs"
])

with tab1:
    st.subheader("Task 1: Number of Apps per Category")
    fig1 = generate_task1_chart(data)
    st.plotly_chart(fig1, use_container_width=True)

with tab2:
    st.subheader("Task 2: Average Rating per Category")
    fig2 = generate_task2_chart(data)
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    st.subheader("Task 3: Sentiment Analysis on Reviews")
    fig3 = generate_task3_chart(data)
    st.plotly_chart(fig3, use_container_width=True)

with tab4:
    st.subheader("Task 4: Multilingual Category Names")
    fig4 = generate_task4_chart(data)
    st.plotly_chart(fig4, use_container_width=True)

with tab5:
    st.subheader("Task 5: Bubble Chart — Size vs Rating")
    fig5 = generate_task5_chart(data)
    st.plotly_chart(fig5, use_container_width=True)

with tab6:
    st.subheader("Task 6: Stacked Area — Cumulative Installs")
    fig6 = generate_task6_chart(data)
    st.plotly_chart(fig6, use_container_width=True)

# -------------------------- Footer --------------------------
st.markdown("---")
st.caption("Built with Streamlit + Plotly | Original project by jovinryan20")
