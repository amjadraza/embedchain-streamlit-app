"""Python file to serve as the frontend"""
import sys
import os

sys.path.append(os.path.abspath('.'))

import streamlit as st
from streamlit_chat import message
from demo_app.components.sidebar import sidebar


def ingest_data(data_urls):

    naval_chat_bot.add("youtube_video", data_urls['youtube_video'])
    naval_chat_bot.add("pdf_file", data_urls['pdf_file'])
    naval_chat_bot.add("web_page", data_urls['web_page_1'])

    st.session_state["IS_BOT_READY"] = True
    # naval_chat_bot.add("web_page", data_urls['web_page_2'])

    # Embed Local Resources
    # naval_chat_bot.add_local("qna_pair", data_urls['pdf_file'])


def response_embedchain(query):
    """Logic for loading the chain you want to use should go here."""
    print(f'Calling response on: {query}')
    response = naval_chat_bot.query(query)
    print(response)
    return response

if __name__ == "__main__":

    st.set_page_config(
        page_title="Chat App: EmbedChain Demo",
        page_icon="📖",
        layout="wide",
        initial_sidebar_state="expanded", )
    st.header("📖 Chat App: EmbedChain Demo")
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
    sidebar()

    if "expander_state" not in st.session_state:
        st.session_state["expander_state"] = True

    def toggle_closed():
        st.session_state["expander_state"] = False

    with st.expander("Source Data Form", expanded = st.session_state["expander_state"]):
        form = st.form(key="source-data", clear_on_submit=False)
        youtube_video = form.text_input("Enter URL youtube video",
                                        placeholder="https://www.youtube.com/watch?v=3qHkcs3kG44")
        pdf_file = form.text_input("Enter URL: pdf",
                                   placeholder="https://navalmanack.s3.amazonaws.com/Eric-Jorgenson_The-Almanack-of-Naval-Ravikant_Final.pdf")
        web_page_1 = form.text_input("Enter URL: web page",
                                     placeholder="https://nav.al/feedback")
        submit_data_form = form.form_submit_button("Submit", on_click=toggle_closed)

    data_dict = {'youtube_video': youtube_video,
                 'pdf_file': pdf_file,
                 'web_page_1': web_page_1}

    if submit_data_form:
        st.session_state["submit_data_form"] = True

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
            if "generated" not in st.session_state:
                st.session_state["generated"] = []

            if "past" not in st.session_state:
                st.session_state["past"] = []

            with st.form("chat_input", clear_on_submit=True):
                a, b = st.columns([4, 1])
                user_input = a.text_input(
                    label="Your message:",
                    placeholder="What would you like to say?",
                    label_visibility="collapsed",
                )
                b.form_submit_button("Send", use_container_width=True)

            print(user_input)

            for idx, msg in enumerate(st.session_state.messages):
                message(msg["content"], is_user=msg["role"] == "user", key=idx)

            if user_input:
                st.session_state.messages.append({"role": "user", "content": user_input})
                message(user_input, is_user=True)

                with st.spinner('CHAT-BOT is at Work ...'):
                    response = response_embedchain(user_input)
                    # st.success('Done')
                st.session_state.messages.append({"role": "assistant", "content": response})
                message(response)

