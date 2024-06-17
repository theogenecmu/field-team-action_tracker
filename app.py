import streamlit as st
import requests

# Backend server URL
BACKEND_URL = 'http://localhost:5000/submit'

# Title of the app
st.title("Data Collection App")

# Form inputs
name = st.text_input("Name")
age = st.number_input("Age", min_value=0)
email = st.text_input("Email")

# Form submission
if st.button("Submit"):
    if not name or not age or not email:
        st.warning("All fields are required.")
    else:
        data = {
            'name': name,
            'age': age,
            'email': email
        }

        try:
            response = requests.post(BACKEND_URL, json=data)
            if response.status_code == 200:
                st.success("Data added successfully to SharePoint!")
            else:
                st.error(f"Failed to add data to SharePoint: {response.json().get('error')}")
        except Exception as e:
            st.error(f"Failed to connect to the backend server: {e}")
