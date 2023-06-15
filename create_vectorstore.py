from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import UnstructuredMarkdownLoader
from langchain.vectorstores import FAISS
import glob
from dotenv import load_dotenv

load_dotenv()

docs = []
schema_files = glob.glob("schemas/*.md")
for schema_file in schema_files:
    loader = UnstructuredMarkdownLoader(schema_file)
    sub_docs = loader.load()
    docs.extend(sub_docs)

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
texts = text_splitter.split_documents(docs)

embeddings = OpenAIEmbeddings()
vector_store = FAISS.from_documents(texts, embeddings)
vector_store.save_local("faiss_index")

# Load vector_store from local copy
vector_store = FAISS.load_local("faiss_index", embeddings)

# Usage:
# from langchain.chains import RetrievalQA
# qa = RetrievalQA.from_chain_type(
#         llm=OpenAI(), chain_type="stuff", retriever=vector_store.as_retriever()
#     )
# res = qa.run("Prompt")
