from flask import Flask, render_template, request, redirect, url_for
from elasticsearch import Elasticsearch
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def search_in_elasticsearch(query):
    # Создайте подключение к Elasticsearch
    es = Elasticsearch(['elasticsearch:9200'],
                       http_auth=('elastic', 'abc123456'))

    # Определите запрос для Elasticsearch
    body = {
        "_source": [],
        "size": 10,
        "query": {
            "multi_match" : {
            "query" : query,
            "fields" : ["content"]
            }
        },
        "highlight": {
            "fields": {
            "content": {}
            }
        }
    }
    
    # Выполните поиск в Elasticsearch
    logger.info(body)
    results = es.search(index="idx", body=body)
    # logger.info(results)

    # Верните результаты
    return results['hits']['hits']



app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    logger.info('home')
    if request.method == 'POST':
        query = request.form.get('query')
        logger.info("search")
        results = search_in_elasticsearch(query)
        logger.info(len(results))
        return render_template('index.html', results=results, query=query)
    return render_template('index.html')



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
