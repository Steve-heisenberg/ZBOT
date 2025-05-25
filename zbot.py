# Author: Stephan John
import streamlit as st
import os
import tempfile
from PyPDF2 import PdfReader
import pandas as pd
import docx
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain_community.chat_models import ChatOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# App UI
st.set_page_config(page_title="ZBOT", layout="wide")
st.header("🤖 ZBOT")

with st.sidebar:
    st.title("📂 Upload Your Document")
    uploaded_file = st.file_uploader("Upload a PDF, DOCX, TXT, CSV, or XLSX file", type=["pdf", "docx", "txt", "csv", "xlsx"])
    retry_button = st.button("Retry")

# Helper: Read text from various file types
@st.cache_data(show_spinner=False)
def extract_text(file, filetype):
    try:
        if filetype == "pdf":
            reader = PdfReader(file)
            return "\n".join([page.extract_text() or "" for page in reader.pages])

        elif filetype == "docx":
            doc = docx.Document(file)
            return "\n".join([para.text for para in doc.paragraphs])

        elif filetype == "txt":
            return file.read().decode("utf-8")

        elif filetype == "csv":
            df = pd.read_csv(file)
            return df.to_string(index=False)

        elif filetype == "xlsx":
            df = pd.read_excel(file)
            return df.to_string(index=False)

    except Exception as e:
        st.error(" Error reading file. Please check the format or content.")
        return None

# Main processing
if uploaded_file and not retry_button:
    file_type = uploaded_file.type.split("/")[-1] or uploaded_file.name.split(".")[-1]
    st.success(f" File '{uploaded_file.name}' uploaded successfully!")

    text = extract_text(uploaded_file, file_type)
    if not text or len(text.strip()) == 0:
        st.warning(" Could not extract any readable text from the file.")
    else:
        # Split text into chunks
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=150
        )
        chunks = splitter.split_text(text)

        try:
            # Validate API key
            if not OPENAI_API_KEY or not OPENAI_API_KEY.startswith("sk-"):
                raise ValueError("Invalid or missing API key")

            # Embeddings
            embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
            vector_store = FAISS.from_texts(chunks, embeddings)

            user_question = st.text_input(" Ask a question about your file")
            if user_question:
                with st.spinner("Analyzing..."):
                    matched_docs = vector_store.similarity_search(user_question)

                    llm = ChatOpenAI(
                        openai_api_key=OPENAI_API_KEY,
                        temperature=0,
                        max_tokens=1000,
                        model_name="gpt-3.5-turbo"
                    )

                    chain = load_qa_chain(llm, chain_type="stuff")
                    response = chain.run(input_documents=matched_docs, question=user_question)

                    st.markdown("### 💬 Answer")
                    st.success(response)

        except Exception as e:
            st.error("Something went wrong. Check your API key or try again later.")

elif retry_button:
    try:
        st.rerun()
    except AttributeError:
        st.experimental_rerun()

else:
    st.info("📄 Please upload a document to begin.")
