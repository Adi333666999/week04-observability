from flask import Flask, request, Response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# Define a Counter named 'http_requests_total'
REQUEST_COUNT = Counter(
 'http_requests_total', 
 'Total HTTP requests', 
 ['method', 'endpoint', 'status']
)

@app.after_request
def track_requests(response):
 # Increment REQUEST_COUNT with the corresponding labels
 REQUEST_COUNT.labels(
 method=request.method, 
 endpoint=request.path, 
 status=response.status_code
 ).inc()
 return response

@app.route('/')
def home():
 return "App is running!", 200

@app.route('/error')
def error():
 # Return an error message with HTTP status 500
 return "Internal Server Error", 500

@app.route('/metrics')
def metrics():
 # Return Prometheus metrics in the expected text format
 return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == '__main__':
 # Host 0.0.0.0 is mandatory so Docker/Kubernetes can reach it later
 app.run(host='0.0.0.0', port=5000)

