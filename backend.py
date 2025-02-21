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
embeddings = OpenAIEmbeddings()
index_name = "test"
# Dictionary to keep track of file embeddings
uploaded_files = {}
loader = PyPDFDirectoryLoader("pdfs")
data = loader.load()

llm = OpenAI()
PINECONE_API_KEY = os.environ['PINECONE_API_KEY']
PINECONE_API_ENV = os.environ['PINECONE_API_ENV']

text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
text_chunks = text_splitter.split_documents(data)

pc = PineconeClient(
     api_key=PINECONE_API_KEY,
      environment=PINECONE_API_ENV
  )

docsearch = Pinecone.from_texts([t.page_content for t in text_chunks], embedding=embeddings, index_name=index_name)


def chat(query):
    docsearch = Pinecone.from_existing_index(index_name=index_name, embedding=embeddings)
    chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=docsearch.as_retriever())
    res = chain.invoke({"query": query})
    return res.get('result')

if __name__ == "__main__":
    query = input("enter your query")
    response=chat(query)
    print(response)