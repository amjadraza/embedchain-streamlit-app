import streamlit as st
import os

from demo_app.components.faq import faq

def set_open_api_key(api_key: str):
    st.session_state["OPENAI_API_KEY"] = api_key
    os.environ["OPENAI_API_KEY"] = api_key
    st.session_state["OPENAI_API_CONFIGURED"] = True
    print('OPENAI API key is Configured Successfully!')


def sidebar():
    with st.sidebar:
        st.markdown(
            "## How to use\n"
            "1. Enter your [OpenAI API key](https://platform.openai.com/account/api-keys) below🔑\n"  # noqa: E501
        )
        open_api_key_input = st.text_input(
            "Openai API Key",
            type="password",
            placeholder="Paste your API key here (sk-...)",
            help="You can get your API key from https://platform.openai.com/account/api-keys.",  # noqa: E501
            value=st.session_state.get("OPEN_API_KEY", ""),
        )

        if open_api_key_input:
            set_open_api_key(open_api_key_input)

        if not st.session_state.get("OPENAI_API_CONFIGURED"):
            st.error("Please configure your Open API key!")
        else:
            st.markdown("Open API Key Configured!")

        st.markdown("---")
        st.markdown("# About")
        st.markdown(
            "📖 This App is template of embedchain-streamlit-app example"
        )
        st.markdown("Made by [DR. AMJAD RAZA](https://www.linkedin.com/in/amjadraza/)")
        st.markdown("embedchain: https://github.com/embedchain/embedchain")
        st.markdown("---")

        faq()
