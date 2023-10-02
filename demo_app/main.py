import sys
import os
import time

sys.path.append(os.path.abspath('.'))

import streamlit as st
# Assuming this import is correct
# from demo_app.components.sidebar import sidebar
from components.sidebar import sidebar
# Initialize session state variables here
if 'form_submitted' not in st.session_state:
    st.session_state['form_submitted'] = False

def ingest_data_dynamic(n):
    print(f'Number of Data Sources are {n}')
    for r in range(n):
        url_ = st.session_state.get(f"value_{r}")
        loader_type = st.session_state.get(f"loader_type_value_{r}")
        print(f"Ingestion {r+1}/{n}: {url_} with loader type {loader_type}")
        naval_chat_bot.add(url_, loader_type)
    
    st.session_state["IS_BOT_READY"] = True

def response_embedchain(query):
    print(f'Calling response on: {query}')
    response = naval_chat_bot.query(query)
    return response

def add_data_form(r):
    st.session_state[f"url_{r}"] = [st.session_state.get(f"value_{r}")]
    st.session_state[f"loader_type_{r}"] = [st.session_state.get(f"loader_type_value_{r}")]
    print(st.session_state.get(f"{r}"))

def add_form_row(row):
    data_form = st.form(key=f'{row}-Form')
    with data_form:
        data_columns = st.columns(2)
        with data_columns[0]:
            loader_type = st.selectbox(
                f"Select Loader Type: {row}",
                ["youtube_video", "pdf_file", "web_page", "qna_pair", "text"],
                key=f"loader_type_value_{row}"
            )

        with data_columns[1]:
            st.text_input(
                f"Enter Doc URL: {row}",
                value="https://www.youtube.com/watch?v=3qHkcs3kG44",
                key=f"value_{row}"
            )
        
        st.form_submit_button(on_click=add_data_form(row))

def provide_data_dynamic():
    with st.expander("Sources Data Form", expanded=st.session_state["expander_state"]):
        num_data_sources = st.slider('Number of Data Sources', min_value=1, max_value=10)
        for r in range(num_data_sources):
            add_form_row(r)
        submit_data_form = st.button("Submit Data", on_click=toggle_closed)
        if submit_data_form:
            st.session_state["submit_data_form"] = True
        return num_data_sources

def toggle_closed():
    st.session_state["expander_state"] = False

if __name__ == "__main__":
    st.set_page_config(
        page_title="💂‍♂️: EmbedChain Demo",
        page_icon="💂‍♂️",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.header("📖 Private Knowledge Store: EmbedChain Demo")
    
    # Commented out for the sake of example
    sidebar()

    if "expander_state" not in st.session_state:
        st.session_state["expander_state"] = True

    num_data_sources = provide_data_dynamic()

    if not st.session_state.get("OPENAI_API_CONFIGURED"):
        st.error("Please configure your API Keys!")

    if not st.session_state.get("submit_data_form"):
        st.error("Please Submit the Data Form")

    if st.session_state.get("OPENAI_API_CONFIGURED") and st.session_state.get("submit_data_form"):
        st.markdown("Main App: Started")
        from embedchain import App as ecApp  # Import your actual App class here
        naval_chat_bot = ecApp()

        if not st.session_state.get("IS_BOT_READY"):
            with st.spinner('Wait for DATA Ingestion'):
                ingest_data_dynamic(num_data_sources)
            st.success('Data Ingestion Done!')

        if st.session_state.get("IS_BOT_READY"):
            if "messages" not in st.session_state:
                st.session_state["messages"] = [
                    {"role": "assistant", "content": "How can I help you?"}
                ]

            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            if user_input := st.chat_input("What is your question?"):
                st.session_state.messages.append({"role": "user", "content": user_input})
                with st.chat_message("user"):
                    st.markdown(user_input)
                with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    full_response = ""
                with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    full_response = ""

                    with st.spinner('CHAT-BOT is at Work ...'):
                        assistant_response = response_embedchain(user_input)
                    for chunk in assistant_response.split():
                        full_response += chunk + " "
                        time.sleep(0.05)
                        message_placeholder.markdown(full_response + "▌")
                    message_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})


