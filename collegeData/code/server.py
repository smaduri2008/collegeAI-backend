from flask import Flask, request, jsonify
from code.RAG import loadFile, response

app = Flask(__name__)

@app.route('/search', methods=['GET'])
def search():
    data = request.get_json()
    if not data or "query" not in data or len(data["query"]) == 0:
        return jsonify({"message": "No query provided"}), 400
    query = data["query"]
    embeddings = loadFile("vectors.json")

    res = response(query, embeddings, 3)
    return jsonify({"response": res}), 404


if __name__ == "__main__":
    app.run(debug=True, port = 5000)