import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(page_title="Dashboard", layout="wide")

# Load and clean data
graph_df = pd.read_csv("data/graph.csv")
graph_df.rename(columns={
    'Name of State': 'State',
    'Name of District': 'District',
    'Predicted Annual Extractable Ground Water Resource': 'PredictedResource',
    'Annual Extractable Ground Water Resource': 'ActualResource'
}, inplace=True)

# Sidebar filters
st.sidebar.title("🔍 Filter")
states = graph_df['State'].dropna().unique()
selected_state = st.sidebar.selectbox("Select State", options=states)

filtered_state_df = graph_df[graph_df['State'] == selected_state]
districts = filtered_state_df['District'].dropna().unique()
selected_district = st.sidebar.selectbox("Select District", options=districts)

filtered_data = filtered_state_df[filtered_state_df['District'] == selected_district]

# Dashboard title
st.title("📊 Groundwater Well Resource Dashboard")
st.write(f"Displaying data for **{selected_district}**, **{selected_state}**")

# Metrics
col1, col2 = st.columns(2)
with col1:
    st.metric("Predicted Resource (MCM)", 
              round(filtered_data['PredictedResource'].mean(), 2) if not filtered_data.empty else "N/A")
with col2:
    st.metric("Actual Resource (MCM)", 
              round(filtered_data['ActualResource'].mean(), 2) if not filtered_data.empty else "N/A")

# Graph
if not filtered_data.empty:
    df_melted = filtered_data.melt(
        id_vars='District',
        value_vars=['PredictedResource', 'ActualResource'],
        var_name='Type',
        value_name='Value'
    )
    fig = px.bar(df_melted, x='District', y='Value', color='Type',
                 barmode='group', title="Predicted vs Actual Resource")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No data available for selected inputs.")
