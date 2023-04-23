## this is the project for instalily 2nd round interview

### Structure

#### data-ingestion.py

This is the script for initializing the langchain siteloader which is a document loader that scrapes website based on the provided sitemap-url and then will index the documents, create the embddings and store them in a persistant chromadb database. This is vector database for storing embeddings and efficient retrival using indices that it creates.<br>

#### main.py

This will run a streamlit app where we can ask the chatbot question
command to run the main.py: streamlit run main.py

You will also need to provide a OpenAI API Key in a .env file in the format: OPEN_AI_KEY=<your-key>
