import os
import base64
import requests
import logging
import json
import datetime
import pandas as pd
import streamlit as st
import ollama 

# Streamlit app UI
st.title("Trading App")

assets = st.selectbox("Select Asset for Balance", assets_list)

if st.button("Get Balance"):
    # If "ALL" is selected, pass an empty string to get all balances
    if assets == "ALL":
        balance_list = luno_get_balance.get_balance("")
    else:
        balance_list = luno_get_balance.get_balance(assets)
    
    # Display the balance
    if balance_list:
        st.write("Balance List:")
        # Display using pandas
        
        balance_df = pd.DataFrame(balance_list)
        st.dataframe(balance_df)
        #st.json(balance_list)
    else:
        st.write("No balance information available.")


# Button for getting fee info
st.button("Get Fee Info", on_click=luno_get_fee_info.get_fee_info)

# Select account ID using a dropdown
id = st.selectbox("Select Account ID", account_ids)

# Use lambda function to pass 'id' as argument to 'get_transactions'
st.button(f"Get Transactions for {id}", on_click=lambda: luno_get_transactions.get_transactions(id))

# Uncomment the following line if needed for order book
# st.button("Get Order Book", on_click=luno_get_order_book.get_order_book)


# LLM Model
st.markdown("## LLM Model") 
model = OllamaFunctions(
    model="phi3", 
    keep_alive=-1,
    format="json"
    )

# Text Input
st.markdown("## Text Input")
text_input = st.text_input("Enter text", "")

# LLM Text output
st.markdown("## LLM Text Output")
st.text(model.predict(text_input))
