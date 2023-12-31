from flask import Flask, render_template, request, redirect, url_for
from elasticsearch import Elasticsearch
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

el_cnn = 'elasticsearch:9200'
el_name = 'elastic'
el_pass = 'abc123456'

def search_in_elasticsearch(query, page=1, page_size=10):
    # Создайте подключение к Elasticsearch
    es = Elasticsearch([el_cnn],
                       http_auth=(el_name, el_pass))

    # Определите запрос для Elasticsearch
    body = {
        "_source": [],
        "from": (page - 1) * page_size,
        "size": page_size,
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

# ------------------------------------------------------------------------

def count_pages(query, page_size=10):
    es = Elasticsearch([el_cnn],
                       http_auth=(el_name, el_pass))

    count_body = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["content"]
            }
        }
    }

    count_results = es.count(index="idx", body=count_body)
    total_results = count_results['count']

    total_pages = (total_results + page_size - 1) // page_size

    return total_pages

# ------------------------------------------------------------------------

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    logger.info('home')
    if request.method == 'GET':
        query = request.args.get('query', default="", type=str)
        
        page_number = request.args.get('page', default=1, type=int)
        page_size = 10  # Размер страницы
        total_pages = count_pages(query, page_size=page_size)
        
        if page_number < 1 or page_number > total_pages:
            page_number = 1
        
        logger.info("search")
        
        results = search_in_elasticsearch(query, page=page_number, page_size=page_size)
        
        logger.info(len(results))
        
        return render_template('index.html', results=results, query=query, current_page=page_number, total_pages=total_pages)
    return render_template('index.html')



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
