import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Google Sheets Authentication
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)
sheet = client.open('YourGoogleSheetName').worksheet('users')  # Replace 'YourGoogleSheetName' and 'users' with your actual sheet name and worksheet

# Function to fetch unique values from a column in Google Sheets
def get_unique_values(sheet, column_name):
    column_values = sheet.col_values(column_name)
    unique_values = list(set(column_values[1:]))  # Exclude header and make unique
    return unique_values

# Streamlit App UI
st.title('Customer Action Tracker')

# Step 1: Select User Type (Populate based on user_type column)
user_types = get_unique_values(sheet, 'user_type')
user_type = st.selectbox('Select User Type', user_types)

# Step 2: Select Username (Populate based on selected user_type and shop)
filtered_usernames = [row[0] for row in sheet.get_all_values() if row[1] == user_type]  # Assuming usernames are in the 1st column (index 0)
username = st.selectbox('Select Username', filtered_usernames)

# Step 3: Select Shop (Populate based on selected username)
selected_row = [row for row in sheet.get_all_values() if row[0] == username][0]  # Assuming username is in the 1st column (index 0) and shop is in the 2nd column (index 1)
shop = selected_row[1]  # Assuming shop is in the 2nd column (index 1)

# Step 4: Input Customer ID
customer_id = st.text_input('Enter Customer ID')

# Validate Customer ID uniqueness
if customer_id:
    existing_customer_ids = sheet.col_values(4)[1:]  # Assuming Customer ID is in the 4th column (index 3 in Python)
    if customer_id in existing_customer_ids:
        st.error('Customer ID already exists. Please enter a unique Customer ID.')
        st.stop()

# Step 5: Select Action Type
action_type = st.selectbox('Select Action Type', ['Convince', 'Repo'])

# Step 6: Submit Button
if st.button('Submit'):
    # Save data to Google Sheets
    row_data = [username, shop, customer_id, action_type]
    sheet.append_row(row_data)
    st.success('Data submitted successfully!')
