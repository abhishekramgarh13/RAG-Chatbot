from flask import Flask, request, jsonify, render_template
import mysql.connector
from datetime import datetime
from langchain_community.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
os.environ['HF_TOKEN'] = os.getenv('HF_TOKEN')

groq_api_key = os.getenv("GROQ_API_KEY")
host= os.getenv("DB_HOST")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")



app = Flask(__name__, template_folder="templates", static_folder="static")

# MySQL Database Configuration
DB_CONFIG = {
    "host": host,
    "user": user,
    "password": password,
    "database": "chatdb"
}

# Load FAISS Index
embeddings = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')
faiss_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
llm = ChatGroq(groq_api_key = groq_api_key,model_name="gemma2-9b-It")

# Function to execute MySQL queries
def execute_query(query, values=None, fetch=False):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, values or ())
    
    result = cursor.fetchall() if fetch else None
    conn.commit()
    
    cursor.close()
    conn.close()
    return result

# Store message in MySQL
def store_message(role, content):
    query = "INSERT INTO chat_history (role, content) VALUES (%s, %s)"
    execute_query(query, (role, content))

# Query FAISS and return top chunks
def get_relevant_chunks(query, k=5):
    embedded_query = embeddings.embed_query(query)
    results = faiss_db.similarity_search_by_vector(embedded_query,k=k)
    return [doc.page_content for doc in results]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_query = data.get("query")

    if not user_query:
        return jsonify({"error": "Query is required"}), 400

    store_message("user", user_query)
    
    retrieved_chunks = get_relevant_chunks(user_query)
    context = "\n\n".join(retrieved_chunks)
    messages = [
        ("system", "Use the following context to answer the user's query."),
        ("human", f"Context: {context}\n\nQuestion: {user_query}")
    ]
    
    response = llm.invoke(messages).content
    
    store_message("system", response)
    return jsonify({"answer": response, "retrieved_chunks": retrieved_chunks})

@app.route('/history', methods=['GET'])
def get_history():
    query = "SELECT id, timestamp, role, content FROM chat_history ORDER BY timestamp DESC"
    history = execute_query(query, fetch=True)
    return jsonify(history)

if __name__ == '__main__':
    app.run()

