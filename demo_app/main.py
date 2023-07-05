"""Python file to serve as the frontend"""
import sys
import os
import time

sys.path.append(os.path.abspath('.'))

import streamlit as st
from demo_app.components.sidebar import sidebar


def ingest_data(data_urls):

    for k, v in data_urls.items():
        print(f"Ingesting:{v}")
        naval_chat_bot.add(k, v)
    # naval_chat_bot.add("pdf_file", data_urls['pdf_file'])
    # naval_chat_bot.add("web_page", data_urls['web_page_1'])

    st.session_state["IS_BOT_READY"] = True
    # naval_chat_bot.add("web_page", data_urls['web_page_2'])

    # Embed Local Resources
    # naval_chat_bot.add_local("qna_pair", data_urls['pdf_file'])


def response_embedchain(query):
    """Logic for loading the chain you want to use should go here."""
    print(f'Calling response on: {query}')
    response = naval_chat_bot.query(query)
    return response


def provide_data_urls():
    with st.expander("Source Data Form", expanded=st.session_state["expander_state"]):
        form = st.form(key="source-data", clear_on_submit=False)

        youtube_video = form.text_input("Enter URL youtube video",
                                        value="https://www.youtube.com/watch?v=3qHkcs3kG44")
        pdf_file = form.text_input("Enter URL: pdf",
                                   value="https://navalmanack.s3.amazonaws.com/Eric-Jorgenson_The-Almanack-of-Naval-Ravikant_Final.pdf")
        web_page_link = form.text_input("Enter URL: web page",
                                     value="https://nav.al/agi")
        submit_data_form = form.form_submit_button("Submit", on_click=toggle_closed)

        if submit_data_form:
            st.session_state["submit_data_form"] = True

    data_dict = {'youtube_video': youtube_video,
                 'pdf_file': pdf_file,
                 'web_page': web_page_link}

    # data_dict = {'pdf_file': pdf_file,
    #              'web_page': web_page_link}
    return data_dict


def toggle_closed():
    st.session_state["expander_state"] = False


if __name__ == "__main__":

    st.set_page_config(
        page_title="Chat App: EmbedChain Demo",
        page_icon="📖",
        layout="wide",
        initial_sidebar_state="expanded", )
    st.header("📖 Chat App: EmbedChain Demo")

    sidebar()

    if "expander_state" not in st.session_state:
        st.session_state["expander_state"] = True

    data_dict = provide_data_urls()

    if not st.session_state.get("OPENAI_API_CONFIGURED") or not st.session_state.get("submit_data_form"):
        st.error("Please configure your API Keys! and Submit the form")

    if st.session_state.get("OPENAI_API_CONFIGURED") and st.session_state.get("submit_data_form"):
        st.markdown("Main App: Started")
        from embedchain import App as ecApp

        naval_chat_bot = ecApp()
        # ingesting data
        if not st.session_state.get("IS_BOT_READY"):
            with st.spinner('Wait for DATA Ingestion'):
                ingest_data(data_dict)
            st.success('Data Ingestion Done!')

        if st.session_state.get("IS_BOT_READY"):

            if "messages" not in st.session_state:
                st.session_state["messages"] = [
                    {"role": "assistant", "content": "How can I help you?"}]

            # Display chat messages from history on app rerun
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            if user_input := st.chat_input("What is your question?"):
                # Add user message to chat history
                st.session_state.messages.append({"role": "user", "content": user_input})
                # Display user message in chat message container
                with st.chat_message("user"):
                    st.markdown(user_input)
                # Display assistant response in chat message container
                with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    full_response = ""

                with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    full_response = ""

                    with st.spinner('CHAT-BOT is at Work ...'):
                        assistant_response = response_embedchain(user_input)
                    # Simulate stream of response with milliseconds delay
                    for chunk in assistant_response.split():
                        full_response += chunk + " "
                        time.sleep(0.05)
                        # Add a blinking cursor to simulate typing
                        message_placeholder.markdown(full_response + "▌")
                    message_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
