

# CS 242: Information Retrieval & Web Search

Winter 2023

## **Build a Search Engine**

## **Team Members:**

1. Anant Krishna Mahale - amaha039
2. Nimalan Karthik Rajasekar - nraja024
3. Muralidhar Radhakrishnan - mradh001
4. Utkarsh Sinh - usinh002

## **Project Title:** "Twitter Data Analysis on COVID-19"

The Covid-19 pandemic has been a global health crisis, and social media platforms such as Twitter have been an important source of information and communication for people worldwide. The goal of this project is to build a Covid-19 related tweet search engine that allows users to search for tweets related to the pandemic and visualize their geolocation data on a map.

## a. Collaboration Details

The team consists of 4 members Anant, Nimalan, Muralidhar, and Utkarsh. The work distribution for the overall project is as follows:

Anant:

- In Part A, responsible for the overall design and implementation of the crawling system, including the architecture, crawling strategy, and collection of the dataset.
- In Part B, worked on building the frontend UI dashboard, including setting up the web services to interact with the backend and implementing the map in the React app.

Nimalan:

- In Part A, focused on cleaning the dataset and the implementation of the PyLucene Index retrieval logic to create indexes of text documents and perform efficient searches on those indexes.
- In Part B, worked on setting up the backend flask server and integrating the web services with the backend.

Murali:

- In Part A, focused on PyLucene Index creation, including the design choices for the PyLucene index and the generation of the Lucene index creation graph.
- In Part B, worked on implementing the BERT indexing for the collected dataset and the backend Python scripts to handle requests from the frontend.

Utkarsh:

- In Part A and B, responsible for testing and evaluating the performance of the system, as well as identifying any limitations and obstacles. In Part B, was also responsible for creating the frontend UI and worked with Anant to design and implement the website.

All members collaborated with Murali on index creation and retrieval as part of the project, and everyone contributed equally to the completion of the project report.

## b. Overview of the System

### **I. Architecture**

- **Overview:** In this project, we scraped tweets from Twitter using the Tweepy library and stored the extracted tweets in the form of a CSV and JSON file with the help of Pandas python library. Functions were in place to check the duplicate tweet before adding it to the dataset. The data was then processed and stored in a JSON file called "combined tweets.json" by extracting the required fields and removing duplicate tweets. The dataset was used to run the PyLucene and BERT indexing on the backend system. A flask server was set up in the backend system and Python scripts were written to use the created indexes to fetch relevant queries based on the user's search terms. The user sends in the search query by interacting with the web dashboard built using the Leaflet library in React to visualize the map and Flask to create a REST API that handles search queries using Lucene and BERT models.
- **Technologies Used:**  The following technologies were used in this project:
    - **React.js**: A JavaScript library for building user interfaces Leaflet: An open-source JavaScript library for interactive maps.
    - **Flask**: A Python web framework for building web applications.
    - **Lucene**: A search engine library written in Java.
    - **BERT**: A pre-trained language model for natural language processing.
    - **Faiss**: A library for efficient similarity search and clustering of dense vectors.
- **Implementation Details:**
    - **Frontend:** The front end of the project was built using React and the Leaflet library. The main component of the front end is the Map component, which renders a map with markers for each tweet that has valid geolocation data. The App component handles the search queries using the REST API and displays the search results in a list below the map. The user can enter a search query and select the search model (Lucene or BERT) to use. When the user submits the search query, the handleSubmit() function in the App component sends a request to the /search endpoint of the REST API, passing the search query, k, and search type as parameters. The search results are then displayed on the map and in the search results list.
    - **Backend:** The backend of the project was built using Flask and handled the search queries using Lucene and BERT models. The REST API has a single endpoint /search, which accepts the search_query, k, and search_type parameters in the query string. The search() function in the app.py file handles the search queries by calling the appropriate search function based on the search_type parameter. If the search_type is Lucene, then the search_lucene() function from search.py is called. If the search_type is BERT, then the search_bert() function from search.py is called. The results from the search function are returned as a JSON string in the response.

![The complete architecture of the project can be viewed in the architecture diagram above.](IR%20Final%20Report%20-%20Team%2010%20acd99a8d8f634222b8a761cdc2a21e0b/IR_(5).jpeg)

The complete architecture of the project can be viewed in the architecture diagram above.

### II. BERT indexing methodology

BERT is used to generate the index by converting the tweets into fixed-size embeddings that can be efficiently compared for similarity. This enables efficient and semantically rich search capabilities for the collection of tweets.

- **Model choice:** The chosen model is 'sentence-transformers/all-distilroberta-v1', a distilled version of the RoBERTa model fine-tuned specifically for sentence embeddings. This model was selected for its balance of performance and computational efficiency. The model and tokenizer are loaded using the Hugging Face Transformers library.
- **Indexing schema:**
    
    First, the script reads the tweet data from a JSON file. The tokenizer and model are then defined using the Hugging Face Transformers library. To process the tweets, a batch size is set, and the Faiss index is initialized with the same dimension as the embedding size (768).
    
    The tweets are processed in batches to optimize computational efficiency. For each batch, the tweets are tokenized using the tokenizer. The tokenization process involves truncating or padding the tweets as necessary to achieve a maximum length of 512 tokens. Once the tweets are tokenized, they are fed into the model, which generates embeddings for each tweet.
    
    To refine the embeddings, the attention mask is applied to retain only the relevant information and discard the padded tokens. Afterward, mean-pooled embeddings are calculated by summing the masked embeddings along the token dimension and dividing by the number of non-padded tokens in each tweet.
    

### **III. BERT indexing for ranking**

The BERT index is used to rank the results by measuring the similarity between the query embedding and the tweet embeddings in the index. By comparing these similarity scores, the script can determine which tweets are the most relevant to the user's query, effectively ranking them accordingly.

Firstly, the script takes a user-provided query and uses the same tokenizer and model ('sentence-transformers/all-distilroberta-v1') as during the index creation to convert the query into a fixed-size vector or embedding. This step ensures that the query and the indexed tweets are represented in the same vector space, allowing for comparison and similarity calculations.

Next, the generated query embedding is used to search the Faiss index. Faiss computes the similarity between the query embedding and the embeddings of the tweets in the index. The similarity measure employed in this case is the inner product (dot product) between the embeddings. This choice is reflected in the index initialization as faiss.IndexFlatIP(768).

After obtaining the similarity scores, the script ranks the results. Higher scores indicate greater similarity between the query and the tweet embeddings. By comparing these scores, the script can determine which tweets are most relevant to the user's query.

Finally, the script retrieves the top results (in this case, the top 5) by selecting the highest-ranked tweet embeddings based on their similarity scores. It then prints the associated tweet text and metadata for each of the top-ranked results, providing the user with the most relevant tweets for their query.

### **IV. Lucene indexing**

The user's query is parsed by calling the parse method on the QueryParser object, generating a parsed query object. The search method is executed on the IndexSearcher object, utilizing the parsed query and the number of results to be retrieved. The search method returns a TopDocs object containing the top-scoring documents. Results are collected in a list of dictionaries containing the document's metadata and score before being printed to the console.

In this retrieval script, a simple QueryParser is used to search only the 'Text' field. To search multiple fields in the Lucene index, the MultiFieldQueryParser can be employed. This parser allows you to search across multiple fields, which is useful when you want to find documents that match the query terms in different fields.

The StandardAnalyzer is used in these scripts because it is well-suited for processing tweets. It performs tokenization, lowercase filtering, and stopword removal. Tokenization is essential for breaking down text into individual words, while lowercase filtering ensures a case-insensitive search, making it more robust. Stopword removal helps in discarding common words that do not carry significant meaning, thereby improving search efficiency. For tweet analysis, the StandardAnalyzer is a suitable choice because it can effectively handle short and informal text, such as the language commonly found on social media platforms. This analyzer can process the unstructured nature of tweets and extract meaningful information, allowing for more accurate search results.

The StandardAnalyzer in the PyLucene index was used in this project. The StandardAnalyzer is a good choice for general text analysis. It tokenizes the input text into separate words, removes stop words (common words like "the" and "and" that do not provide much value for searching), and converts all the words to lowercase. This helps to improve the precision and recall of search results.

The EnglishAnayzer was initially used for the text analysis, but multiple tweets had words which were not entirely in the English language, hence the more general-purpose StandardAnalyzer was chosen over the EnglishAnalyzer.

### **V. Comparison of the run time of the BERT and Lucene index construction and retrieval**

A graph has been plotted to report on the runtime of the Lucene and BERT Index creation process. In the graph, the x-axis contains the number of documents indexed and the y-axis has the run time to index the documents. The run time is got by the difference between the end time and start time in each iteration when a document is added to the index. The runtime and number of documents are added to two lists and the graph is plotted using matplotlib.

![The above graph for Lucene depicts that the runtime increases proportionately as the number of documents increases.](IR%20Final%20Report%20-%20Team%2010%20acd99a8d8f634222b8a761cdc2a21e0b/plot.png)

The above graph for Lucene depicts that the runtime increases proportionately as the number of documents increases.

![While this BERT indexing graph shows that the runtime increases linearly as the number of documents increases.](IR%20Final%20Report%20-%20Team%2010%20acd99a8d8f634222b8a761cdc2a21e0b/bert_runtime_plot.png)

While this BERT indexing graph shows that the runtime increases linearly as the number of documents increases.

![The above graph represents the time taken for querying a single word in both Lucene and BERT for 10 to 10000 results.](IR%20Final%20Report%20-%20Team%2010%20acd99a8d8f634222b8a761cdc2a21e0b/singleWork_Runtime.png)

The above graph represents the time taken for querying a single word in both Lucene and BERT for 10 to 10000 results.

![The above graph represents the time taken for querying 3 words in both Lucene and BERT for 10 to 10000 results.](IR%20Final%20Report%20-%20Team%2010%20acd99a8d8f634222b8a761cdc2a21e0b/longWork_Runtime.png)

The above graph represents the time taken for querying 3 words in both Lucene and BERT for 10 to 10000 results.

The graphs were plotted for a small sample of tweets to visualize the relationship between the time taken for indexing and the number of tweets. As seen from the graphs above, PyLucene takes about 0.25 seconds to index 1000 tweets whereas BERT takes about 300 seconds to index 1000 tweets. The difference in time is extremely high of the order 1200 times, hence this explains the constraints we faced while trying to index using BERT.

As seen from the above figure, the time taken for querying increases with the increase in the number of results for Lucene. But that is not the case with BERT, where the time remains constant for any number of tweets. This trend is observed for both single-word queries and multiple-word queries.

### VI. Comparison between the quality of the rankings between Lucene and BERT

It is difficult to make a conclusive comparison between Lucene and BERT in terms of the quality of rankings since their strengths and weaknesses vary depending on the dataset and search requirements. Moreover, the BERT index used in the report was built on a smaller dataset, which may limit its performance in larger datasets. Nevertheless, some general observations can be made based on the report:

- **PyLucene** is a flexible and efficient search engine library suitable for both small and large datasets. It is optimized for keyword-based searches and can handle complex search logic. PyLucene can provide fast and accurate search results based on the presence of specific keywords or phrases in the documents, and it supports multiple fields in the index for advanced search capabilities.
- **BERT**-based search solutions are designed to capture semantic relationships between documents and provide a deeper understanding of the content. BERT can generate semantically rich embeddings that enable efficient and accurate similarity search. It can be beneficial for search tasks in datasets of various sizes, from small to large, where understanding the meaning and context is crucial.
- The choice between **PyLucene** and a **BERT**-based search solution (or combining them) depends on the specific dataset and search requirements. PyLucene is a good choice when efficient keyword-based searches are sufficient, while BERT-based search solutions are more appropriate when semantic understanding and capturing the relationships between documents are essential.

Based on these observations, it can be said that both PyLucene and BERT have their own strengths and weaknesses in terms of the quality of rankings. One model may be better suited than the other in specific cases depending on the dataset, search requirements and the need for semantic understanding in the search process.

Based on our observation, we found out that since the length of tweets is not significantly large, the two indices perform reasonably well as can be seen from the below example. But for instances, where the search query is longer, we saw that BERT performed better than Lucene. Also, we noticed, BERT takes the context of the search queries into consideration, whereas Lucene uses direct keyword matching.
  

![Lucene Tweet example for the query “covid quarantine help”](IR%20Final%20Report%20-%20Team%2010%20acd99a8d8f634222b8a761cdc2a21e0b/luceneexample.jpg)

Lucene Tweet example for the query “covid quarantine help”

![BERT Tweet example for the query “covid quarantine help”](IR%20Final%20Report%20-%20Team%2010%20acd99a8d8f634222b8a761cdc2a21e0b/bertExample.jpg)

BERT Tweet example for the query “covid quarantine help”

## **c. Limitations of the System**

Bert index which we created is for a smaller dataset than what Pylucene was indexed for, This is because BERT indexing is more time-consuming and demanding than Lucene indexing, which led to timeout issues and crashes when running the BERT indexing process on our server. So we had to make BERT indexing to be able to resume from where the indexing process stopped during the crash and index our tweets in batches, but even this was troublesome if the index file gets corrupted during a crash then a new index file needs to be created and indexing is done from the start. Hence our BERT model was indexed on a 500MB dataset instead of the complete 1.7Gb dataset.

In our initial implementation, we attempted to use Geolib to obtain the geolocation data for tweets with user location data. However, due to limitations in the Geolib library, we were unable to obtain reliable geolocation data for all tweets. As a result, we decided to randomly plot the tweets on the map that do not have geolocation data. This was done purely for illustrative purposes to demonstrate the functionality of the map and is not intended to represent the actual geolocation of the tweets.

## **d. Obstacles and Solutions**

During the course of working on this project, we encountered the following issues. An explanation of what the problem was and how we resolved them has been summarized below.

### I. Excessive time is taken during BERT indexing

While indexing using BERT, the indexing process took a lot of time (>24hrs) as our initial dataset was of the order of 1.7GB. The indexing process was also failing in between due to timeout issues. We resolved this issue by modifying the index code to process the tweets in batches and save the current status after every batch. If there were to be a failure during the indexing process, the code will read the already written index file and resume from the point right before the crash. Due to the above issues, we were only able to index data worth about 500MB.

### II. Twitter data does not have enough geotagged tweets

Only About 20% of the tweets collected were geotagged. Hence the probability of the tweets returned based on our query to have geographical information is small. We tried the ‘Nominatim API’ to get the location information but faced issues as mentioned in the next point. In order to visualize our results in a better way on the map in our web dashboard, we resorted to adding random geolocations using the Geolib library to tweets which did not have any geolocation information. This was done purely for illustrative purposes on the dashboard and does may not reflect the actual location.

### III. **Nominatim API limitation for tweet location lookup**

To try and resolve the above issue, we tried using an API called Nominatim. Nominatim uses OpenStreetMap data to find locations on Earth by name and address (geocoding). But there was a limitation of 1000 tweets per day to retrieve the location information. Hence we had to resort to random geolocation generation as mentioned above.

### IV. **Setting up the backend server.**

During the setup process of the backend server, we tried setting up a flask server but faced connection issues. Hence we tried other approaches such as remote connection use Paramiko, which is a Python implementation of the SSHv2 protocol, providing both client and server functionality. This again caused issues while trying to connect to the cs242 client. We finally resolved the issue by setting up a Flask server and establishing a connection through port 8888 which was being used by Jupyter Notebooks.

### V. Crawling of Twitter Data.

One of the main obstacles encountered was during crawling, the crawler was only able to collect around 2000 tweets per minute. To gather a large enough dataset we had to run the crawler on multiple machines after which we were able to collect 1.7Gb of data.

## **e. Instructions on how to deploy the system.**

### I. **Instruction on how to Deploy the Crawler**

To deploy the crawler, these steps need to be followed:

1. Install Python and the required dependencies. This can be done by running ‘install_dependencies.sh’ bash file.
2. Clone the source code from the repository.
3. Open a terminal window and navigate to the directory containing the code.
4. Run by using command : python scrapper.py <action> --hashtag <HASHTAG> Example: python scrapper.py scrapper --hashtag covid19 or python scrapper.py process

### II. **Running the Project: Instructions for Retrieving and Querying the Index**

1. Ensure that all necessary dependencies are installed.
2. To retrieve the Lucene Index and query it, follow these steps:
    1. In the terminal, navigate to the location of the code.
    2. To index the data, run **[indexer.sh](http://indexer.sh)** with the command `**./index.sh <lucene/bert> <path to dataset.json> <path to indexer>.**` For example, if you want to index tweets using Lucene, run `**./index.sh lucene input_tweets.json lucene_index.**`
    3. To query the Bert indexer, use `**python3 bert_retrieval.py <path/to/index_file> <query_string> [--k <num_results>] [--dataset-path <path/to/dataset_file>].**`
    4. To query the Lucene indexer, use `**python3 <path/to/lucene_retrieval.py> <path/to/index_dir> <query_string>.**`
3. To run the backend Flask app, follow these steps:
    
    a. Clone the repository to your local machine.
    
    b. Install the required Python packages by running **pip install -r requirements.txt**.
    
    c. Update the file paths in `**search.py**` to point to your own indexes.
    
    d. Run the app with the command **`python3 app.py.`**
    
4. To run the frontend, follow these steps:
    1. Navigate to the folder.
    2. Run **`start_React.sh**.`
    3. Note: The project uses the following dependencies and you may need to make the .sh file executable by running `**chmod +x filename.sh**`
        - React
        - axios
        - antd
        - leaflet
        - leaflet.markercluster
        - react-dom
        - react-scripts
        - react-router-dom

## g. **Screenshots showing the system in action.**

![The above screenshot demonstrates that **Pylucene** is performing well with shorter queries](IR%20Final%20Report%20-%20Team%2010%20acd99a8d8f634222b8a761cdc2a21e0b/Untitled.png)

The above screenshot demonstrates that **Pylucene** is performing well with shorter queries

![The above screenshot demonstrates that **BERT** is performing well with shorter queries](IR%20Final%20Report%20-%20Team%2010%20acd99a8d8f634222b8a761cdc2a21e0b/Untitled%201.png)

The above screenshot demonstrates that **BERT** is performing well with shorter queries

![The above screenshot demonstrates that BERT is performing well with longer queries as well](IR%20Final%20Report%20-%20Team%2010%20acd99a8d8f634222b8a761cdc2a21e0b/Untitled%202.png)

The above screenshot demonstrates that BERT is performing well with longer queries as well

![The above screenshot demonstrates that Pylucene performs well with longer queries.](IR%20Final%20Report%20-%20Team%2010%20acd99a8d8f634222b8a761cdc2a21e0b/Untitled%203.png)

The above screenshot demonstrates that Pylucene performs well with longer queries.

![This above is a screenshot of the terminal showing the backend in operation.](IR%20Final%20Report%20-%20Team%2010%20acd99a8d8f634222b8a761cdc2a21e0b/Untitled%204.png)

This above is a screenshot of the terminal showing the backend in operation.

## **h. Conclusion**

In conclusion, this project demonstrates how to build a Covid-19-related tweet search engine using Lucene and BERT models. The project allows users to search for tweets related to the pandemic and visualize their geolocation data on a map. The front end of the project was built using React and the Leaflet library, while the back end was built using Flask and Lucene. The REST API handles the search queries using Lucene and BERT models and returns the search results as a JSON string. The project can be extended to include more search models and additional features such as sentiment analysis and topic modelling. However, limitations in external libraries may pose challenges in obtaining accurate geolocation data for tweets.
