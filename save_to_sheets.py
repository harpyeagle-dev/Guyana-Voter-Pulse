
import streamlit as st
import gspread
from google.oauth2 import service_account

def save_vote_to_sheets(vote_data):
    st.info("📡 Connecting to Google Sheets...")

    try:
        # Load credentials from Streamlit secrets
        credentials = service_account.Credentials.from_service_account_info(
            st.secrets["connections"]["gsheets"],
            scopes=[
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive"
            ],
        )

        client = gspread.authorize(credentials)

        # Open spreadsheet and select sheet
        spreadsheet = client.open("fresh_votes_template")  # Name of your Google Sheet
        worksheet = spreadsheet.worksheet("Sheet1")        # Change if your tab has a different name

        row = list(vote_data.values())
        worksheet.append_row(row)

        st.success("✅ Vote successfully saved to Google Sheets!")

    except Exception as e:
        st.error("❌ Failed to save vote to Google Sheets.")
        st.exception(e)
