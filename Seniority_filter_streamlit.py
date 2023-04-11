import pandas as pd
import streamlit as st
import base64


def app():
    # Define the list of substrings to search for
    # Case sensitive substring
    substringsCS = ['CEO', 'COO', 'CFO', 'CTO', 'CHRO', 'CMO', 'CLO', 'CSO', 'CIO', 'CTIO', 'CSIO', 'CCO', 'CDO', 'VP']
    # Case insensitive substring 
    substringsCI = ['Chief','Vice President', 'Vice-President', 'Partner', 'Owner', 'Founder','President']
    
    st.title("Seniority Filter V1")
    st.subheader("Property of Connected Circles")
    
    # File uploader
    uploaded_file = st.file_uploader("Choose a CSV file to filter", type="csv")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        # Create a boolean mask to identify rows where the "Title" column contains any of the case-sensitive substrings
        maskCS = df['Title'].str.contains('|'.join(substringsCS))

        # Create a boolean mask to identify rows where the "Title" column contains any of the case-insensitive substrings
        maskCI = df['Title'].str.contains('|'.join(substringsCI), case=False)

        # Create a new column called "CXO+" with a value of "Yes" for rows that match either condition, and "No" otherwise
        df['CXO+'] = (maskCS | maskCI).map({True: 'Yes', False: 'No'})

        # Filter to only include CXO+, delete CXO+ column
        dffiltered = df[df["CXO+"]=="Yes"]
        dffiltered = dffiltered.drop("CXO+", axis=1)

        # Download link
        csv = dffiltered.to_csv(index=False)
        b64 = base64.b64encode(csv.encode('utf-8')).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="filtered_data.csv">Download Filtered CSV File</a>'

        # Display filtered data and download link
        st.write(dffiltered)
        st.markdown(href, unsafe_allow_html=True)


if __name__ == "__main__":
    app()
