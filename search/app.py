from index import Index
from load import load


def build_index(load_data, index):
    for _, document in enumerate(load_data):
        index.index_document(document)

    return index

if __name__ == "__main__":
    index = Index()
    index = build_index(load('data/data.xml'), index)

    result = index.search('COVID-19 in europe')

    count = 0
    for doc in result:
        if count < 5: 
            print(doc.title)
            count += 1
        else: break
