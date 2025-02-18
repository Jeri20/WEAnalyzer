# backend/db.py
import psycopg2
import json
import os
# Function to store analysis data into the database
def store_in_db(title: str, entities: list, search_intent: str, embedding: list):
    # Database connection (ensure to configure your credentials properly)
    conn = psycopg2.connect(
        host='localhost',
        database='WEAnalyzer',
        user='postgres',
        password=os.getenv('pas')
    )
    
    # Prepare and execute the insert query
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO website_analysis (title, entities, search_intent, embedding)
        VALUES (%s, %s, %s, %s)
    """, (
        title,
        json.dumps(entities),  # Store entities as a JSON array
        search_intent,
        json.dumps(embedding)  # Store the embedding as JSON
    ))
    
    # Commit the transaction and close the connection
    conn.commit()
    cursor.close()
    conn.close()
