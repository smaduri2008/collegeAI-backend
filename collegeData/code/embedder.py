from sentence_transformers import SentenceTransformer
import json
import os


model = SentenceTransformer("all-MiniLM-L6-v2")

with open(".venv/data.json", "r") as f:
    data = json.load(f)

if(os.path.exists("../vectors.json")) and os.path.getsize("../vectors.json") > 0:
    with open(".venv/vectors.json", "r") as f:
        vectors = json.load(f)
else:
    vectors = []


for idx, doc in enumerate(data):
    text = doc["title"] + "".join(doc["comments"])
    embedding = model.encode(text).tolist()
    vectors.append({
        "index": idx,
        "embedding": embedding
    })

with open(".venv/vectors.json", "w", encoding="utf-8") as f:
    json.dump(vectors, f, ensure_ascii=False, indent=4)



