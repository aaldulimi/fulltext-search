from index import Index
from load import load


def build_index(load_data, index):
    for _, document in enumerate(load_data):
        index.index_document(document)

    return index

if __name__ == "__main__":
    index = Index()
    index = build_index(load('data/data.xml'), index)

    max_results = 5
    search_query = 'COVID19 DONALD TRUMP'

    result = index.search(search_query)

    if result == []: print('No results found')

    count = 0
    for doc in result:
        if count < max_results: 
            print(doc.title)
            count += 1
        else: 
            break
