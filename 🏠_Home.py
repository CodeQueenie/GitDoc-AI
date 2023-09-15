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
        - 📖 **Rich Documentation Access:** Instantly access detailed project documentation, READMEs, code snippets, and more.
        - 💬 **Interactive Chat:** Engage in dynamic conversations with GitDoc to find the information you need, ask questions, and get code-related insights.
        - 🔒 **Secure Access:** Your data privacy is our priority. GitDoc ensures a secure and seamless browsing experience.
        - 🧠 **AI-Powered Insights:** Powered by advanced Language Models, GitDoc provides intelligent code recommendations and context-aware responses.
        - 🚀 **Boost Your Development:** Speed up your coding workflow, troubleshoot issues, and stay up-to-date with the latest project changes.
        - 🌟 **Join the GitDoc Community:** Connect with fellow developers, share your expertise, and collaborate on projects within the GitDoc ecosystem.
        - 🌈 **User-Friendly Interface:** A clean, intuitive, and responsive interface ensures that your coding experience is smooth and enjoyable.

        Experience the future of GitHub documentation exploration with GitDoc - Where curiosity meets code! 🚀📚💬
    """
    )

if __name__ == "__main__":
    main()
