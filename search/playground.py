from search.index import Index
from search.load import load
import time


def build_index(load_data, index):
    for _, document in enumerate(load_data):
        index.index_document(document)

    return index

if __name__ == "__main__":
    index = Index()
    index = build_index(load('data/data.xml'), index)

    max_results = 5
    search_query = 'capitol riots'

    start_time = time.time()
    result = index.search(search_query)

    print(time.time() - start_time)
    if result == []: print('No results found')

    count = 0
    for doc in result:
        if count < max_results: 
            print(doc.title)
            count += 1
        else: 
            break
