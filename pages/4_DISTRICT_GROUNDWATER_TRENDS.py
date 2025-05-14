# pages/groundwater_trend.py

import streamlit as st
import pandas as pd
import plotly.graph_objects as go


st.title("📊 Groundwater Status by District")

# Load the updated CSV file
df = pd.read_csv("Data/Current_Draft.csv")

# Clean up column names
df.columns = [col.strip() for col in df.columns]

# Dropdowns for selection
states = sorted(df['Name of State'].dropna().unique())
selected_state = st.selectbox("Select State", states)

districts = sorted(df[df['Name of State'] == selected_state]['Name of District'].dropna().unique())
selected_district = st.selectbox("Select District", districts)

# Filter data
data = df[(df['Name of State'] == selected_state) & (df['Name of District'] == selected_district)]

if not data.empty:
    st.subheader(f"💧 Groundwater Details for {selected_district}, {selected_state}")
    
    # Extract values
    total_extraction = data['Total Current Annual Ground Water Extraction'].values[0]
    future_availability = data['Net Ground Water Availability for future use'].values[0]
    stage_percent = data['Stage of Ground Water Extraction (%)'].values[0]

    # Create bar chart
    fig = go.Figure(data=[
        go.Bar(name="Total Extraction", x=["Extraction"], y=[total_extraction], marker_color='crimson'),
        go.Bar(name="Availability for Future Use", x=["Availability"], y=[future_availability], marker_color='seagreen'),
        go.Bar(name="Extraction Stage (%)", x=["Extraction Stage"], y=[stage_percent], marker_color='orange')
    ])

    fig.update_layout(title=f"Groundwater Extraction vs Availability in {selected_district}",
                      yaxis_title="Volume (in MCM or %)",
                      xaxis_title="Metric",
                      barmode='group')

    st.plotly_chart(fig, use_container_width=True)

    # Show raw data below
    st.markdown("### 📋 Full Data for Selected District")
    st.write(data)
else:
    st.warning("No data available for the selected state and district.")
