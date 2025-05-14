import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="State & District-wise Water Usage", layout="wide")
st.title("🚿 Groundwater Usage Breakdown (Domestic vs Industrial)")

# Load data
df = pd.read_csv("Data/District_Statewise_Well.csv")
df.columns = [col.strip() for col in df.columns]

# Use 70:30 split assumption
df["Domestic Use (MCM)"] = df["Current Annual Ground Water Extraction For Domestic & Industrial Use"] * 0.7
df["Industrial Use (MCM)"] = df["Current Annual Ground Water Extraction For Domestic & Industrial Use"] * 0.3

st.markdown("### 🔎 Select View Type")
view_type = st.radio("Choose a level:", ["State-wise", "District-wise"], horizontal=True)

# ------------------ STATE LEVEL ----------------------
if view_type == "State-wise":
    grouped_state = df.groupby("Name of State").agg({
        "Domestic Use (MCM)": "sum",
        "Industrial Use (MCM)": "sum"
    }).reset_index()

    top_n = st.slider("Select Top N States by Domestic Use", 3, len(grouped_state), 10)
    grouped_state = grouped_state.sort_values(by="Domestic Use (MCM)", ascending=False).head(top_n)

    fig = px.bar(
        grouped_state,
        x="Name of State",
        y=["Domestic Use (MCM)", "Industrial Use (MCM)"],
        barmode="group",
        title="Top States: Domestic vs Industrial Water Use",
        color_discrete_map={
            "Domestic Use (MCM)": "#2E86AB",
            "Industrial Use (MCM)": "#F39C12"
        },
        labels={"value": "Water Use (MCM)", "Name of State": "State", "variable": "Use Type"}
    )
    st.plotly_chart(fig, use_container_width=True)

# ------------------ DISTRICT LEVEL ----------------------
else:
    selected_state = st.selectbox("Select a State", sorted(df["Name of State"].unique()))
    state_df = df[df["Name of State"] == selected_state]

    top_n = st.slider("Select Top N Districts by Domestic Use", 3, len(state_df), 10)
    state_df = state_df.sort_values(by="Domestic Use (MCM)", ascending=False).head(top_n)

    fig = px.bar(
        state_df,
        x="Name of District",
        y=["Domestic Use (MCM)", "Industrial Use (MCM)"],
        barmode="group",
        title=f"Top Districts in {selected_state}: Domestic vs Industrial Water Use",
        color_discrete_map={
            "Domestic Use (MCM)": "#2E86AB",
            "Industrial Use (MCM)": "#F39C12"
        },
        labels={"value": "Water Use (MCM)", "Name of District": "District", "variable": "Use Type"}
    )
    st.plotly_chart(fig, use_container_width=True)

# Optional: Raw data table toggle
with st.expander("📄 Show Raw Data"):
    st.write(df[["Name of State", "Name of District", "Domestic Use (MCM)", "Industrial Use (MCM)"]])
