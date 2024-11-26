from src.indexer.document_index import APIDocIndex


def search_documents_in_index(query_word, library_name):
    doc_index = APIDocIndex()
    doc_index.search_index(query_word, library_name)


if __name__ == '__main__':
    search_documents_in_index("OneHotEncoder", "sklearn")
