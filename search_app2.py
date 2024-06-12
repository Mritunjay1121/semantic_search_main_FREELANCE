"""
    Create an Streamlit app that does the following:

    - Reads an input from the user
    - Embeds the input
    - Search the vector DB for the entries closest to the user input
    - Outputs/displays the closest entries found
"""
import streamlit as st
import pandas as pd
from embed_and_store_data import embed
# Set page title and favicon
st.set_page_config(page_title="Simple Search App", page_icon=":mag:", layout="wide")

# Custom CSS for styling
st.markdown(
    """
    <style>
        body {
            background-color: #f0f2f6;  /* Light gray background */
        }
        .stButton>button {
            background-color: #3366ff;  /* Blue button color */
            color: white;  /* Text color */
        }
        .stTextInput>div>div>input {
            background-color: #ffffff;  /* White input field background */
            color: #333333;  /* Text color */
        }
    </style>
    """,
    unsafe_allow_html=True
)

def main():
    st.title("Simple Search App")
    
    # Input field for user input
    user_input = st.text_input("Enter your query:")
    
    if st.button("Search"):
        # Perform search or processing based on user input
        if user_input:
            # Example: Display user input on the screen
            print("Starting")
            closest_entry=embed(user_input)
            print("Ended")

            st.write("Closest entry: ", closest_entry)
        else:
            st.write("Please enter a query.")

if __name__ == "__main__":
    main()
