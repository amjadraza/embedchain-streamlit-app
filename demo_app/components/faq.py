# flake8: noqa
import streamlit as st


def faq():
    st.markdown(
        """
# FAQ
## What is embedchain?
embedchain is a framework to digest data from various sources, video, text, pdf etc and 
prepares the Chat-Bot 


## What Libraries are being use?
Basic Setup is using embedchain, streamlit and openai.
example:
youtube: "https://www.youtube.com/watch?v=3qHkcs3kG44"
pdf_file: "https://navalmanack.s3.amazonaws.com/Eric-Jorgenson_The-Almanack-of-Naval-Ravikant_Final.pdf"
web : "https://nav.al/feedback"

Question: What unique capacity does Naval argue humans possess when it comes to understanding explanations or concepts?

## How is the Data Ingestion Works?
Fill the Data Input form with URL of relevant Data and submit. Data is 
downloaded, chuncked and embeddings are stored in local db 

## Bot Response
Having Data Ingestion complete, users can ask the questions, relevant to data.

## Disclaimer?
This is a template App, when using with openai_api key, you will be charged a nominal fee depending
on number of prompts etc.

"""
    )
