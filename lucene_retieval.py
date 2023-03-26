import os
import sys
import lucene
import json
import logging,sys
logging.disable(sys.maxsize)
from org.apache.lucene.document import Document,Field,FieldType
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.store import SimpleFSDirectory, NIOFSDirectory,MMapDirectory
from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import FieldInfo,IndexWriterConfig, IndexWriter, IndexOptions,DirectoryReader
from org.apache.lucene.search import IndexSearcher,BoostQuery,Query
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search.similarities import BM25Similarity
from org.apache.lucene.queryparser.classic import MultiFieldQueryParser

def retrieve_simplequery(store_dir, query):
    search_dir = NIOFSDirectory(Paths.get(store_dir))
    searcher = IndexSearcher(DirectoryReader.open(search_dir))
    parser = QueryParser('Text', StandardAnalyzer())
    parsed_query = parser.parse(query)
    top_docs = searcher.search(parsed_query, 5).scoreDocs
    top_k_docs = []
    for hit in top_docs:
        doc = searcher.doc(hit.doc)
        top_k_docs.append({
        "score": hit.score,
        "Text": doc.get("Text"),
        "User": doc.get("User"),
        "Timestamp":doc.get("Timestamp"),
        "Geolocation": doc.get("Geolocation"),
        "Tweet URL": doc.get("Tweet URL"),
        "External URLs": doc.get("External URLs"),
        "User Location": doc.get("User Location"),
        "Hashtag": doc.get("Hashtag"),})
    for result in top_k_docs:
        print("Score:", result["score"])
        print("Text:", result["Text"])
        print("User:", result["User"])
        print("Timestamp:", result["Timestamp"])
        print("Geolocation:", result["Geolocation"])
        print("Tweet URL:", result["Tweet URL"])
        print("External URLs:", result["External URLs"])
        print("User Location:", result["User Location"])
        print("Hashtag:", result["Hashtag"])
        print("\n")
lucene.initVM(vmargs=['-Djava.awt.headless=true'])
if len(sys.argv) < 3:
    print("Usage: python retrieving.py <index_dir> <query>")
    sys.exit(1)

index_dir = sys.argv[1]
query = sys.argv[2]
retrieve_simplequery(index_dir, query)