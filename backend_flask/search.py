import json
import lucene
import sys
import json
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.store import NIOFSDirectory
from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import FieldInfo, IndexWriterConfig, IndexWriter, IndexOptions, DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from transformers import AutoTokenizer, AutoModel
import torch
import faiss
import numpy as np

lucene_index_dir = "newluceneindex"
faiss_index_path = "newbertindex2"

def retrieve_simplequery(store_dir,query):
    vm_env = lucene.getVMEnv()
    vm_env.attachCurrentThread()
    search_dir = NIOFSDirectory(Paths.get(store_dir))
    searcher = IndexSearcher(DirectoryReader.open(search_dir))
    parser = QueryParser('Text', StandardAnalyzer())
    parsed_query = parser.parse(query)
    top_docs = searcher.search(parsed_query, 100).scoreDocs
    doc_list = []
    for hit in top_docs:
        doc = searcher.doc(hit.doc)
        doc_list.append({
            "Text": doc.get("Text"),
            "User": doc.get("User"),
            "User Location": doc.get("User Location"),
            "Timestamp": doc.get("Timestamp"),
            "Tweet URL": doc.get("Tweet URL"),
            "Geolocation": {
                "Longitude": doc.get("Longitude"),
                "Latitude": doc.get("Latitude")
            },
            "Hashtag": doc.get("Hashtag")
        })
    docjson = json.dumps(doc_list, ensure_ascii=False)
    # print(docjson)
    return docjson


def convert_to_embedding(query):
    tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-distilroberta-v1')
    model = AutoModel.from_pretrained('sentence-transformers/all-distilroberta-v1')

    tokens = {'input_ids': [], 'attention_mask': []}
    new_tokens = tokenizer.encode_plus(query, max_length=512,
                                       truncation=True, padding='max_length',
                                       return_tensors='pt')
    tokens['input_ids'].append(new_tokens['input_ids'][0])
    tokens['attention_mask'].append(new_tokens['attention_mask'][0])
    tokens['input_ids'] = torch.stack(tokens['input_ids'])
    tokens['attention_mask'] = torch.stack(tokens['attention_mask'])
    with torch.no_grad():
        outputs = model(**tokens)
    embedding = outputs.last_hidden_state.mean(dim=1)[0].numpy()
    return embedding

def search_faiss_index(index_path, query):
    with open('combined tweets.json') as f:
        data = json.load(f)

    query_embedding = convert_to_embedding(query)
    index_loaded = faiss.read_index(index_path)

    D, I = index_loaded.search(np.array([query_embedding]),100)
    doc_list = []
    for i in range(len(I[0])):
        passage = data[I[0][i]]
        doc_list.append({
            "Text": passage["Text"],
            "User": passage["User"],
            "User Location": passage["User Location"],
            "Timestamp": passage["Timestamp"],
            "Tweet URL": passage["Tweet URL"],
            "Geolocation": {
                "Longitude": passage["Geolocation"]["Longitude"],
                "Latitude": passage["Geolocation"]["Latitude"]
            },
            "Hashtag": passage["Hashtag"]
        })

    docjson = json.dumps(doc_list, ensure_ascii=False)
    # print(docjson)
    return docjson

def search_lucene(query):
    data = retrieve_simplequery(lucene_index_dir, query)
    return data


def search_bert(query):
    data = search_faiss_index(faiss_index_path,query )
    return data