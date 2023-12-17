from flask import Flask, render_template, request, redirect, url_for
from elasticsearch import Elasticsearch
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def search_in_elasticsearch(query):
    # Создайте подключение к Elasticsearch
    es = Elasticsearch(['elasticsearch'])

    # Определите запрос для Elasticsearch
    body = {
        "query": {
            "match": {
                "content": query
            }
        },
        "sort": [
            {"_score": {"order": "desc"}}
        ]
    }

    # Выполните поиск в Elasticsearch
    results = es.search(index="idx", body=body)

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
        return render_template('results.html', results=results)
    return render_template('index.html')



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
