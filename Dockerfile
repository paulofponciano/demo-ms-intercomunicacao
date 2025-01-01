FROM python:3.9-slim

WORKDIR /app

COPY app/ /app/

RUN pip install --no-cache-dir -r requirements.txt

ENV TITLE="Default Title" \
    RESPONSE_TIME=0 \
    EXTERNAL_CALL_URL="" \
    EXTERNAL_CALL_METHOD="GET" \
    HTTP_PORT=5000

EXPOSE 5000

CMD ["python", "main.py"]