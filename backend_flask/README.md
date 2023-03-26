# Flask app using Lucene and BERT for search

## Introduction

This Flask app provides a search function that can use either Lucene or BERT to search through a collection of tweets. The app has been set up to allow Cross-Origin Resource Sharing (CORS), meaning it can be accessed by other domains.

## Requirements

To use this app, you need to have the following installed:

- Python 3.6 or later
- Flask
- Flask-Cors
- Lucene
- Transformers
- PyTorch
- Faiss

You'll also need to update the following file paths in `search.py` to point to your own indexes:
lucene_index_dir = "newluceneindex"
faiss_index_path = "newbertindex2"


Note that the `lucene_index_dir` variable should point to the directory containing the Lucene index, and the `faiss_index_path` variable should point to the file containing the Faiss index.

## Installation

1. Clone the repository to your local machine.
2. Install the required Python packages using `pip install -r requirements.txt`.
3. Update the file paths in `search.py` to point to your own indexes.
4. Run the app with `python app.py`.

## Usage

To use the app, navigate to `http://class-050.cs.ucr.edu:8888/search?search_query=test&k=100&search_type=lucene` in your browser, or use a tool like `curl` to make a request. The following parameters are required for the request:

- `search_query`: the text to search for
- `k`: the number of search results to return
- `search_type`: the type of search to use (`lucene` or `bert`)

Example request using `curl`:
curl -X GET "http://class-050.cs.ucr.edu:8888/search?search_query=test&k=100&search_type=lucene"

## Contributors
CS_242 IR Group 10
