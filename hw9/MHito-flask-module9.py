#import libraries and modules
from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
import psycopg2
from psycopg2 import OperationalError

app = Flask(__name__)

#in-memory store for scraped data
# Structure: { topic: { "topic": ..., "title": ..., "content": ..., "num_links": ... } }
data_store = {}

#PostgreSQL connection parameters
load_dotenv()  # Load variables from .env file

PG_HOST = os.getenv('PG_HOST')
PG_PORT = os.getenv('PG_PORT')
PG_DBNAME = os.getenv('PG_DBNAME')
PG_USER = os.getenv('PG_USER')
PG_PASSWORD = os.getenv('PG_PASSWORD')

def get_db_connection():
    """Establish a PostgreSQL database connection"""
    try:
        conn = psycopg2.connect(
            host=PG_HOST,
            port=PG_PORT,
            dbname=PG_DBNAME,
            user=PG_USER,
            password=PG_PASSWORD)
        return conn
    except OperationalError as e:
        print("Error connecting to PostgreSQL:", e)
        return None

def init_db():
    """Initialize db and create schema and table if they do not exist"""
    conn = get_db_connection()
    if conn is None:
        return "Connection error"
    cur = conn.cursor()
    #create schema if it does not exist
    cur.execute("CREATE SCHEMA IF NOT EXISTS wiki;")
    #create table if it does not exist
    create_table_query = """
    CREATE TABLE IF NOT EXISTS wiki.wikipedia_data (
        topic TEXT PRIMARY KEY,
        title TEXT,
        content TEXT,
        num_links INTEGER);
    """
    cur.execute(create_table_query)
    conn.commit()
    cur.close()
    conn.close()

@app.route('/scrape', methods=['POST'])
def scrape_wikipedia():
    """
    POST endpoint that accepts JSON: { "topic": "Data_engineering" }
    Scrapes the Wikipedia page for that topic and extracts:
    - Page title
    - First 100 characters of the opening paragraph
    - Number of links on the page
    Saves the data in an in-memory store and returns it as JSON
    """
    data = request.get_json()
    if not data or "topic" not in data:
        return jsonify({"error": "JSON must contain 'topic' field"}), 400

    topic = data["topic"]
    url = f"https://en.wikipedia.org/wiki/{topic}"
    
    try:
        resp = requests.get(url)
        resp.raise_for_status()
    except requests.RequestException as e:
        return jsonify({"error": f"Error fetching page: {str(e)}"}), 500

    soup = BeautifulSoup(resp.text, 'html.parser')
    
    #extract the page title using the <title> tag
    page_title = soup.title.string if soup.title else "No title found"
    
    #find the first paragraph with non-empty text using the <p> tag 
    paragraph = ""
    for p in soup.find_all('p'):
        text = p.get_text(strip=True)
        if text:
            paragraph = text
            break
    opening_paragraph = paragraph[:100]  # first 100 characters
    
    #count the number of links on the page using the <a> tags
    links = soup.find_all('a')
    num_links = len(links)

    #prepare the record
    record = {
        "topic": topic,
        "title": page_title,
        "content": opening_paragraph,
        "num_links": num_links}
    #save to in-memory store
    data_store[topic] = record

    return jsonify(record), 200

@app.route('/delete', methods=['DELETE'])
def delete_topic():
    """
    DELETE endpoint that accepts JSON: { "topic": "Data_engineering" }
    Deletes the corresponding record from the in-memory store
    """
    data = request.get_json()
    if not data or "topic" not in data:
        return jsonify({"error": "JSON must contain 'topic' field"}), 400

    topic = data["topic"]
    if topic in data_store:
        del data_store[topic]
        return jsonify({"message": f"Record for topic '{topic}' deleted"}), 200
    else:
        return jsonify({"error": f"No record found for topic '{topic}'"}), 404

@app.route('/update', methods=['PUT'])
def update_topic():
    """
    PUT endpoint that accepts JSON with keys:topic, title, content, and num_links
    Updates the corresponding record in the in-memory store
    """
    data = request.get_json()
    required_fields = ["topic", "title", "content", "num_links"]
    if not data or not all(field in data for field in required_fields):
        return jsonify({"error": f"JSON must contain fields: {required_fields}"}), 400

    topic = data["topic"]
    if topic not in data_store:
        return jsonify({"error": f"No record found for topic '{topic}'"}), 404

    # Update the record in the in-memory store
    data_store[topic] = {
        "topic": topic,
        "title": data["title"],
        "content": data["content"][:100],
        "num_links": int(data["num_links"])}
    return jsonify({"message": f"Record for topic '{topic}' updated",
                    "record": data_store[topic]}), 200

@app.route('/save', methods=['POST'])
def save_to_postgres():
    """
    Endpoint to save current in-memory records to PostgreSQL
    Saves all records from the in-memory store to the table 'wiki.wikipedia_data'
    """
    #first initialize the DB schema and table
    init_db()

    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Could not connect to PostgreSQL."}), 500
    cur = conn.cursor()

    #insert or update each record
    for record in data_store.values():
        insert_query = """
        INSERT INTO wiki.wikipedia_data (topic, title, content, num_links)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (topic)
        DO UPDATE SET title = EXCLUDED.title,
                      content = EXCLUDED.content,
                      num_links = EXCLUDED.num_links;
        """
        cur.execute(insert_query, (record["topic"], record["title"], 
                                   record["content"], record["num_links"]))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "All records saved to PostgreSQL"}), 200

@app.route('/records', methods=['GET'])
def get_records():
    """
    GET endpoint that retrieves all records from the PostgreSQL table
    'wiki.wikipedia_data' and returns them as a JSON response
    """
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Could not connect to PostgreSQL"}), 500
    cur = conn.cursor()
    cur.execute("SELECT topic, title, content, num_links FROM wiki.wikipedia_data;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    
    records = []
    for row in rows:
        record = {
            "topic": row[0],
            "title": row[1],
            "content": row[2],
            "num_links": row[3]}
        records.append(record)
    
    return jsonify(records), 200

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)

