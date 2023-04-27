import streamlit as st
from dotenv import load_dotenv
import os
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
import logging
import chromadb
load_dotenv()
logging.basicConfig(level=logging.DEBUG)

os.environ["OPENAI_API_KEY"] = os.getenv("OPEN_AI_KEY")
ABS_PATH = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(ABS_PATH, "db1")


def query_chromadb():
    client_settings = chromadb.config.Settings(
        chroma_db_impl="duckdb+parquet",
        persist_directory=DB_DIR,
        anonymized_telemetry=False
    )

    embeddings = OpenAIEmbeddings(openai_api_key=os.environ['OPENAI_API_KEY'])

    vectorstore = Chroma(
        collection_name="langchain_store",
        embedding_function=embeddings,
        client_settings=client_settings,
        persist_directory=DB_DIR,
    )
    return vectorstore


def load_chain():
    vectordb = query_chromadb()
    chain = RetrievalQAWithSourcesChain.from_chain_type(
        ChatOpenAI(temperature=0),
        chain_type="stuff",
        retriever=vectordb.as_retriever(),
        reduce_k_below_max_tokens=True
    )
    return chain


def get_prompt():
    prompt = st.text_input(label="",
                           placeholder="Enter the prompt", value="")
    return prompt


st.set_page_config(page_title="Hello World", page_icon=":robot:",
                   layout="centered", initial_sidebar_state="expanded")


with st.container():
    left, right = st.columns(2)
    with left:
        st.header("Product chat bot")
        st.write(
            "Hi, I am a chat bot that can answer questions about products from jcrew.com :wave:")
    with right:
        st.image("chatbot.png", width=300)


with st.container():
    st.write('---')
    st.markdown("## Please enter the your question below")
    input_text = get_prompt()
    st.write('---')

    if input_text:
        st.write(f'Your question: {input_text}')
        chain = load_chain()
        response=chain({"question": input_text}, return_only_outputs=True)
        st.write("chatbot's response:")
        st.write(response["answer"])
        st.write("chatbot's source for this answer:")
        st.write(response["sources"])
