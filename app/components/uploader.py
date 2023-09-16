import streamlit as st

def load_pdf():
    col1, col2 = st.columns(2)
    with col1:
        st.slider('Chunk Size', min_value=100, max_value=2000, value=500, key="chunk_size")
    with col2:
        st.slider('Chunk Overlap', min_value=0, max_value=500, value=100, key="chunk_overlap")

    uploaded_file = st.file_uploader("Upload PDF files", type=["zip"])
    if uploaded_file is not None:
        return uploaded_file