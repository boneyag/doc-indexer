import os
from bs4 import BeautifulSoup

from src.indexer.document_index import APIDocIndex

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(asctime)s %(module)s %(levelname)s: %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    level=logging.INFO
)


def add_documents_to_index(file_path):
    doc_index = APIDocIndex()

    with open(file_path, 'r') as f:
        html_content = f.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    plain_text = soup.get_text()
    if soup.find('h1') is None:
        logger.error(f"Document {file_path} does not have a title")
        return
    title = soup.find('h1').text
    # remove the '#' at the end of the title
    if title.endswith('#'):
        title = title[:-1]
    doc_index.add_document(
        title=title,
        path=file_path,
        content=plain_text
    )


if __name__ == '__main__':
    for root, dirs, files in os.walk(os.path.join(os.path.dirname(__file__), '../data')):
        for file in files:
            if file.endswith('.html'):
                # logger.info(f"Adding document {file} to the index")
                add_documents_to_index(os.path.join(root, file))
