from whoosh.fields import SchemaClass, TEXT, ID
from whoosh.analysis import StemmingAnalyzer


class APIDocSchema(SchemaClass):
    title = TEXT(stored=True)
    path = ID(stored=True, unique=True)
    content = TEXT(analyzer=StemmingAnalyzer(), stored=False)
