import sqlite3
import pickle

conn = sqlite3.connect("embeddings.db")
cursor = conn.cursor()

cursor.execute("SELECT employee_id, embedding FROM face_embeddings")
rows = cursor.fetchall()

if not rows:
    print("❌ No embeddings found in database")
else:
    print("✅ Embeddings found:")
    for emp_id, blob in rows:
        emb = pickle.loads(blob)
        print(f"Employee ID: {emp_id}, Embedding length: {len(emb)}")
