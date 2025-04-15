from sentence_transformers import SentenceTransformer, util
from huggingface_hub import InferenceClient
import numpy as np
import json
import os
import torch

hfToken = "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"

model = SentenceTransformer("all-MiniLM-L6-v2")

client = InferenceClient(model="mistralai/Mistral-7B-Instruct-v0.1", token=hfToken)

def loadFile(fileName):
    with open(fileName, "r") as f:
        return json.load(f)

def findSimilarities(query, embeddings, top_k = 3):
    similarities = []
    queryEmbedding = model.encode(query, convert_to_tensor=True)
    embeddings = loadFile(embeddings)
    for embedding in embeddings:
        doc_embedding = torch.tensor(embedding["embedding"]).to(queryEmbedding.device)
        sim = float(util.cos_sim(queryEmbedding, doc_embedding)[0][0])
        similarities.append((embedding, sim))

    #sort similarities array using the sim values rather than embedding values (to get highest sim)
    similarities.sort(key=lambda x: x[1], reverse=True)

    return similarities[:top_k]

def response(query, embeddings, top_k = 3):
   context = ""
   results = findSimilarities(query, embeddings, top_k)
   contextData = loadFile(".venv/data.json")
   for result in results:
       context += "".join(contextData[result[0]["index"]]["comments"]) + "\n"

   prompt = f"""### Instruction:
   Answer the user's question using ONLY the provided context below. 
   If the context is irrelevant, say "I don't have enough information about this", or answer it using your own knowledge.

   ### Question:
   {query}

   ### Context:
   {context}

   ### Response:
   """

   response = client.text_generation(
       prompt=prompt,
       max_new_tokens=300,
       temperature=0.3,
       do_sample=True,
       return_full_text=False,
   )

   return response


print(response("what are the differences between the SAT and ACT", "vectors.json", 3))









