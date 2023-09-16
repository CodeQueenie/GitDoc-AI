import os
import PyPDF2
import tiktoken
import streamlit as st
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS

load_dotenv()

tiktoken.encoding_for_model('gpt-3.5-turbo')
tokenizer = tiktoken.get_encoding('cl100k_base')

def tiktoken_len(text):
    tokens = tokenizer.encode(text, disallowed_special=())
    return len(tokens)

def process_md_file(md_file, path):
    with open(md_file, "r", encoding="utf-8") as md:
        md_content = md.read()
        text_splitter = get_text_splitter()
        chunks = text_splitter.create_documents([md_content], metadatas=[{"page": 1, "file": path}])
        return chunks

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

def get_text_splitter():
    chunk_size = st.session_state["chunk_size"] or 500
    chunk_overlap = st.session_state["chunk_overlap"] or 100
    return RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=tiktoken_len,
        separators=["\n\n", "\n", " ", ""]
    )

def process_folder(folder, branch):
    chunks = []
    for root, _, files in os.walk(folder):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            relative_path = os.path.relpath(file_path, folder)
            relative_path = st.session_state["document_url"] + "/blob/" + branch + '/' + relative_path
            
            if file_name.endswith(".md"):
                chunks.extend(process_md_file(file_path, relative_path))
            
            if file_name.endswith(".pdf"):
                chunks.extend(process_pdf_file(file_path, relative_path))

    return chunks


def create_vector(folder_path, branch = "main"):
    chunks = process_folder(folder_path, branch)
    openai_api_key = st.session_state.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key, disallowed_special=())
    vectorstore = FAISS.from_documents(chunks, embeddings)

    return vectorstore
