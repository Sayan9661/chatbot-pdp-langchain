from langchain.document_loaders.sitemap import SitemapLoader
import chromadb
import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from dotenv import load_dotenv
import logging
import re

load_dotenv()
logging.basicConfig(level=logging.DEBUG)

os.environ["OPENAI_API_KEY"] = os.getenv("OPEN_AI_KEY")

ABS_PATH = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(ABS_PATH, "db1")


def get_documents():
    # import nest_asyncio
    # nest_asyncio.apply()
    loader = SitemapLoader(
        web_path="Enter the sitemap xml here"
    )

    loader.requests_per_second = 2
    documents = loader.load()
    return documents
    # text_splitter = CharacterTextSplitter(chunk_size=5000, chunk_overlap=0)
    # texts = text_splitter.split_documents(documents)
    # embeddings = OpenAIEmbeddings(openai_api_key=os.environ['OPENAI_API_KEY'])


def init_chromadb():

    client_settings = chromadb.config.Settings(
        chroma_db_impl="duckdb+parquet",
        persist_directory=DB_DIR,
        anonymized_telemetry=False
    )
    embeddings = OpenAIEmbeddings()

    vectorstore = Chroma(
        collection_name="langchain_store",
        embedding_function=embeddings,
        client_settings=client_settings,
        persist_directory=DB_DIR,
    )

    vectorstore.add_documents(documents=get_documents(), embedding=embeddings)
    vectorstore.persist()


def query_chromadb():
    client_settings = chromadb.config.Settings(
        chroma_db_impl="duckdb+parquet",
        persist_directory=DB_DIR,
        anonymized_telemetry=False
    )

    embeddings = OpenAIEmbeddings()

    vectorstore = Chroma(
        collection_name="langchain_store",
        embedding_function=embeddings,
        client_settings=client_settings,
        persist_directory=DB_DIR,
    )
    result = vectorstore.similarity_search_with_score(query="DRESS", k=4)
    print(result)


def main():
    init_chromadb()
    # query_chromadb()


if __name__ == '__main__':
    main()
