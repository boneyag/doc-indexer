import os
import os.path
import re
from whoosh.index import create_in, open_dir
from whoosh.qparser import QueryParser

from src.indexer.schema import APIDocSchema
from src.indexer.util import get_clean_text_from_html

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(asctime)s %(module)s %(levelname)s: %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    level=logging.INFO
)

class APIDocIndex:
    def __init__(self):
        index_path = os.path.join(os.path.dirname(__file__), "../indexdir")
        if not os.path.exists(index_path) or not os.listdir(index_path):
            os.makedirs(index_path, exist_ok=True)
            self.ix = create_in(index_path, APIDocSchema)
        else:
            self.ix = open_dir(index_path)

    def add_document(self, title, path, content):
        with self.ix.searcher() as searcher:
            parser = QueryParser("path", self.ix.schema)
            query = parser.parse(path)
            results = searcher.search(query)

            if results:
                for result in results:
                    logger.info(f"Document with path {path} already exists in the index.")
                    with self.ix.writer() as writer:
                        writer.delete_by_term("path", result['path'])

        with self.ix.writer() as writer:
            writer.add_document(
                title=title,
                path=path,
                content=content
            )

    def count_num_docs(self):
        with self.ix.searcher() as searcher:
            print("Indexed Documents:")
            print(f"Number of documents: {searcher.doc_count()}")

    def print_index(self):
        with self.ix.searcher() as searcher:
            for term in searcher.lexicon("content"):
                print(term.decode("utf-8"))
            print("End of Index.")

    def search_index(self, query_word, library_name):
        print(f"Searching for: {query_word}")
        with self.ix.searcher() as searcher:
            query = QueryParser("content", self.ix.schema).parse(query_word)
            results = searcher.search(query)
            if results:
                for result in results:
                    if re.search(rf'\/data\/{library_name}\/', result['path']):
                        with open(result['path'], "r") as f:
                            html_content = f.read()
                        clean_text = get_clean_text_from_html(
                            html_content, library_name, query_word)
                        if clean_text:
                            print(clean_text)
            else:
                print("No results found")
