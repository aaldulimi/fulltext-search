from tokenizer import analyze
from load import load

class Index:
    def __init__(self):
        self.index = {}
        self.documents = {}

    def index_document(self, document):
        if document.id not in self.documents:
            self.documents[document.id] = document

        for token in analyze(document.body):
            if token not in self.index:
                self.index[token] = set()
            self.index[token].add(document.id)


    def _results(self, analyzed_query):
        return [self.index.get(token, set()) for token in analyzed_query]


    def search(self, query):
        analyzed_query = analyze(query)
        results = self._results(analyzed_query)
        documents = [self.documents[doc_id] for doc_id in set.intersection(*results)]

        return documents





    