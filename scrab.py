from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import bs4
import os
from dotenv import load_dotenv
load_dotenv()
os.environ['HF_TOKEN'] = os.getenv('HF_TOKEN')


def load_documents(urls):
    """
    Loads web pages and extracts relevant content using BeautifulSoup filtering.
    
    :param urls: List of URLs to load
    :return: List of document objects
    """
    loader = WebBaseLoader(
        web_paths=urls,
        bs_kwargs=dict(parse_only=bs4.SoupStrainer(
            class_="comp mntl-sc-page mntl-block article-body-content"
        ))
    )
    return loader.load()

def clean_text(documents):
    """
    Cleans and extracts text content from documents.
    
    :param documents: List of loaded document objects
    :return: Concatenated cleaned text
    """
    return "\n\n".join(doc.page_content.strip() for doc in documents if doc.page_content)

def split_into_chunks(text, chunk_size=250, chunk_overlap=20):
    """
    Splits the text into smaller chunks using LangChain's RecursiveCharacterTextSplitter.
    
    :param text: The cleaned text to be split
    :param chunk_size: Maximum size of each chunk (characters)
    :param chunk_overlap: Overlap size to maintain context
    :return: List of text chunks
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )
    return text_splitter.split_text(text)

def embed_and_store(chunks, save_path="faiss_index"):
    """
    Embeds text chunks and stores them in a FAISS vector database.

    :param chunks: List of LangChain Document chunks
    :param save_path: Path to save FAISS index
    """
    # Load HuggingFace embeddings
    embeddings = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')

    # Create FAISS index from document embeddings
    db = FAISS.from_texts(chunks, embeddings)

    # Save FAISS index
    db.save_local(save_path)
    print(f"FAISS index saved to: {save_path}")

def main():
    urls = [
        "https://www.investopedia.com/types-of-stocks-5215684",
        "https://www.investopedia.com/meme-stock-5206762",
    ]
    
    # Load and process documents
    documents = load_documents(urls)
    cleaned_text = clean_text(documents)
    chunks = split_into_chunks(cleaned_text)
    embed_and_store(chunks,"faiss_index")
    

    

if __name__ == "__main__":
    main()
