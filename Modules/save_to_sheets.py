# save_to_sheets.py

import gspread
from google.auth.exceptions import GoogleAuthError
from gspread.exceptions import APIError
import streamlit as st

def save_vote_to_sheets(vote_data):
    try:
        # Use credentials.json if local or st.secrets if on Streamlit Cloud
        gc = gspread.service_account(filename="credentials.json")
        # gc = gspread.service_account_from_dict(st.secrets["gcp_service_account"])  # if using secrets.toml

        # Open the sheet
        try:
            sh = gc.open("fresh_votes_template")
            worksheet = sh.sheet1
        except gspread.SpreadsheetNotFound:
            st.error("Spreadsheet 'fresh_votes_template' not found.")
            return

        # Append the vote data to the next row
        worksheet.append_row(vote_data)
        st.success("✅ Vote saved successfully!")

    except GoogleAuthError as e:
        st.error("Google authentication failed.")
        print(f"Auth error: {e}")

    except APIError as e:
        st.error("Google Sheets API error.")
        print(f"API error: {e}")

    except Exception as e:
        st.error("Unexpected error occurred.")
        print(f"Unexpected error: {e}")
