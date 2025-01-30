import mysql.connector

def create_database():
    """
    Creates the MySQL database if it does not exist.
    """
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Abhishek"
    )
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS chatdb;")
    cursor.close()
    conn.close()
    print("Database 'chatdb' created successfully!")

def create_table():
    """
    Creates the chat_history table inside chatdb.
    """
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Abhishek",
        database="chatdb"
    )
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INT AUTO_INCREMENT PRIMARY KEY,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            role ENUM('user', 'system') NOT NULL,
            content TEXT NOT NULL
        );
    """)
    cursor.close()
    conn.close()
    print("Table 'chat_history' created successfully!")

if __name__ == "__main__":
    create_database()
    create_table()