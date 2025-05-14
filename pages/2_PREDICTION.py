import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from fpdf import FPDF

# Page title
st.title("💧 Current Water Level with NAQUIM Data")

# Load model training data
dataset_path = './Data/District_Statewise_Well.csv'
df_model = pd.read_csv(dataset_path).dropna()

# Features and target
X = df_model[[  
    'Recharge from rainfall During Monsoon Season',
    'Recharge from other sources During Monsoon Season',
    'Recharge from rainfall During Non Monsoon Season',
    'Recharge from other sources During Non Monsoon Season',
    'Total Natural Discharges'
]]
y = df_model['Annual Extractable Ground Water Resource']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predict on test set
y_pred = model.predict(X_test)

# Evaluation metrics
r2 = r2_score(y_test, y_pred)

# Display model evaluation metrics
with st.expander("📊 Model Evaluation Metrics"):
    st.markdown(f"**Accuracy:** {r2:.2f}")
    



# Load current draft data
df = pd.read_csv('./Data/Current_Draft.csv')

# Well depth suggestion logic
def calculate_well_depth(total_extraction):
    if total_extraction < 10000:
        return 112
    elif total_extraction < 15000:
        return 128
    elif total_extraction < 17000:
        return 141
    else:
        return 157

def recommend_drilling_method(depth):
    if depth < 100:
        return "Hand Bore or Auger Drilling"
    elif 100 <= depth < 150:
        return "Rotary Percussion Drilling"
    else:
        return "Rotary Rig with Mud Circulation"

# Input form
col1, col2 = st.columns(2)
with col1:
    name_of_state = st.selectbox('Select State', df['Name of State'].unique())
    selected_district = st.selectbox('Select District', df[df['Name of State'] == name_of_state]['Name of District'].unique())
    recharge_rain_monsoon = st.text_input('Recharge from rainfall During Monsoon Season (MCM)')
    recharge_other_monsoon = st.text_input('Recharge from other sources During Monsoon Season (MCM)')

with col2:
    recharge_rain_nonmonsoon = st.text_input('Recharge from rainfall During Non Monsoon Season (MCM)')
    recharge_other_nonmonsoon = st.text_input('Recharge from other sources During Non Monsoon Season (MCM)')
    natural_discharges = st.text_input('Total Natural Discharges (MCM)')

# Predict button
if st.button('🔮 Predict Total Extractable Ground Water Resource'):
    if not recharge_rain_monsoon or not recharge_other_monsoon or not recharge_rain_nonmonsoon or not recharge_other_nonmonsoon or not natural_discharges:
        st.warning("⚠️ Please enter all the input fields.")
    else:
        input_data = pd.DataFrame({
            'Recharge from rainfall During Monsoon Season': [float(recharge_rain_monsoon)],
            'Recharge from other sources During Monsoon Season': [float(recharge_other_monsoon)],
            'Recharge from rainfall During Non Monsoon Season': [float(recharge_rain_nonmonsoon)],
            'Recharge from other sources During Non Monsoon Season': [float(recharge_other_nonmonsoon)],
            'Total Natural Discharges': [float(natural_discharges)],
        })

        predicted_resource = model.predict(input_data)[0]
        st.success(f"✅ **Total Extractable Ground Water Resource:** {predicted_resource:.2f} MCM")

        filtered_df = df[(df['Name of State'] == name_of_state) & (df['Name of District'] == selected_district)]

        if filtered_df.empty:
            st.warning("⚠️ No matching district data found.")
        else:
            total_extraction = filtered_df['Total Current Annual Ground Water Extraction'].values[0]
            st.info(f"💦 Total Current Annual Ground Water Extraction: {total_extraction:.2f} MCM")

            if predicted_resource < 1:
                st.error("❌ Predicted resource is too low to calculate stage.")
            else:
                stage_extraction = (total_extraction / predicted_resource) * 100

                # Stage interpretation
                if stage_extraction < 70:
                    st.success(f"🟢 Stage of Extraction: {stage_extraction:.2f}% (Safe)")
                elif stage_extraction < 90:
                    st.warning(f"🟠 Stage of Extraction: {stage_extraction:.2f}% (Semi-critical)")
                elif stage_extraction <= 100:
                    st.warning(f"🔴 Stage of Extraction: {stage_extraction:.2f}% (Critical)")
                else:
                    st.error(f"🚨 Stage of Extraction: {stage_extraction:.2f}% (Over-exploited)")

                # Well depth and method
                suggested_depth = calculate_well_depth(total_extraction)
                drill_method = recommend_drilling_method(suggested_depth)
                st.info(f"📏 Suggested Well Depth: {suggested_depth} meters")
                st.info(f"🛠️ Recommended Drilling Technique: {drill_method}")

                # PDF generation
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", 'B', 16)
                pdf.cell(200, 10, "Groundwater Prediction Report", ln=1, align='C')
                pdf.set_font("Arial", '', 12)
                pdf.ln(10)
                pdf.cell(200, 10, f"State: {name_of_state}", ln=1)
                pdf.cell(200, 10, f"District: {selected_district}", ln=1)
                pdf.cell(200, 10, f"Predicted Resource: {predicted_resource:.2f} MCM", ln=1)
                pdf.cell(200, 10, f"Total Extraction: {total_extraction:.2f} MCM", ln=1)
                pdf.cell(200, 10, f"Stage of Extraction: {stage_extraction:.2f}%", ln=1)
                pdf.cell(200, 10, f"Well Depth Suggestion: {suggested_depth} meters", ln=1)
                pdf.cell(200, 10, f"Drilling Method: {drill_method}", ln=1)

                pdf_data = pdf.output(dest='S').encode('latin1')

                st.download_button(
                    label="📥 Download Report as PDF",
                    data=pdf_data,
                    file_name=f"{selected_district}_{name_of_state}_groundwater_report.pdf",
                    mime="application/pdf"
                )
