from flask import Flask, jsonify, request
import os
import requests
from tenacity import retry, stop_after_attempt, wait_exponential
import logging
from prometheus_flask_exporter import PrometheusMetrics

logger = logging.getLogger(__name__)

app = Flask(__name__)
metrics = PrometheusMetrics(app)
RETRY_COUNT = metrics.counter(
    'http_serivce_call_retries_total',
    'Total count of operation retries initiated within requests',
    labels={'endpoint': lambda: "unknown", # Default, set dynamically in callback
            'target_service': lambda: "unknown", # Default, set dynamically in callback
            'reason': lambda: "unknown"}        # Default, set dynamically in callback
)


def before_retry_callback(retry_state):
    endpoint = request.path if request else "flask-app1"
    downstream = "unknown"
    RETRY_COUNT.labels(
        endpoint=endpoint,
        target_service=target_service,
        reason="retry"
    ).inc()


class BlogService:
    def __init__(self):
        # Get the blog service URL from environment or use default kubernetes service DNS
        self.base_url = os.getenv("FLASK_APP2_SERVICE", "http://flask-app2-service:8082")  # kubernetes service name
        self.timeout = 3  # seconds

    @retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=1, max=8),
        before_sleep=before_retry_callback
    )
    def get_blog(self, blog_id):
        try:
            response = requests.get(
                f"{self.base_url}/blogs/{blog_id}",
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching blog {blog_id}: {str(e)}")
            raise

    @retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=1, max=8),
        before_sleep=before_retry_callback
    )
    def get_all_blogs(self):
        try:
            response = requests.get(
                f"{self.base_url}/blogs",
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching blog {blog_id}: {str(e)}")
            raise

    @retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=1, max=8),
        before_sleep=before_retry_callback
    )
    def post_blog(self):
        payload = {
            "title": "Test Blog",
            "content": "Test Content",
            "author": "Test Author"
        }
        try:
            response = requests.post(
                f"{self.base_url}/blogs",
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error post blog: {str(e)}")
            raise


blog_service = BlogService()

@app.route('/get_blog/<blog_id>')
def get_blog(blog_id):
    return blog_service.get_blog(blog_id)

@app.route('/post_blog', methods=["POST"])
def post_blog():
    return blog_service.post_blog()

@app.route('/get_all_blogs')
def get_all_blogs():
    return blog_service.get_all_blogs()

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

@app.route('/')
def hello():
    return jsonify({
        "message": "Hello from Flask!",
        "environment": os.getenv("ENVIRONMENT", "development")
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
