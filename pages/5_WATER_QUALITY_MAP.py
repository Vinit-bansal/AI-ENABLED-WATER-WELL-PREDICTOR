import streamlit as st
import pandas as pd
import plotly.express as px


# Page setup
st.set_page_config(page_title="Water Quality Map", layout="wide")
st.title("📍 Groundwater Sample Locations with Chemistry")

# Load and clean data
df = pd.read_csv("data/data_20221_cleaned.csv")
df.columns = [col.strip() for col in df.columns]

# Convert data types
for col in ['LATITUDE', 'LONGITUDE', 'TDS', 'pH', 'EC', 'NO3', 'U(ppb)', 'Ca', 'F']:
    df[col] = pd.to_numeric(df[col], errors='coerce')

df = df.dropna(subset=['LATITUDE', 'LONGITUDE'])

# Sidebar filters
st.sidebar.header("🔍 Filter & Location Info")

# State selection
states = sorted(df['STATE'].dropna().unique())
selected_state = st.sidebar.selectbox("Select State", states)

# Copy to avoid SettingWithCopyWarning
state_df = df[df['STATE'] == selected_state].copy()

# Location selection
locations = sorted(state_df['LOCATION'].dropna().unique())
selected_location = st.sidebar.selectbox("Select Location", locations)

# Get selected location data
point_data = state_df[state_df['LOCATION'] == selected_location].iloc[0]

# Sidebar details
st.sidebar.markdown("### 📊 Water Chemistry")
st.sidebar.markdown(f"**District**: {point_data['DISTRICT']}")
st.sidebar.markdown(f"**TDS**: {point_data['TDS']} mg/L")
st.sidebar.markdown(f"**pH**: {point_data['pH']}")
st.sidebar.markdown(f"**EC**: {point_data['EC']} µS/cm")
st.sidebar.markdown(f"**NO₃**: {point_data['NO3']} mg/L")
st.sidebar.markdown(f"**Fluoride (F)**: {point_data['F']} mg/L")
st.sidebar.markdown(f"**Uranium (U)**: {point_data['U(ppb)']} ppb")

# Download buttons
st.sidebar.markdown("---")
st.sidebar.markdown("### 📥 Download Data")
st.sidebar.download_button(
    label="⬇ Download State Data as CSV",
    data=state_df.to_csv(index=False).encode('utf-8'),
    file_name=f"{selected_state}_groundwater_data.csv",
    mime="text/csv"
)

st.sidebar.download_button(
    label="⬇ Download Location Data as CSV",
    data=point_data.to_frame().T.to_csv(index=False).encode('utf-8'),
    file_name=f"{selected_location}_groundwater_data.csv",
    mime="text/csv"
)

# Cap TDS for color scaling
state_df['TDS_Capped'] = state_df['TDS'].apply(lambda x: min(x, 1000) if pd.notna(x) else 0)

# Create Plotly map
fig = px.scatter_map(
    state_df,
    lat="LATITUDE",
    lon="LONGITUDE",
    color="TDS_Capped",
    color_continuous_scale="Turbo",
    zoom=6,
    hover_name="LOCATION",
    height=700,
    hover_data={
        "DISTRICT": True,
        "TDS": True,
        "pH": True,
        "EC": True,
        "NO3": True,
        "F": True,
        "U(ppb)": True,
        "LATITUDE": False,
        "LONGITUDE": False
    },
    title=f"🗺️ Groundwater Sample Locations in {selected_state}"
)

fig.update_layout(mapbox_style="open-street-map", margin={"r":0,"t":40,"l":0,"b":0})
st.plotly_chart(fig, use_container_width=True)
