import streamlit as st
from google.oauth2 import service_account
import gspread

def save_votes_to_sheets(vote_data):
    scope = ["https://www.googleapis.com/auth/spreadsheets"]
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["google_service_account"],
        scopes=scope
    )
    client = gspread.authorize(credentials)

    sheet = client.open("fresh_votes_template").sheet1
    sheet.append_row([vote_data['choice'], vote_data['timestamp']])
