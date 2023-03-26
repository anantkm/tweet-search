import os
import argparse
from transformers import AutoTokenizer, AutoModel
import torch
import faiss
import json
import numpy as np

# Define command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("input_file", help="path to input JSON file")
parser.add_argument("output_file", help="path to output Faiss index file")
args = parser.parse_args()

# Load the sample data
with open(args.input_file) as f:
    data = json.load(f)

# Define the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-distilroberta-v1')
model = AutoModel.from_pretrained('sentence-transformers/all-distilroberta-v1')

# Batch size for processing the tweets
batch_size = 64

# Initialize the Faiss index
index = faiss.IndexFlatIP(768)  # Use the same dimension as the embedding size

# Check for existing index and progress
if os.path.exists(args.output_file):
    index = faiss.read_index(args.output_file)
    with open(args.output_file + ".progress", 'r') as f:
        start_index = int(f.read())
else:
    start_index = 0

# Calculate the total number of batches
total_batches = (len(data) + batch_size - 1) // batch_size

# Process the tweets in batches
for i in range(start_index, len(data), batch_size):
    batch = data[i:i + batch_size]
    texts = [entry['Text'] for entry in batch]

    # Tokenize the batch
    tokens = tokenizer(texts, max_length=512, truncation=True, padding='max_length', return_tensors='pt')

    # Generate embeddings for the batch
    with torch.no_grad():
        outputs = model(**tokens)
    embeddings = outputs.last_hidden_state

    # Apply attention mask to embeddings
    mask = tokens['attention_mask'].unsqueeze(-1).expand(embeddings.size()).float()
    masked_embeddings = embeddings * mask

    # Calculate mean-pooled embeddings
    summed_mask = torch.clamp(mask.sum(1), min=1e-9)
    summed = torch.sum(masked_embeddings, dim=1)
    mean_pooled = summed / summed_mask

    # Convert mean-pooled embeddings to numpy array
    mean_pooled = mean_pooled.numpy()

    # Add the embeddings to the index
    index.add(mean_pooled)

    # Save the index and progress
    faiss.write_index(index, args.output_file)
    with open(args.output_file + ".progress", 'w') as f:
        f.write(str(i + batch_size))

    # Print progress
    current_batch = i // batch_size + 1
    print(f"Indexed batch {current_batch} of {total_batches}")

print("BERT index created")
