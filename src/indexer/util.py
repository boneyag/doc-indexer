import re
from bs4 import BeautifulSoup

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(asctime)s %(module)s %(levelname)s: %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    level=logging.INFO
)


def has_py_class_or_function(css_class):
    if css_class in ['py class', 'py function', 'py property', 'py attribute', 'py method']:
        return css_class


def get_clean_text_from_html(html_content, library_name, api_name):
    soup = BeautifulSoup(html_content, 'html.parser')

    # if library_name == 'pandas':
    #     api_doc = soup.find('article', {"class": "bd-article", "role": "main"})
    #     api_doc_text = api_doc.text.strip()
    #     # additional whitespace removal
    #     clean_text = re.sub(r'\n{2,}', '\n', api_doc_text)
    #     return clean_text

    if library_name in ['matplotlib', 'pandas', 'numpy', 'seaborn', 'sklearn']:
        # logger.info(f"Isolating {api_name} content in {library_name} API doc")
        api_doc = soup.find_all('dl', class_=has_py_class_or_function)
        # logger.info(f"Found {len(api_doc)} possible hits")
        for item in api_doc:
            # TODO: check if the tool calling passes the API name or fully qualified name
            # if the fully qualified name is passed, only need to provide api_name to the regex
            if item.find('dt', {'id': re.compile(rf".*{api_name}")}):
                clean_text = re.sub(r'\n{2,}', '\n', item.text)
                return clean_text.strip()
        # print(api_doc_text)


if __name__ == '__main__':
    import os

    with open(os.path.join(os.path.dirname(__file__), '../data/matplotlib/dates_api.html'), 'r') as f:
        html_content = f.read()
    get_clean_text_from_html(html_content, 'matplotlib')
