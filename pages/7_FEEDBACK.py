import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="User Feedback", layout="centered")
st.title("📝 Feedback Form")

st.write("We value your feedback! Please share your thoughts about the system.")

# Input fields
name = st.text_input("Name")
email = st.text_input("Email")
rating = st.slider("Rate the system (1 = Poor, 5 = Excellent)", 1, 5, 3)
comments = st.text_area("Your suggestions or comments")

if st.button("Submit Feedback"):
    if name and email:
        feedback = {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Name": name,
            "Email": email,
            "Rating": rating,
            "Comments": comments
        }

        feedback_df = pd.DataFrame([feedback])

        # Save to feedback.csv
        feedback_path = "data/feedback.csv"
        if os.path.exists(feedback_path):
            existing = pd.read_csv(feedback_path)
            feedback_df = pd.concat([existing, feedback_df], ignore_index=True)

        feedback_df.to_csv(feedback_path, index=False)
        st.success("✅ Thank you for your feedback!")
    else:
        st.warning("Please enter your name and email.")
