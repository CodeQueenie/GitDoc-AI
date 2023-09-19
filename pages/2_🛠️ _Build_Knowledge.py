import streamlit as st
from app.components.uploader import load_docs
from app.components.sidebar import sidebar
from app.utils.load_knowledge import create_vector
import pickle
import zipfile
import os

def initialise():
    if 'vectorstore' not in st.session_state:
        st.session_state['vectorstore'] = None
    if 'document_url' not in st.session_state:
        st.session_state['document_url'] = None

def unzip_file(zip_file):
    # get the file name without extension
    file_name = os.path.splitext(zip_file.name)[0]
    branch = file_name.split('-')[-1]

    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        unzip_dir = 'unzipped_files'
        zip_ref.extractall(unzip_dir)
        return unzip_dir + '/' + file_name, branch

def create_vectorstore(uploaded_file):
    if uploaded_file is not None:
        unzip_path, branch = unzip_file(uploaded_file)
        vectorstore = create_vector(unzip_path, branch)
        try:
            os.remove(unzip_path)
        except:
            print("Error while deleting directory ", unzip_path)
            # remove every file in the directory
            for root, dirs, files in os.walk(unzip_path):
                for file in files:
                    os.remove(os.path.join(root, file))
            pass

        return vectorstore


def main():
    st.set_page_config(page_title="Build knowledge", page_icon="🛠️")
    initialise()
    sidebar(is_model=False)
    st.header('🛠️ Build your knowledge base')

    if st.session_state['vectorstore'] is None:
        with st.form("my_form"):
            st.write("""
             1. Get the documentation repo url which is used for returning source links.
             2. Download the code as a zip file, We will use only the pdf and md files for knowledge base creation.
             """)
            if st.session_state['vectorstore'] is None:
                document_url = st.text_input(
                "Enter the documentation repo url",
                placeholder="Example: https://github.com/streamlit/docs")
                uploaded_file = load_docs()

                submitted = st.form_submit_button("Create knowledge base")
                if submitted and uploaded_file is not None and document_url != "":
                    st.session_state['document_url'] = document_url
                    st.session_state['vectorstore'] = create_vectorstore(uploaded_file)
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