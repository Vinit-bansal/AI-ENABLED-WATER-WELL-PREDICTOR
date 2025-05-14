import streamlit as st
from PIL import Image

# Configure the page
st.set_page_config(
    page_title="AI-enabled Well Water Prediction System",
    page_icon="💧",
    layout="wide"
)

# Load logo
logo = Image.open("logo.png")

# Header section with logo and title
col1, col2 = st.columns([1, 6])
with col1:
    st.image(logo, width=80)
with col2:
    st.markdown("<h1 style='margin-bottom:0;'>AI-enabled Well Water Prediction System</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='color:gray; margin-top:5px;'>Forecasting Groundwater Availability Across Indian Regions</h4>", unsafe_allow_html=True)

# Divider
st.markdown("---")

# Introduction Box
st.markdown("""
<div style='padding: 20px; background-color: #FFFFFF; border-left: 5px solid #2C6E49; border-radius: 8px; font-size: 17px;'>
    🌊 Welcome to the AI-powered platform developed to help <strong>farmers, engineers, researchers, and policy-makers</strong> make informed decisions about groundwater well construction and usage.<br><br>
    With integrated NAQUIM data from CGWB, this system predicts water availability, drilling needs, extraction sustainability, and much more.
</div>
""", unsafe_allow_html=True)

# Spacer
st.markdown("")

# Features Section
st.markdown("### 🔧 Key Features")
st.markdown("""
- ✅ AI-based prediction of groundwater well suitability  
- 📏 Estimates of expected water-bearing depth and discharge  
- 🚜 Recommended drilling technique based on aquifer data  
- 📊 Dashboards for district/state-wise analysis  
- 💦 Water quality trends and TDS maps  
- 📥 One-click PDF report generation  
- 🗳️ Feedback collection for continuous improvement
""")

# Final Acknowledgment or Footer
st.markdown("---")
st.markdown("""
<div style='text-align:center; font-size:14px; color: #888;'>
Empowering sustainable groundwater management through intelligent data-driven solutions.
</div>
""", unsafe_allow_html=True)
