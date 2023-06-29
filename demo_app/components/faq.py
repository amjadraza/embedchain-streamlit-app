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
