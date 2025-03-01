FROM python:3.13-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py gunicorn.conf.py .
USER nobody
ENTRYPOINT ["gunicorn"]
EXPOSE 8080
CMD ["--workers=4", "--bind=0.0.0.0:8080", "--graceful-timeout=60", "app:build()"]
