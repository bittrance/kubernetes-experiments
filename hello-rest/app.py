import logging, os, time

from datetime import datetime
from flask import Flask

logger = logging.getLogger('gunicorn.error')

app = Flask(__name__)

def build():
    app.request_delay = float(os.getenv("HELLO_REST_REQUEST_DELAY", "1.0"))
    return app

@app.route("/health")
def health():
    return "ok"

@app.route("/")
def hello_world():
    start = datetime.now().isoformat()
    logger.info(f"start request {start}")
    time.sleep(app.request_delay)
    end = datetime.now().isoformat()
    logger.info(f"end request {end}")
    return "<p>Hello, World!</p>"
