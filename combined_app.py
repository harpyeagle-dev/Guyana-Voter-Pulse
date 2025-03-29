
import streamlit as st
st.set_page_config(page_title="🗳️ Guyana Voter Pulse", layout="centered")

import pandas as pd
import datetime
import save_to_sheets

# Example voting interface
st.title("Guyana Voter Pulse")

# Basic form to simulate voting
with st.form("vote_form"):
    region = st.selectbox("Region", [f"Region {i}" for i in range(1, 11)])
    party = st.selectbox("Party", ["PPP", "APNU", "AFC", "GAP", "Other"])
    candidate = st.text_input("Preferred presidential candidate")
    reason = st.text_area("Why this candidate? (optional)")
    age = st.selectbox("Age", ["18–24", "25–34", "35–44", "45–54", "55+"])
    gender = st.radio("Gender", ["Male", "Female", "Other"])
    diaspora = st.radio("Where do you live?", ["In Guyana", "Diaspora"])
    issues = st.multiselect("Top 3 issues", ["Jobs", "Education", "Healthcare", "Cost of living", "Crime", "Corruption", "Infrastructure"])
    fair = st.radio("Do you believe the election will be fair?", ["Yes", "No", "Not sure"])
    gecom = st.radio("Do you trust GECOM?", ["Yes", "No", "Not sure"])
    submit_vote = st.form_submit_button("Submit Vote")

if submit_vote:
    if len(issues) > 3:
        st.error("⚠️ Please select no more than 3 issues.")
    else:
        vote_data = {
            "Timestamp": datetime.datetime.now(),
            "Code": "TEST001",
            "Region": region,
            "Party": party,
            "Preferred Candidate": candidate,
            "Candidate Reason": reason,
            "Age": age,
            "Gender": gender,
            "Diaspora": diaspora,
            "Top Issues": ", ".join(issues),
            "Fairness": fair,
            "GECOM Trust": gecom
        }
        save_votes_to_sheets(vote_data)
