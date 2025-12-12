from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
CORS(app)  # Autorise les requêtes depuis le front

DB_HOST = os.getenv("DB_HOST", "tp_postgres")
DB_PORT = int(os.getenv("DB_PORT", 5432))
DB_NAME = os.getenv("DB_NAME", "tp")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

# NOUVELLE ROUTE
@app.route("/status")
def status():
    return jsonify({"status": "OK"})

@app.route("/items", methods=["GET"])
def get_items():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM items;")
    rows = cur.fetchall()
    conn.close()
    return jsonify(rows)

@app.route("/items", methods=["POST"])
def add_item():
    data = request.json
    name = data.get("name")
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO items (name) VALUES (%s) RETURNING id, name;", (name,))
    new = cur.fetchone()
    conn.commit()
    conn.close()
    return jsonify({"id": new[0], "name": new[1]}), 201

@app.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM items WHERE id=%s;", (item_id,))
    conn.commit()
    conn.close()
    return jsonify({"status": "deleted"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
