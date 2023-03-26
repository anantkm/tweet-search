from flask import Flask, request, jsonify
from search import search_lucene, search_bert
import lucene
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.before_first_request
def init_jvm():
    lucene.initVM(vmargs=['-Djava.awt.headless=true', '-Djava.version=11'])
def load_index():
    global index_handler
    index_handler = IndexHandler()

@app.route('/search')
def search():
    # Get the parameters from the query string
    vm_env = lucene.getVMEnv()
    search_query = request.args.get('search_query')
    k = int(request.args.get('k'))
    search_type = request.args.get('search_type')

    # Check if the search type is 'lucene' or 'bert'
    if search_type == 'lucene':
        results = search_lucene(search_query)
    elif search_type == 'bert':
        results = search_bert(search_query)
    else:
        return 'Invalid search type'

    # Convert the search results to a JSON string and return it as the response
    print(results)
    response = jsonify(results)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == '__main__':
    app.run('0.0.0.0',port=8888)