import pandas as pd
import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# Load the CSV file into a DataFrame
df = pd.read_csv('combined_block.csv', delimiter=',', encoding='utf-8')

# Handle missing values if any
df = df.dropna()

# Convert timestamps to datetime objects
df['block_timestamp'] = pd.to_datetime(df['block_timestamp'], unit='s')
df['transaction_timestamp'] = pd.to_datetime(df['transaction_timestamp'], unit='s')

# Set the page layout and title
st.set_page_config(page_title="Blockchain Data Explorer", layout="wide")

# Add custom CSS for styling
st.markdown(
    """
    <style>
    body {
        color: white;
        background-color: #2c3e50; /* Dark background for contrast */
    }
    .sidebar .sidebar-content {
        background-color: #34495e; /* Darker sidebar background */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# URL of the image hosted on GitHub
image_url = "https://raw.githubusercontent.com/Sneakyfox1051/Fox-Chain/main/sneakyfox_1051-removebg-preview.png"

# Fetch the image
response = requests.get(image_url)
image = Image.open(BytesIO(response.content))

# Display the image at the topmost portion
st.image(image, use_column_width=False, width=70)  # Adjust width as needed

# Main title and description
st.title('Fox Chain - Blockchain Data Explorer')
st.write("""
    Explore and query blockchain data easily. 
    You can ask questions or view specific details from the blockchain.
""")

# Sidebar for toggling between Query and Search
st.sidebar.header("Navigation")
option = st.sidebar.selectbox("Choose an option:", ("Query Blockchain Data", "Search Blockchain Data"))

# Function to handle the query model
def query_model(query, df):
    # Normalize the query to lowercase and strip surrounding whitespace
    query = query.lower().strip().rstrip('.')

    # Informative responses
    informative_responses = {
        "what is meant by the amount in blockchain?": "The 'amount' in a blockchain transaction represents the value being transferred from one party to another. It is often expressed in a specific currency or token.",
        "what does a block represent?": "A block in a blockchain contains a collection of transactions that have been validated and recorded. Each block is linked to the previous one, forming a chain.",
        "what is the purpose of a blockchain?": "Blockchain technology provides a secure and transparent way to record transactions and data across a distributed network, ensuring integrity and trust without a central authority.",
        "what is meant by the sender in blockchain?": "The 'sender' in a blockchain transaction is the party initiating the transfer of value or data to another party (the receiver).",
        "what is meant by the receiver in blockchain?": "The 'receiver' in a blockchain transaction is the party that receives the value or data from the sender.",
        "what is a transaction id?": "A transaction ID is a unique identifier assigned to each transaction in the blockchain, allowing for easy tracking and verification.",
        "what is meant by nonce in blockchain?": "A nonce is a number used once in cryptographic communications. In blockchain, it is often used to ensure that each block is unique and to prevent replay attacks.",
        "what does a block contain?": "A block contains the following parameters: index, block_timestamp, previous_hash, nonce, hash, sender, receiver, amount, transaction_timestamp, transaction_id.",
        "what is a hash in blockchain?": "A hash is a fixed-length string of characters generated by a hash function. It uniquely represents the data in a block and ensures data integrity by making it nearly impossible to alter without detection.",
    }

    # Check for informative questions first
    if query in informative_responses:
        return informative_responses[query]

    # Check for 'block' and extract the index if present
    if 'block' in query:
        index_part = query.split('block')
        if len(index_part) > 1:
            try:
                index = int(index_part[1].strip())
            except ValueError:
                return "Invalid index provided. Please ensure you mention a valid block index."
        else:
            return "Invalid query. Please specify the block index."

        # Check for specific parameters in the query
        if 'sender' in query:
            parameter = 'sender'
        elif 'amount' in query:
            parameter = 'amount'
        elif 'hash' in query:
            parameter = 'hash'
        elif 'previous_hash' in query:
            parameter = 'previous_hash'
        elif 'transaction id' in query or 'transaction_id' in query:  # Recognizes both formats
            parameter = 'transaction_id'
        elif 'nonce' in query:
            parameter = 'nonce'
        elif 'transaction_timestamp' in query:
            parameter = 'transaction_timestamp'
        elif 'receiver' in query:
            parameter = 'receiver'
        else:
            return "Invalid query. Please ask about a specific parameter (e.g., sender, amount)."

        # Search the DataFrame based on the index and parameter
        try:
            row = df.loc[df['index'] == index]
        except KeyError:
            return f"No data found for index {index}"

        # Check if the parameter exists in the DataFrame
        if parameter in row.columns:
            if not row.empty:
                value = row[parameter].values[0]
                return f"The {parameter} of block {index} is {value}."
            else:
                return f"No data found for block {index}"
        else:
            return f"No information available for parameter '{parameter}'"

    # If the query doesn't mention 'block', return an invalid query message
    return "Invalid query format. Please specify the block index and the parameter you are interested in."

# Input section for Query Blockchain Data
if option == "Query Blockchain Data":
    st.subheader("Query Blockchain Data")
    
    # Sample questions to guide users
    st.write("Here are some sample questions you can ask:")
    st.write("1. Who is the sender of block 1?")
    st.write("2. What is the amount in block 1?")
    st.write("3. Give me the transaction ID of block 1.")
    st.write("4. What does a block represent?")
    
    # Create a text input for the user's query
    user_input = st.text_input("Enter your question:")

    # Query and display the result
    if user_input:
        response = query_model(user_input, df)
        st.write("Model's response:", response)

# Input section for Search Blockchain Data
if option == "Search Blockchain Data":
    st.subheader("Search Blockchain Data")
    columns = df.columns.tolist()
    selected_column = st.selectbox("Select a column to filter", columns)
    filter_value = st.text_input(f"Enter the value to search in '{selected_column}':")

    # Filter and display the DataFrame based on user input
    if filter_value:
        filtered_df = df[df[selected_column].astype(str).str.contains(filter_value, case=False, na=False)]
        if not filtered_df.empty:
            st.write(f"Showing results for {selected_column} containing '{filter_value}':")
            st.dataframe(filtered_df)
        else:
            st.write(f"No results found for {selected_column} containing '{filter_value}'")
