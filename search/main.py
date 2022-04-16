from fastapi import FastAPI
import uvicorn 
from search.index import Index
from search.load import load
import time

 
def build_index(load_data, index):
    for document in load_data:
        index.index_document(document)

    return index

app = FastAPI()
index = Index()
index = build_index(load('data/data.xml'), index)

@app.get("/index/search")
async def search_index(query: str = 'football', limit: int = 5):
    results_json = {}
    results_json['results'] = []

    start_time = time.time()
    result = index.search(query)
    compute_time = time.time()

    count = 0
    for doc in result:
        if count < limit:
            doc_json = {}
            doc_json['title'] = doc.title
            doc_json['author'] = doc.author
            doc_json['body'] = doc.body
            doc_json['datetime'] = doc.datetime
            doc_json['url'] = doc.url

            results_json['results'].append(doc_json)
            count += 1
        else:
            break
    
    results_json['seconds'] = compute_time - start_time
    results_json['count'] = count

    return results_json


def start():
    """Launched with `poetry run start` at root level"""
    uvicorn.run("search.main:app", host="0.0.0.0", port=8000, reload=True)
