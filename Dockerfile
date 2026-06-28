FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    libssl-dev \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .
COPY instagrapi/ ./instagrapi/

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -e . \
    && pip install --no-cache-dir fastapi uvicorn

RUN mkdir -p /app/sessions /app/data

COPY main.py .

EXPOSE 8989

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8989"]
