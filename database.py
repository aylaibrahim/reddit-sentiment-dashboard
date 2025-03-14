import mysql.connector

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "ucandoit!",
    "database": "reddit_sentiment"    
}

def connect():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    return conn, cursor

def insert_data(username, text):
    conn, cursor = connect()
    query = "INSERT INTO sentiment_data (username, text) VALUES (%s, %s)"
    values = (username, text)
    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()

def fetch_sentiment_data(username):
    conn, cursor = connect()
    query = "SELECT sentiment FROM sentiment_data WHERE username = %s"
    cursor.execute(query, (username,))
    sentiments = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return sentiments
    
