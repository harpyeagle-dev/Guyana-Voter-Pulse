
import streamlit as st
st.set_page_config(page_title="🗳️ Guyana Voter Pulse", layout="centered")

import pandas as pd
import datetime
import os
import save_to_sheets

VOTES_FILE = "votes.csv"
CODES_FILE = "valid_codes.csv"

if "step" not in st.session_state:
    st.session_state.step = 1

if "code" not in st.session_state:
    st.session_state.code = ""

st.title("🗳️ Guyana Voter Pulse")

# --- Step 1: Request Access Code ---
if st.session_state.step == 1:
    st.subheader("Step 1: Request Access Code")
    email = st.text_input("Enter your email address to receive a one-time voting code:")
    if st.button("Request Code"):
        if "@" not in email or "." not in email:
            st.error("Please enter a valid email address.")
        else:
            st.session_state.code = "TEST001"  # Replace with generated code logic if needed
            st.success("✅ Code issued: TEST001 (For testing only)")
            st.session_state.step = 2
            st.rerun()

# --- Step 2: Verify Code ---
elif st.session_state.step == 2:
    st.subheader("Step 2: Verify Access Code")
    code_input = st.text_input("Enter your access code:")
    if st.button("Verify Code"):
        if os.path.exists("valid_codes.csv"):
            codes_df = pd.read_csv("valid_codes.csv")
            match = codes_df[codes_df["code"] == code_input]

            if not match.empty and not match.iloc[0]["used"]:
                st.success("✅ Code verified.")
                st.session_state.code = code_input
                st.session_state.step = 3
                st.rerun()
            elif not match.empty and match.iloc[0]["used"]:
                st.error("⚠️ This code has already been used.")
            else:
                st.error("❌ Invalid code.")
        else:
            st.error("Codes file missing.")

# --- Step 3: Cast Vote ---
elif st.session_state.step == 3:
    st.subheader("Step 3: Cast Your Vote")

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
                "Code": st.session_state.code,
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
            save_to_sheets(vote_data)
            st.session_state.step = 4
            st.rerun()

# --- Step 4: Dashboard / Summary ---
elif st.session_state.step == 4:
    st.subheader("Step 4: Thank You! View Voting Summary")
    st.success("✅ Your vote has been submitted.")
    st.balloons()
