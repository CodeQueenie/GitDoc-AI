import streamlit as st
from dotenv import load_dotenv
import os

def setup_langsmith():
    load_dotenv()
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
    os.environ["LANGCHAIN_API_KEY"] =  st.secrets["LANGCHAIN_API_KEY"] if "LANGCHAIN_API_KEY" in st.secrets else os.environ["LANGCHAIN_API_KEY"]
    os.environ["LANGCHAIN_PROJECT"] = "GitDoc-AI"

def main():
    setup_langsmith()
    st.set_page_config(
        page_title="Hello",
        page_icon="👋",
    )
    st.write("# 🚀 GitDoc AI 📚")
    st.markdown(
    """ 
        > GitDoc is your ultimate GitHub Documentation Explorer! It's your trusty sidekick for navigating through the vast world of open-source projects, making code exploration and documentation retrieval a breeze. 🚀
            
        ## Key Features
        - 📖 **Rich Documentation Access:** Instantly access project documentation, READMEs, code snippets, and more.
        - 🌟 **Interactive Chat:** Engage with GitDoc for info, questions, and code insights.
        - 🧠 **AI-Powered Insights:** Intelligent code tips with advanced Language Models.
        - 🚀 **Boost Your Development:** Speed up coding, troubleshoot, and stay updated.
        - 🌈 **User-Friendly Interface:** Enjoy a smooth coding experience.

        ## Setup your own GitDoc AI?
        1. 📝 Create a knowledge base at [Build Knowledge](https://gitdoc-ai.streamlit.app/Build_Knowledge)
            - Enter the GitHub repository URL
            - Download and upload github repo as zip.
        2. 🤖 Connect a chatbot at [Docs Chat](https://gitdoc-ai.streamlit.app/Docs_Chat)
            - Upload your create knowledge base file.
            - Start chatting with your own GitDoc AI.

        Experience the future of GitHub documentation exploration with GitDoc - Where curiosity meets code! 🚀📚💬
    """
    )

if __name__ == "__main__":
    main()
