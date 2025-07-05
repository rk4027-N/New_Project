from flask import Flask
from prometheus_client import generate_latest, Counter, Gauge
import time

app = Flask(__name__)

REQUESTS_TOTAL = Counter('http_requests_total', 'Total HTTP Requests', ['method', 'endpoint'])
IN_PROGRESS_REQUESTS = Gauge('http_requests_in_progress', 'In-progress HTTP Requests', ['method', 'endpoint'])
LAST_REQUEST_TIMESTAMP = Gauge('last_request_timestamp', 'Timestamp of the last request')

@app.route('/')
def hello():
    REQUESTS_TOTAL.labels(method='GET', endpoint='/').inc()
    IN_PROGRESS_REQUESTS.labels(method='GET', endpoint='/').inc()
    time.sleep(0.1)
    IN_PROGRESS_REQUESTS.labels(method='GET', endpoint='/').dec()
    LAST_REQUEST_TIMESTAMP.set(time.time())
    return "Hello from DevOps!"

@app.route('/metrics')
def metrics():
    return generate_latest()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
