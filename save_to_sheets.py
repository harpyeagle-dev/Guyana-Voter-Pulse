import streamlit as st
from st_files_connection import FilesConnection
import pandas as pd
import gspread
from google.oauth2 import service_account

# Create a connection object using the secrets in your .streamlit/secrets.toml file
conn = st.connection("gsheets", type=FilesConnection)

# Function to append data to Google Sheets
def append_to_sheet(data_to_append):
    # Create a connection object using credentials from secrets
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["connections"]["gsheets"],
        scopes=[
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ],
    )
    
    # Create a gspread client
    client = gspread.authorize(credentials)
    
    # Open the spreadsheet (fresh_votes_template)
    spreadsheet = client.open("fresh_votes_template")
    
    # Select a worksheet (replace with your worksheet name or index)
    worksheet = spreadsheet.worksheet("fresh_votes_template")
    
    # Append the data
    worksheet.append_rows(data_to_append)
    
    return True

# Example usage
if st.button("Add Data"):
    # Example data to append (list of lists, each inner list is a row)
    new_data = [["John Doe", 30, "New York"], ["Jane Smith", 25, "Los Angeles"]]
    
    if append_to_sheet(new_data):
        st.success("Data successfully appended to Google Sheet!")
    else:
        st.error("Failed to append data.")
