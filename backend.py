from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.vectorstores import Pinecone
from pinecone import Pinecone as PineconeClient
from langchain.chains import RetrievalQA
import os



os.environ['OPENAI_API_KEY'] ="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"
os.environ['PINECONE_API_KEY'] ="pcsk_5Gmbmn_6txh6EaUAgtHbKdyAHG37p7TKdFgANFAQgTxuBLuWjmS7MvFyjasSpA7LcR273Y"
os.environ['PINECONE_API_ENV'] ="aws-starter"
PINECONE_API_KEY = os.environ['PINECONE_API_KEY']
PINECONE_API_ENV = os.environ['PINECONE_API_ENV']
pc = PineconeClient(
     api_key=PINECONE_API_KEY,
      environment=PINECONE_API_ENV
  )
index_name = "test"
embeddings = OpenAIEmbeddings()
llm = OpenAI()
uploaded_files = {}


def process_and_store_embeddings(file_path, file_id):
    """Processes the file, generates embeddings, and stores them in Pinecone."""
    loader = PyPDFDirectoryLoader("pdfs")
    data = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
    text_chunks = text_splitter.split_documents(data)

    docsearch = Pinecone.from_texts([t.page_content for t in text_chunks], embedding=embeddings, index_name=index_name)

    uploaded_files[file_id] = file_path  # Track the file
    return f"Uploaded and stored embeddings for {file_id}"

def delete_file_and_embeddings(file_id):
    """Deletes a file and its corresponding embeddings from Pinecone."""
    if file_id in uploaded_files:
        index = Pinecone.from_existing_index(index_name=index_name, embedding=embeddings)
        index.delete(id=file_id)  # Remove from Pinecone

        # Remove from local storage
        file_path = uploaded_files[file_id]
        if os.path.exists(file_path):
            os.remove(file_path)

        del uploaded_files[file_id]
        return f"Deleted {file_id} and its embeddings."
    
    return f"{file_id} not found."


def chat(query):
    """Handles chatbot interaction using embeddings."""
    docsearch = Pinecone.from_existing_index(index_name=index_name, embedding=embeddings)
    chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=docsearch.as_retriever())
    res = chain.invoke({"query": query})
    return res.get('result')