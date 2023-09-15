import zipfile
import os
import streamlit as st
from load_knowledge import create_vector

def unzip_file(zip_file):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        unzip_dir = 'unzipped_files'
        zip_ref.extractall(unzip_dir)
        return unzip_dir

def load_pdf():
    col1, col2 = st.columns(2)
    with col1:
        st.slider('Chunk Size', min_value=100, max_value=2000, value=500, key="chunk_size")
    with col2:
        st.slider('Chunk Overlap', min_value=0, max_value=500, value=100, key="chunk_overlap")

    uploaded_file = st.file_uploader("Upload PDF files", type=["zip"])
    
    if uploaded_file is not None:
        unzip_path = unzip_file(uploaded_file)
        vectorstore = create_vector(unzip_path)
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