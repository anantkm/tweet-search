import argparse
import json
import numpy as np
import faiss
import torch
from transformers import AutoTokenizer, AutoModel

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Search FAISS index for a given query.")
parser.add_argument("index_path", help="Path to the FAISS index file.")
parser.add_argument("query", help="The query to search for.")
parser.add_argument("--k", type=int, default=100, help="Number of search results to return.")
parser.add_argument("--dataset-path", default="combined tweets.json", help="Path to the dataset file.")
args = parser.parse_args()

# Load dataset
with open(args.dataset_path) as f:
    data = json.load(f)

# Load pre-trained tokenizer and model
tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-distilroberta-v1')
model = AutoModel.from_pretrained('sentence-transformers/all-distilroberta-v1')

def convert_to_embedding(query):
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

# Load FAISS index and perform nearest neighbor search
query_embedding = convert_to_embedding(args.query)
index_loaded = faiss.read_index(args.index_path)
D, I = index_loaded.search(np.array([query_embedding]), args.k)

# Print search results
print("Top {} results for query '{}':".format(args.k, args.query))
for i in range(len(I[0])):
    passage = data[I[0][i]]
    print(" {}  Text: {}".format(i+1, passage['Text']))
    print("   User: {}".format(passage['User']))
    print("   Timestamp: {}".format(passage['Timestamp']))
    print("   Tweet URL: {}".format(passage['Tweet URL']))
    print("   Geolocation: {}".format(passage['Geolocation']))
    print("   Hashtag: {}\n".format(passage['Hashtag']))
