import os
import PyPDF2
import tiktoken
import pickle
import streamlit as st
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS

# Load environment variables from a .env file if needed
load_dotenv()

# Set up the tokenizer for the model
tiktoken.encoding_for_model('gpt-3.5-turbo')
tokenizer = tiktoken.get_encoding('cl100k_base')

# Create the length function for token counting
def tiktoken_len(text):
    tokens = tokenizer.encode(text, disallowed_special=())
    return len(tokens)

# Function to process a Markdown file and split it into chunks
def process_md_file(md_file, path):
    with open(md_file, "r", encoding="utf-8") as md:
        md_content = md.read()
        text_splitter = get_text_splitter()
        chunks = text_splitter.create_documents([md_content], metadatas=[{"page": 1, "file": path}])
        return chunks

# Function to process a PDF file and split it into chunks
def process_pdf_file(pdf_file_path, relative_path):
    pdfFileObj = open(pdf_file_path, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    num_pages = pdfReader.numPages
    chunks = []

    for i in range(num_pages):
        pageObj = pdfReader.getPage(i)
        text = pageObj.extractText()
        text_splitter = get_text_splitter()
        chunks.extend(text_splitter.create_documents([text], metadatas=[{"page": i, "file": relative_path}]))

    return chunks

# Function to create a text splitter with specific parameters
def get_text_splitter():
    chunk_size = st.session_state["chunk_size"] or 500
    chunk_overlap = st.session_state["chunk_overlap"] or 100
    return RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=tiktoken_len,
        separators=["\n\n", "\n", " ", ""]
    )

# Function to process all files in a folder and split them into chunks
def process_folder(folder):
    chunks = []
    for root, _, files in os.walk(folder):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            relative_path = os.path.relpath(file_path, folder)
            if st.session_state["document_url"]:
                relative_path = st.session_state["document_url"] + "/tree/main/" + relative_path
            
            if file_name.endswith(".md"):
                chunks.extend(process_md_file(file_path, relative_path))
            
            if file_name.endswith(".pdf"):
                chunks.extend(process_pdf_file(file_path, relative_path))

    return chunks


def create_vector(folder_path = "docs/content"):
    chunks = process_folder(folder_path)
    openai_api_key = st.session_state.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key, disallowed_special=())
    vectorstore = FAISS.from_documents(chunks, embeddings)

    return vectorstore

if __name__ == "__main__":
    vectorstore_path = "vectorstore/doc.pkl"
    vectorstore = create_vector()

    with open(vectorstore_path, 'wb') as f:
        pickle.dump(vectorstore, f)