import streamlit as st
from app.components.uploader import load_pdf
from app.components.sidebar import sidebar
import pickle
import os

def initialise():
    if 'vectorstore' not in st.session_state:
        st.session_state['vectorstore'] = None
    if 'document_url' not in st.session_state:
        st.session_state['document_url'] = None 

def main():
    st.set_page_config(page_title="Build knowledge", page_icon="🛠️")
    initialise()
    sidebar()
    st.header('🛠️ Build your knowledge base')

    if st.session_state['vectorstore'] is None:
        if st.session_state['document_url'] is None:
            st.session_state['document_url'] = st.text_input("Enter the documentation repo url")
        else:
            st.session_state['vectorstore'] = load_pdf()
            if st.session_state['vectorstore'] is not None:
                with open("vectorstore/uploaded.pkl", 'wb') as f:
                    pickle.dump(st.session_state['vectorstore'], f)
                with open("vectorstore/uploaded.pkl", "rb") as file:
                    st.download_button(
                        label="Download Vectorstore",
                        data=file,
                        file_name="Knowledge-base.pkl",
                        mime="application/octet-stream"
                    )
                    st.write("Knowledge base created!")
                    os.remove("vectorstore/uploaded.pkl")
    else:
        st.write("Knowledge base already created!")


if __name__ == "__main__":
    main()