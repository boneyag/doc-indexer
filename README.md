## Library document indexer and searcher

The project uses [Whoosh](https://whoosh.readthedocs.io/en/latest/indexing.html) to index and search library documents.

The script need the html files to be stored in the data directory (e.g.,`<project_root>/data/<lib_name>/*.html`). The html files are not included in here. Create the data directory and other subdirectories and put all the files that need to be indexed in the subdirectories. 

### Content of src/indexer
* schema.py - document index schema
* document_index.py - class that index documents and search the index
* util.py - support functions to extract only relevant parts from a html file after getting a hit in search
* add_documents.py - script that go through the data directory to add html files to the index
* search_documents.py - script that takes the search query and call the search function from the class (in the document_index.py)
