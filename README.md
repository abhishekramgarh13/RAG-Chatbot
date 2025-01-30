# RAG-Chatbot

## Overview
This project is a **Retrieval-Augmented Generation (RAG) Chatbot** using **Flask**, **FAISS**, **LangChain**, and **MySQL**. The chatbot retrieves relevant document chunks and generates responses using a language model.

## Installation & Setup

### 1. Create a Virtual Environment (Conda)
```sh
conda create --name rag_chatbot python=3.9 -y
conda activate rag_chatbot
```

### 2. Clone the Repository
```sh
git clone https://github.com/abhishekramgarh13/RAG-Chatbot.git
cd RAG-Chatbot
```

### 3. Install Dependencies
```sh
pip install -r requirements.txt
```

### 4. Set Environment Variables
Create a `.env` file in the project directory and add the following:
```ini
HF_TOKEN=your_huggingface_token
GROQ_API_KEY=your_groq_api_key
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=Abhishek
```

## Database Setup

### 1. Start MySQL Server
Ensure MySQL is running on your machine.

### 2. Create the Database & Table
Run the following command to create the required MySQL database and table:
```sh
python db.py
```

## Generate FAISS Vector Database
To generate the FAISS index, run:
```sh
python scrab.py
```

## Running the Flask Application
Start the chatbot API with:
```sh
python app.py
```
The API will be accessible at `http://127.0.0.1:5000/`

## Testing the Endpoints

### 1. Chat Endpoint
To test the `/chat` endpoint, send a POST request:
```sh
curl -X POST http://127.0.0.1:5000/chat \
     -H "Content-Type: application/json" \
     -d '{"query": "What are cyclical stocks?"}'
```

### 2. Chat History Endpoint
To retrieve chat history:
```sh
curl -X GET http://127.0.0.1:5000/history
```

### 3. Run Unit Tests
To run tests, execute:
```sh
pytest test_app.py -v
```

## License
This project is licensed under the MIT License.

