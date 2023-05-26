## Automated website scrapper and a chatbot
### Decription
This is a automated website scrapper and a chatbot powered with OPENAI's LLM based on langchain.<br>
First we scrape data using langchain siteloader. Then index and store the text data in the form of word embeddings for OPENAI in a vectorDB, in this case ChromaDB. We can then use this DataBase along with OPENAI LLM to answer questions based on the data. All of this is done with the help of langchain chains/agents. The LLM and vectorDB can be swapped out as per requirements.  

### Structure

#### data-ingestion.py

This is the script for initializing the langchain siteloader which is a document loader that scrapes website based on the provided sitemap-url and then will index the documents, create the embddings and store them in a persistant chromadb database. This is vector database for storing embeddings and efficient retrival using indices that it creates.<br>

#### main.py

This will run a streamlit app where we can ask the chatbot question<br>
command to run the main.py: streamlit run main.py

You will also need to provide a OpenAI API Key in a .env file in the format: OPEN_AI_KEY=<your-key>
