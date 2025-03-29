
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def save_vote_to_sheets(vote_data):
    st.warning("🧠 DEBUG: save_vote_to_sheets() called")

    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(
            st.secrets["google_service_account"], scope
        )
        st.success("✅ Credentials loaded")

        client = gspread.authorize(creds)
        sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1Vd1j96QzMOks9Uex98u1EZ7PYb2NRdf2w6h6fFfTdJA").sheet1
        st.success("✅ Connected to sheet: " + sheet.title)

        row = list(vote_data.values())
        sheet.append_row(row)
        st.success("✅ Vote appended to Google Sheet")

    except Exception as e:
        st.error("❌ Error writing to Google Sheets:")
        st.exception(e)
