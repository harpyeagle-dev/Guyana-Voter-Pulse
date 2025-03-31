import gspread
from google.auth.exceptions import GoogleAuthError
from gspread.exceptions import APIError
import streamlit as st

def save_vote_to_sheets(vote_data):
    try:
        # Authenticate
        gc = gspread.service_account(filename="credentials.json")  # Or use from_dict with st.secrets if on Streamlit Cloud

        # List all visible spreadsheets for debugging
        files = gc.list_spreadsheet_files()
        spreadsheet_names = [f['name'] for f in files]
        print(f"Found spreadsheets: {spreadsheet_names}")

        # Attempt to open the target sheet
        try:
            sh = gc.open("fresh_votes_template")
        except gspread.SpreadsheetNotFound:
            st.error("Spreadsheet 'fresh_votes_template' not found. Make sure it exists and is shared with the service account.")
            return

        worksheet = sh.sheet1

        # Append the vote data to the sheet
        worksheet.append_row(vote_data)
        st.success("Vote successfully saved to Google Sheet.")

    except GoogleAuthError as e:
        st.error(f"Authentication failed: {e}")
        print(f"Auth error: {e}")

    except APIError as e:
        st.error("Google Sheets API error. Check logs for full details.")
        print(f"API error: {e}")

    except Exception as e:
        st.error("An unexpected error occurred.")
        print(f"Unexpected error: {e}")
