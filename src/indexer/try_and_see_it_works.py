from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID
from whoosh.analysis import StemmingAnalyzer
from whoosh.qparser import QueryParser
from bs4 import BeautifulSoup
import os, os.path
import re

schema = Schema(
        title=TEXT(stored=True),
        path=ID(stored=True),
        content=TEXT(stored=False, analyzer=StemmingAnalyzer())
    )

if not os.path.exists("indexdir"):
    os.mkdir("indexdir")
ix = create_in("indexdir", schema)
writer = ix.writer()

with open(os.path.join(os.path.dirname(__file__), "../data/pandas/pandas.DataFrame.T.html"), "r") as f:
    content = f.read()
    f_path = os.path.join(os.path.dirname(__file__), "../data/pandas/pandas.DataFrame.T.html")
soup = BeautifulSoup(content, 'html.parser')
plain_text = soup.get_text()
writer.add_document(title=u"pandas.DataFrame.T", path=f_path, content=plain_text)

with open(os.path.join(os.path.dirname(__file__), "../data/pandas/pandas.DataFrame.columns.html"), "r") as f:
    content = f.read()
    f_path = os.path.join(os.path.dirname(__file__), "../data/pandas/pandas.DataFrame.columns.html")
    soup = BeautifulSoup(content, 'html.parser')
plain_text = soup.get_text()
writer.add_document(title=u"pandas.DataFrame.columns", path=f_path, content=plain_text)
writer.commit()

with ix.searcher() as searcher:
    print("Indexed Documents:")
    print(searcher.doc_count())
    for term in searcher.lexicon("content"):
        print(term)
    print("End of Index.")

with ix.searcher() as searcher:
    query = QueryParser("content", ix.schema).parse("column")
    results = searcher.search(query)
    print(f"Number of hits: {len(results)}")
    if results:
        print(results[0])
        with open(results[0]['path'], "r") as f:
            html_content = f.read()
        soup = BeautifulSoup(html_content, 'html.parser')
        api_doc = soup.find('article', {"class": "bd-article", "role": "main"})
        api_doc_text = api_doc.text.strip()
        # additional whitespace removal
        clean_text = re.sub(r'\n{2,}', '\n', api_doc_text)
        print(clean_text)
    else:
        print("No results found")
