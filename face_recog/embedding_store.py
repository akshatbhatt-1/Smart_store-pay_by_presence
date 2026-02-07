import sqlite3
import pickle

DB_PATH = "embeddings.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Create table (once)
cursor.execute("""
CREATE TABLE IF NOT EXISTS face_embeddings (
    employee_id TEXT PRIMARY KEY,
    embedding BLOB
)
""")
conn.commit()

def save_embedding(employee_id, embedding):
    blob = pickle.dumps(embedding)
    cursor.execute(
        "REPLACE INTO face_embeddings VALUES (?, ?)",
        (employee_id, blob)
    )
    conn.commit()

def load_embeddings():
    cursor.execute("SELECT employee_id, embedding FROM face_embeddings")
    rows = cursor.fetchall()
    return {
        emp_id: pickle.loads(blob)
        for emp_id, blob in rows
    }
