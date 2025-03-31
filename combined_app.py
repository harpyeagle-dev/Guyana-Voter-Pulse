
import streamlit as st
st.set_page_config(page_title="🗳️ Guyana Voter Pulse", layout="centered")

import pandas as pd
import datetime
import os
import smtplib
from email.mime.text import MIMEText
from Modules.save_to_sheets import save_votes_to_sheets

# --- Email sending logic ---
def send_code_email(to_email, code):
    st.info(f"📤 Sending code to {to_email}")
    sender = st.secrets["EMAIL"]["address"]
    password = st.secrets["EMAIL"]["password"]

    body = f"Your one-time voting code is: {code}"
    msg = MIMEText(body)
    msg["Subject"] = "Your Guyana Voter Pulse Access Code"
    msg["From"] = sender
    msg["To"] = to_email

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        st.error(f"❌ Email failed: {e}")
        return False

# --- Step control ---
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
            try:
                codes_df = pd.read_csv("valid_codes.csv")
                available = codes_df[codes_df["used"] == False]

                if not available.empty:
                    selected_code = available.iloc[0]["code"]
                    codes_df.loc[codes_df["code"] == selected_code, "used"] = True
                    codes_df.to_csv("valid_codes.csv", index=False)

                    success = send_code_email(email, selected_code)

                    if success:
                        st.success("✅ Code sent to your email.")
                        st.session_state.code = selected_code
                        st.session_state.step = 2
                        st.rerun()
                    else:
                        st.error("❌ Email failed to send.")
                else:
                    st.error("⚠️ No codes available.")
            except Exception as e:
                st.error(f"Error loading codes: {e}")

# --- Step 2: Verify Code ---
elif st.session_state.step == 2:
    st.subheader("Step 2: Verify Access Code")
    code_input = st.text_input("Enter the code you received:")
    if st.button("Verify Code"):
        codes_df = pd.read_csv("valid_codes.csv")
        match = codes_df[codes_df["code"] == code_input]
        if not match.empty and match.iloc[0]["used"]:
            st.success("✅ Code verified.")
            st.session_state.code = code_input
            st.session_state.step = 3
            st.rerun()
        elif not match.empty:
            st.error("⚠️ This code was already used.")
        else:
            st.error("❌ Invalid code.")

# --- Step 3: Voting Form ---
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
            save_votes_to_sheets(vote_data)
            st.session_state.step = 4
            st.rerun()

# --- Step 4: Summary ---
elif st.session_state.step == 4:
    st.success("✅ Thank you for casting your vote!")
    st.balloons()
