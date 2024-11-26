from bs4 import BeautifulSoup
import os


with open(os.path.join(os.path.dirname(__file__), '../data/pandas/pandas.core.groupby.DataFrameGroupBy.std.html'), 'r') as f:
    html_content = f.read()
soup = BeautifulSoup(html_content, 'html.parser')
print(soup.h1)