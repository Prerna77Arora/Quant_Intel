FROM python:3.11-slim

WORKDIR /app

COPY backend/ /app/backend
COPY ml/ /app/ml
COPY data_pipeline/ /app/data_pipeline
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]