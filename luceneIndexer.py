import os
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
import time
import matplotlib.pyplot as plt
import argparse

# Define command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("index_dir", help="path to the output index directory")
parser.add_argument("tweets_dir", help="path to the input JSON file containing tweet data")
args = parser.parse_args()

def create_index(docs, dir):
    if not os.path.exists(dir):
        os.mkdir(dir)
    start_time = time.time()
    x = []
    y = []
    document_count = 0
    store = SimpleFSDirectory(Paths.get(dir))
    analyzer = StandardAnalyzer()
    config = IndexWriterConfig(analyzer)
    config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
    writer = IndexWriter(store, config)
    contextType = FieldType()
    contextType.setStored(True)
    contextType.setTokenized(True)
    contextType.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)
    for doc in docs:
        text = doc['Text']
        user = doc['User']
        timestamp=doc['Timestamp']
        geolocation = str(doc['Geolocation'])
        tweet_url = doc['Tweet URL']
        external_urls = doc['External URLs']
        user_location = doc['User Location']
        hashtag = doc['Hashtag']
        doc = Document()
        doc.add(Field('Text', str(text), contextType))
        doc.add(Field('User', str(user), contextType))
        doc.add(Field('Timestamp',str(timestamp),contextType))
        doc.add(Field('Geolocation', str(geolocation), contextType))
        doc.add(Field('Tweet URL', str(tweet_url), contextType))
        doc.add(Field('External URLs', str(external_urls), contextType))
        doc.add(Field('User Location', str(user_location), contextType))
        doc.add(Field('Hashtag', str(hashtag), contextType))
        writer.addDocument(doc)
        document_count += 1
        end_time = time.time()
        run_time = end_time - start_time
        x.append(document_count)
        y.append(run_time)
    print("Index created")
    plt.plot(x, y)
    plt.xlabel("Number of Documents")
    plt.ylabel("Run Time (seconds)")
    plt.title("Lucene Index Creation Performance")
    plt.show()
    writer.close()
    plt.savefig("plot.png")

lucene.initVM(vmargs=['-Djava.awt.headless=true'])

with open(args.tweets_dir,'r') as f:
    docs = json.load(f)

create_index(docs, args.index_dir)
