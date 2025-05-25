import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter

#Upload a PDF file
st.header("ZBOT")

with st.sidebar:
    st.title("Documents")
    file = st.file_uploader("Upload your document:", type="pdf")

#Extract the text

if file is not None:
    pdf_reader = PdfReader(file)
    text=""
    for page in pdf_reader.pages:
        text += page.extract_text()
        #st.write(text)

#Break into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n"],
        chunk_size=1000,
        chunk_overlap=150,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    #st.write(chunks)

#get user question
    user_question = st.text_input("Ask something")

#do similarity search
