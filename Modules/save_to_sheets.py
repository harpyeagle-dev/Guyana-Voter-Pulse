import gspread
from google.oauth2.service_account import Credentials

def save_vote_to_sheets(vote_data):
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]

    creds = Credentials.from_service_account_info(
        st.secrets["google_service_account"], scopes=scope
    )
    client = gspread.authorize(creds)
    
    # Open sheet by name or URL
    sheet = client.open("fresh_votes_template").sheet1
    
    # Append the values as a new row
    row = list(vote_data.values())
    sheet.append_row(row)
