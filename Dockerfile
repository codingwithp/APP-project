FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    cmake \
    build-essential \
    libboost-all-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
COPY service.json /app/service.json


COPY . .

ENV FLASK_RUN_HOST=0.0.0.0

EXPOSE 8000

CMD ["python", "app.py"]
