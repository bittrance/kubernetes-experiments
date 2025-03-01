import logging, os, time

logger = logging.getLogger('gunicorn.error')

def on_starting(server):
    startup_delay = float(os.getenv("HELLO_REST_STARTUP_DELAY", "0"))
    time.sleep(startup_delay)
    logger.info(f"Started up after {startup_delay} seconds")


