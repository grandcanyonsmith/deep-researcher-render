FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl && \
    rm -rf /var/lib/apt/lists/*

# Copy service code
COPY deep-researcher/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY deep-researcher/app.py /app/app.py
COPY deep-researcher/server.py /app/server.py

# Render expects Docker services to listen on $PORT (defaults to 10000)
EXPOSE 10000
ENV PORT=10000
CMD ["sh", "-lc", "uvicorn server:app --host 0.0.0.0 --port ${PORT:-10000}"]
