
import streamlit as st
import pandas as pd
import datetime
import random
import string
import os
import save_vote_to_sheets

# App setup
st.set_page_config(page_title="🗳️ Guyana Voter Pulse", layout="centered")
st.title("🇬🇾 Guyana Voter Pulse")

CODES_FILE = "valid_codes.csv"
if not os.path.exists(CODES_FILE):
    pd.DataFrame(columns=["email", "code", "issued", "used"]).to_csv(CODES_FILE, index=False)

if "step" not in st.session_state:
    st.session_state.step = 1
if "email" not in st.session_state:
    st.session_state.email = ""
if "code" not in st.session_state:
    st.session_state.code = ""

# Step 1: Request Code
if st.session_state.step == 1:
    st.subheader("📩 Request One-Time Access Code")
    email = st.text_input("Enter your email address to receive a code:")
    if st.button("Request Code"):
        if "@" in email and "." in email:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            st.session_state.email = email
            st.session_state.code = code
            st.success(f"✅ Your code is: {code} (for demo/testing)")

            df = pd.read_csv(CODES_FILE)
            if not df[df["email"] == email].empty:
                st.warning("⚠️ Code already issued to this email.")
            else:
                df = pd.concat([df, pd.DataFrame([{
                    "email": email,
                    "code": code,
                    "issued": datetime.datetime.now(),
                    "used": False
                }])], ignore_index=True)
                df.to_csv(CODES_FILE, index=False)
            st.session_state.step = 2
            st.rerun()
        else:
            st.error("Please enter a valid email address.")

# Step 2: Enter Code
elif st.session_state.step == 2:
    st.subheader("🔐 Enter Your Access Code")
    entered = st.text_input("Enter the code sent to your email:")
    if st.button("Validate Code"):
        if entered:
            df = pd.read_csv(CODES_FILE)
            match = df[df["code"] == entered]
            if not match.empty and not match.iloc[0]["used"]:
                st.session_state.code = entered
                st.success("✅ Code validated.")
                st.session_state.step = 3
                st.rerun()
            else:
                st.error("❌ Invalid or already used code.")
        else:
            st.warning("Please enter your code.")

# Step 3: Voting Form
elif st.session_state.step == 3:
    st.subheader("🗳️ Cast Your Vote")
    with st.form("vote_form"):
        region = st.selectbox("Region", [f"Region {i}" for i in range(1, 11)])
        party = st.selectbox("Party", ["PPP", "APNU", "AFC", "LJP", "URP", "TNM", "ANUG", "ALP", "GAP", "Other"])
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
        st.info("🧠 Submit button clicked — preparing to save vote")
        save_vote_to_sheets(vote_data)

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

        st.warning("🧠 Calling save_vote_to_sheets() now...")
        st.success("🎯 Vote data passed to Google Sheets function.")

        df = pd.read_csv(CODES_FILE)
        df.loc[df["code"] == st.session_state.code, "used"] = True
        df.to_csv(CODES_FILE, index=False)

        st.session_state.step = 4
        st.rerun()

# Step 4: Done
elif st.session_state.step == 4:
    st.success("🎉 Thank you for voting! Your vote has been recorded.")
    st.markdown("🔒 This page can now be closed.")
